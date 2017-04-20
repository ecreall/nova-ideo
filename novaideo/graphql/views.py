# -*- coding: utf-8 -*-
"""GraphQL view."""
from graphql_wsgi import graphql_wsgi
from pyramid.view import view_config
from pyramid.request import Response

from .schema import schema


@view_config(
    request_method='OPTIONS',
    route_name='graphql'
)
@view_config(
    request_method='POST',
    route_name='graphql'
)
def graphqlview(context, request):  #pylint: disable=W0613
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
