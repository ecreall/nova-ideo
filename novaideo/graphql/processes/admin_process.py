import graphene
import dateutil.parser

from ..util import get_execution_data
from novaideo import _



class AddDeadline(graphene.Mutation):

    class Input:
        context = graphene.String()
        date = graphene.String()

    root = graphene.Field('novaideo.graphql.schema.Root')
    action_id = 'novaideoabstractprocess.adddeadline'

    @staticmethod
    def mutate(root, args, context, info):
        args = dict(args)
        context, request, action, args = get_execution_data(
            AddDeadline.action_id, args)
        if action:
            date = dateutil.parser.parse(args['date'])
            action.execute(context, request, {'deadline': date})
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return AddDeadline(root=context)


class EditDeadline(graphene.Mutation):

    class Input:
        context = graphene.String()
        date = graphene.String()

    root = graphene.Field('novaideo.graphql.schema.Root')
    action_id = 'novaideoabstractprocess.editdeadline'

    @staticmethod
    def mutate(root, args, context, info):
        args = dict(args)
        context, request, action, args = get_execution_data(
            EditDeadline.action_id, args)
        if action:
            date = dateutil.parser.parse(args['date'])
            action.execute(context, request, {'deadline': date})
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return EditDeadline(root=context)
