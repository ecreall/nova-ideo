import graphene

from ..util import get_execution_data
from novaideo import _



class Select(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    context = graphene.Field('novaideo.graphql.schema.EntityUnion')
    action_id = 'novaideoabstractprocess.select'

    @staticmethod
    def mutate(root, args, context, info):
        args = dict(args)
        context, request, action, args = get_execution_data(
            Select.action_id, args)
        status = False
        if action:
            action.execute(context, request, {})
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return Select(context=context, status=status)


class Deselect(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    context = graphene.Field('novaideo.graphql.schema.EntityUnion')
    action_id = 'novaideoabstractprocess.deselect'

    @staticmethod
    def mutate(root, args, context, info):
        args = dict(args)
        context, request, action, args = get_execution_data(
            Deselect.action_id, args)
        status = False
        if action:
            action.execute(context, request, {})
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return Deselect(context=context, status=status)
