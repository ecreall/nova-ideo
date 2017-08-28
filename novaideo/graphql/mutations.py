import datetime
import pytz
import graphene
import urllib

from pontus.schema import select

from novaideo.content.idea import Idea as IdeaClass, IdeaSchema
from novaideo.content.comment import Comment as CommentClass, CommentSchema
from .util import get_context, get_action, get_execution_data
from novaideo import _

_marker = object()


class Upload(graphene.InputObjectType):
    name = graphene.String()
    type = graphene.String()
    uri = graphene.String()


class CreateIdea(graphene.Mutation):

    class Input:
        title = graphene.String()
        text = graphene.String()
        keywords = graphene.List(graphene.String)
        attached_files = graphene.List(Upload)

    status = graphene.Boolean()
    idea = graphene.Field('novaideo.graphql.schema.Idea')
    action_id = 'ideamanagement.creat'

    @staticmethod
    def mutate(root, args, context, info):
        idea_schema = select(
            IdeaSchema(), ['title', 'text', 'keywords', 'attached_files'])
        args = dict(args)
        attached_files = args.pop('attached_files', None)
        uploaded_files = []
        if attached_files:
            for index, file_ in enumerate(attached_files):
                file_storage = context.POST.get(
                    'variables.attachedFiles.'+str(index))
                fp = file_storage.file
                fp.seek(0)
                uploaded_files.append({
                    'fp': fp,
                    'filename': urllib.parse.unquote(file_storage.filename)})

        args['attached_files'] = uploaded_files
        args = idea_schema.deserialize(args)
        args['attached_files'] = [f['_object_data']
                                  for f in args['attached_files']]
        context, request, action, args = get_execution_data(
            CreateIdea.action_id, args)
        new_idea = None
        if action:
            new_idea = IdeaClass(**args)
            appstruct = {
                '_object_data': new_idea
            }
            action.execute(context, request, appstruct)
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        status = new_idea is not None
        return CreateIdea(idea=new_idea, status=status)


class CreateAndPublishIdea(graphene.Mutation):

    class Input:
        title = graphene.String()
        text = graphene.String()
        keywords = graphene.List(graphene.String)
        attached_files = graphene.List(Upload)
        # the Upload object type deserialization currently doesn't work,
        # it fails silently, so we actually get a list of None.
        # So if we uploaded 3 files, we get attached_files = [None, None, None]
        # We retrieve the files with the hard coded
        # variables.attachedFiles.{0,1,2} below.
        # This code will not work if batched mode is
        # implemented in graphql-wsgi and batched mode is enabled on apollo.

    status = graphene.Boolean()
    idea = graphene.Field('novaideo.graphql.schema.Idea')
    action_id = 'ideamanagement.creatandpublish'

    @staticmethod
    def mutate(root, args, context, info):
        idea_schema = select(
            IdeaSchema(), ['title', 'text', 'keywords', 'attached_files'])
        args = dict(args)
        attached_files = args.pop('attached_files', None)
        uploaded_files = []
        if attached_files:
            for index, file_ in enumerate(attached_files):
                file_storage = context.POST.get(
                    'variables.attachedFiles.'+str(index))
                fp = file_storage.file
                fp.seek(0)
                uploaded_files.append({
                    'fp': fp,
                    'filename': urllib.parse.unquote(file_storage.filename)})

        args['attached_files'] = uploaded_files
        args = idea_schema.deserialize(args)
        args['attached_files'] = [f['_object_data']
                                  for f in args['attached_files']]
        context, request, action, args = get_execution_data(
            CreateAndPublishIdea.action_id, args)
        new_idea = None
        if action:
            new_idea = IdeaClass(**args)
            appstruct = {
                '_object_data': new_idea
            }
            action.execute(context, request, appstruct)
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        status = new_idea is not None
        return CreateAndPublishIdea(idea=new_idea, status=status)


class Support(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    idea = graphene.Field('novaideo.graphql.schema.Idea')
    action_id = 'ideamanagement.support'
    withdraw_action_id = 'ideamanagement.withdraw_token'

    @staticmethod
    def mutate(root, args, context, info):
        data = dict(args)
        context, request, w_action, args = get_execution_data(
            Support.withdraw_action_id, data)
        if w_action:
            w_action.execute(context, request, {})

        context, request, action, args = get_execution_data(
            Support.action_id, data)
        status = False
        if action:
            action.execute(context, request, {})
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return Support(idea=context, status=status)


class Oppose(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    idea = graphene.Field('novaideo.graphql.schema.Idea')
    action_id = 'ideamanagement.oppose'
    withdraw_action_id = 'ideamanagement.withdraw_token'

    @staticmethod
    def mutate(root, args, context, info):
        data = dict(args)
        context, request, w_action, args = get_execution_data(
            Oppose.withdraw_action_id, data)
        if w_action:
            w_action.execute(context, request, {})

        context, request, action, args = get_execution_data(
            Oppose.action_id, data)
        status = False
        if action:
            action.execute(context, request, {})
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return Oppose(idea=context, status=status)


class WithdrawToken(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    idea = graphene.Field('novaideo.graphql.schema.Idea')
    action_id = 'ideamanagement.withdraw_token'

    @staticmethod
    def mutate(root, args, context, info):
        args = dict(args)
        context, request, action, args = get_execution_data(
            WithdrawToken.action_id, args)
        status = False
        if action:
            action.execute(context, request, {})
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return WithdrawToken(idea=context, status=status)


class CommentObject(graphene.Mutation):

    class Input:
        context = graphene.String()
        action = graphene.String()
        comment = graphene.String()
        attached_files = graphene.List(Upload)
        # the Upload object type deserialization currently doesn't work,
        # it fails silently, so we actually get a list of None.
        # So if we uploaded 3 files, we get attached_files = [None, None, None]
        # We retrieve the files with the hard coded
        # variables.attachedFiles.{0,1,2} below.
        # This code will not work if batched mode is
        # implemented in graphql-wsgi and batched mode is enabled on apollo.

    status = graphene.Boolean()
    comment = graphene.Field('novaideo.graphql.schema.Comment')

    @staticmethod
    def mutate(root, args, context, info):
        comment_schema = select(
            CommentSchema(), ['comment', 'files'])
        args = dict(args)
        action_id = args.pop('action')
        context_oid = args.pop('context')
        attached_files = args.pop('attached_files', None)
        uploaded_files = []
        if attached_files:
            for index, file_ in enumerate(attached_files):
                file_storage = context.POST.get(
                    'variables.attachedFiles.'+str(index))
                fp = file_storage.file
                fp.seek(0)
                uploaded_files.append({
                    'fp': fp,
                    'filename': urllib.parse.unquote(file_storage.filename)})

        args['files'] = uploaded_files
        args = comment_schema.deserialize(args)
        args['files'] = [f['_object_data']
                                  for f in args['files']]
        args['context'] = context_oid
        args['intention'] = 'Remark' # TODO the intention must be submitted by the user
        context, request, action, args = get_execution_data(
            action_id, args)
        new_comment = None
        if action:
            new_comment = CommentClass(**args)
            appstruct = {
                '_object_data': new_comment
            }
            action.execute(context, request, appstruct)
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        status = new_comment is not None
        return CommentObject(comment=new_comment, status=status)


class MarkCommentsAsRead(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()

    @staticmethod
    def mutate(root, args, context, info):
        data = dict(args)
        channel = get_context(data.get('context'), _marker)
        status = False
        if context.user and channel is not _marker:
            now = datetime.datetime.now(tz=pytz.UTC)
            context.user.set_read_date(channel, now)
            status = True

        return MarkCommentsAsRead(status=status)


class Select(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    idea = graphene.Field('novaideo.graphql.schema.Idea')
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

        return Select(idea=context, status=status)


class Deselect(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    idea = graphene.Field('novaideo.graphql.schema.Idea')
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

        return Deselect(idea=context, status=status)


class Mutations(graphene.ObjectType):
    create_idea = CreateIdea.Field()
    create_and_publish = CreateAndPublishIdea.Field()
    support_idea = Support.Field()
    oppose_idea = Oppose.Field()
    select = Select.Field()
    deselect = Deselect.Field()
    withdraw_token_idea = WithdrawToken.Field()
    comment_object = CommentObject.Field()
    mark_comments_as_read = MarkCommentsAsRead.Field()