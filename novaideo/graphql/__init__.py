from graphql_wsgi import graphql_wsgi
from .schema import schema

graphql = graphql_wsgi(schema.schema)


def graphqlview(context, request):
    return graphql(request)


def includeme(config):
    config.add_route('graphql', '/graphql')
    config.add_view(graphqlview, route_name='graphql')
    config.add_route('graphiql', '/graphiql')
    config.add_view(route_name='graphiql', renderer='graphiql.pt')
    config.add_static_view('graphiql',
                           'novaideo:graphql/build')
