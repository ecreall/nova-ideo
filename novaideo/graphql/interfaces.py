import graphene
from graphene import relay

from substanced.util import get_oid

from .util import get_actions


class IEntity(relay.Node):
    
    oid = graphene.String()
    title = graphene.String()
    created_at = graphene.String()
    state = graphene.List(graphene.String)
    actions = graphene.List(
        'novaideo.graphql.schema.Action',
        process_id=graphene.String(),
        node_ids=graphene.List(graphene.String))

    def resolve_created_at(self, args, context, info):
        return self.created_at.isoformat()

    def resolve_oid(self, args, context, info):  # pylint: disable=W0613
        return get_oid(self, None)

    def resolve_actions(self, args, context, info):  # pylint: disable=W0613
        return get_actions(self, context, args)