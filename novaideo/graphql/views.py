# -*- coding: utf-8 -*-
"""GraphQL view."""
import json
import datetime
import pytz
from dace.objectofcollaboration.principal.util import has_role
from dace.util import find_catalog
from graphql_wsgi import graphql_wsgi
from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.request import Response
from pyramid.view import view_config
from pyramid.security import remember, forget

from substanced.util import get_oid
from substanced.event import LoggedIn

from novaideo.content.interface import IPerson
from .schema import schema, get_user_by_token


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
    if is_private and not auth_user(token, request):
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
            headers = remember(request, get_oid(user))
            request.registry.notify(LoggedIn(login, user, context, request))
            user.last_connection = datetime.datetime.now(tz=pytz.UTC)
            if hasattr(user, 'reindex'):
                user.reindex()

            request.response.headerlist.extend(headers)
            return {
                'status': True,
                'token': user.api_token
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
           
        

