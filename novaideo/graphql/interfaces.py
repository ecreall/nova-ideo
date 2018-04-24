import graphene
from graphene import relay

from substanced.util import get_oid

from .util import get_actions, ResolverLazyList, get_all_comments


class IDebatable(relay.Node):

    channel = graphene.Field('novaideo.graphql.schema.Channel',)
    comments = relay.ConnectionField(
        'novaideo.graphql.schema.Comment',
        filter=graphene.String())
    len_comments = graphene.Int()

    def resolve_channel(self, args, context, info):
        if not hasattr(self, 'get_channel'):
            return None

        return self.get_channel(getattr(context, 'user', None))

    def resolve_comments(self, args, context, info):
        if not hasattr(self, 'get_channel'):
            return []

        channel = self.get_channel(getattr(context, 'user', None))
        total_count, oids = get_all_comments(channel, args)
        return ResolverLazyList(
            oid,
            Comment,
            total_count=total_count)

    def resolve_len_comments(self, args, context, info):
        if not hasattr(self, 'get_channel'):
            return 0

        channel = self.get_channel(getattr(context, 'user', None))
        return channel.len_comments if channel else 0


class IEntity(relay.Node):

    oid = graphene.String()
    title = graphene.String()
    created_at = graphene.String()
    state = graphene.List(graphene.String)
    actions = graphene.List(
        'novaideo.graphql.schema.Action',
        action_tags=graphene.List(graphene.String),
        process_tags=graphene.List(graphene.String),
        process_ids=graphene.List(graphene.String),
        node_ids=graphene.List(graphene.String))
    evaluation_stats= graphene.Field('novaideo.graphql.schema.EvaluationStats')
    examination_stats= graphene.Field('novaideo.graphql.schema.ExaminationStats')
    nb_followers = graphene.Int()

    def resolve_created_at(self, args, context, info):
        return self.created_at.isoformat()

    def resolve_oid(self, args, context, info):  # pylint: disable=W0613
        return get_oid(self, None)

    def resolve_actions(self, args, context, info):  # pylint: disable=W0613
        return get_actions(self, context, args)

    def resolve_evaluation_stats(self, args, context, info):  # pylint: disable=W0613
        return self

    def resolve_examination_stats(self, args, context, info):  # pylint: disable=W0613
        return self

    def resolve_nb_followers(self, args, context, info):  # pylint: disable=W0613
        return getattr(self, 'len_selections', 0)
