# -*- coding: utf-8 -*-
"""GraphQL view."""
import json
import datetime
import pytz
import uuid
from dace.objectofcollaboration.principal.util import has_role
from dace.util import find_catalog
from graphql_wsgi import graphql_wsgi
from graphql_wsgi.main import parse_body, get_graphql_params
from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.request import Response
from pyramid.view import view_config
from pyramid.security import remember, forget

from substanced.util import get_oid
from substanced.event import LoggedIn

from novaideo.content.interface import IPerson
from .schema import schema
from .util import get_user_by_token

AUTHORIZED_QUERIES = ['SiteData', 'Registration', 'ConfirmRegistration', 'ResetPassword', 'ConfirmResetPassword']

def auth_user(token, request):
    current_user = None
    user = get_user_by_token(token)
    if (has_role(user=user, role=('SiteAdmin', )) or
            'active' in getattr(user, 'state', [])):
        current_user = user
        request.user = current_user

    return current_user


@view_config(
    request_method='OPTIONS',
    route_name='graphql'
)
@view_config(
    request_method='POST',
    route_name='graphql',
    renderer='json'
)
def graphqlview(context, request):  #pylint: disable=W0613
    token = request.headers.get('X-Api-Key', '')
    is_private = getattr(request.root, 'only_for_members', False)
    auth = auth_user(token, request)
    if is_private and not auth:
        to_verify = False
        try:
            query, variables, operation_name = get_graphql_params(
                request, parse_body(request))
            if operation_name not in AUTHORIZED_QUERIES:
                to_verify = True
        except:
            to_verify = True
        
        if to_verify:
            response = HTTPUnauthorized()
            response.content_type = 'application/json'
            return response

    if request.method == 'OPTIONS':
        response = Response(status=200, body=b'')
        response.headerlist = []  # we have to reset headerlist
        response.headerlist.extend(
            (
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Headers', 'Content-Type'),
            )
        )
    else:
        solver = graphql_wsgi(schema)
        response = solver(request)
        response.headerlist.append(
            ('Access-Control-Allow-Origin', '*')
        )

    return response


@view_config(request_method='POST', name='json_login', renderer='json')
def login(context, request):
    login_data = json.loads(request.body.decode())
    login = login_data.get('login', None)
    password = login_data.get('password', None)
    token = login_data.get('token', None)
    logged_user = None
    if token:
        logged_user = auth_user(token, request)

    if login and password:
        novaideo_catalog = find_catalog('novaideo')
        dace_catalog = find_catalog('dace')
        identifier_index = novaideo_catalog['identifier']
        object_provides_index = dace_catalog['object_provides']
        query = object_provides_index.any([IPerson.__identifier__]) &\
            identifier_index.any([login])
        users = list(query.execute().all())
        user = users[0] if users else None
        valid_check = user and user.check_password(password)
        if valid_check and \
           (has_role(user=user, role=('SiteAdmin', )) or \
           'active' in getattr(user, 'state', [])):
            logged_user = user
            if getattr(logged_user, 'api_token', None) is None:
                logged_user.api_token = uuid.uuid4().hex

    if logged_user:
        headers = remember(request, get_oid(logged_user))
        request.registry.notify(LoggedIn(login, logged_user, context, request))
        logged_user.last_connection = datetime.datetime.now(tz=pytz.UTC)
        request.response.headerlist.extend(headers)
        if hasattr(logged_user, 'reindex'):
            logged_user.reindex()

        return {
            'status': True,
            'token': logged_user.api_token
        }

    return {
        'status': False,
        'token': None
    }


@view_config(request_method='POST', name='json_logout')
def logout(context, request):
    headers = forget(request)
    data = {
        'status': True
    }
    return Response(json=data, status=200, headerlist=headers)


@view_config(request_method='POST', name='json_validate_login', renderer='json')
def validate_login(context, request):
    login_data = json.loads(request.body.decode())
    login = login_data.get('login', None)
    user= None
    if login:
        novaideo_catalog = find_catalog('novaideo')
        dace_catalog = find_catalog('dace')
        identifier_index = novaideo_catalog['identifier']
        object_provides_index = dace_catalog['object_provides']
        query = object_provides_index.any([IPerson.__identifier__]) &\
            identifier_index.any([login])
        users = list(query.execute().all())
        user = users[0] if users else None
    
    return {'status': True if user else False}
