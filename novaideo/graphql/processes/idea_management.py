import graphene
import urllib

from dace.util import get_obj
from pontus.schema import select

from novaideo.content.idea import Idea as IdeaClass, IdeaSchema
from novaideo.content.comment import Comment
from ..util import (
    get_context, get_action, get_execution_data,
    get_current_request, extract_files)
from . import Upload
from novaideo import _, log


_marker = object()


class CreateIdea(graphene.Mutation):

    class Input:
        context = graphene.String()
        title = graphene.String()
        text = graphene.String()
        keywords = graphene.List(graphene.String)
        attached_files = graphene.List(Upload)
        old_files = graphene.List(graphene.String)
        anonymous = graphene.Boolean()

    status = graphene.Boolean()
    idea = graphene.Field('novaideo.graphql.schema.Idea')
    actions_ids = {
        Comment: 'commentmanagement.transformtoidea',
        'default': 'ideamanagement.creat'
    }


    @staticmethod
    def mutate(root, args, context, info):
        idea_schema = select(
            IdeaSchema(), ['title', 'text', 'keywords', 'attached_files', 'anonymous'])
        args = dict(args)
        request = get_current_request()
        old_files = []
        context_oid = args.pop('context')
        for of in args.pop('old_files'):
            try:
                old_files.append(get_obj(int(of)))
            except Exception as e:
                log.warning(e)
                continue

        old_files = [f.copy() for f in old_files]
        args['attached_files'] = extract_files('attached_files', request)
        args = idea_schema.deserialize(args)
        args['attached_files'] = [f['_object_data']
                                  for f in args['attached_files']]
        args['attached_files'].extend(old_files)
        if context_oid: args['context'] = context_oid
        default_action_id = CreateIdea.actions_ids['default']
        context = get_context(context_oid)
        context, request, action, args = get_execution_data(
            CreateIdea.actions_ids.get(context.__class__, default_action_id), args)
        new_idea = None
        if action:
            anonymous = args.pop('anonymous', False)
            new_idea = IdeaClass(**args)
            appstruct = {
                '_object_data': new_idea,
                'anonymous': anonymous
            }
            action.execute(context, request, appstruct)
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        status = new_idea is not None
        return CreateIdea(idea=new_idea, status=status)


class EditIdea(graphene.Mutation):

    class Input:
        context = graphene.String()
        title = graphene.String()
        text = graphene.String()
        keywords = graphene.List(graphene.String)
        old_files = graphene.List(graphene.String)
        attached_files = graphene.List(Upload)

    status = graphene.Boolean()
    idea = graphene.Field('novaideo.graphql.schema.Idea')
    action_id = 'ideamanagement.edit'

    @staticmethod
    def mutate(root, args, context, info):
        idea_schema = select(
            IdeaSchema(), ['title', 'text', 'keywords', 'attached_files'])
        args = dict(args)
        request = get_current_request()
        context_oid = args.pop('context')
        old_files = []
        for of in args.pop('old_files'):
            try:
                old_files.append(get_obj(int(of)))
            except Exception as e:
                log.warning(e)
                continue

        args['attached_files'] = extract_files('attached_files', request)
        args = idea_schema.deserialize(args)
        args['attached_files'].extend([{'_object_data': f} for f in old_files])
        args['context'] = context_oid
        context, request, action, args = get_execution_data(
            EditIdea.action_id, args)
        status = False
        if action:
            action.execute(context, request, args)
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return EditIdea(idea=context, status=status)


class CreateAndPublishIdea(graphene.Mutation):

    class Input:
        context = graphene.String()
        title = graphene.String()
        text = graphene.String()
        keywords = graphene.List(graphene.String)
        attached_files = graphene.List(Upload)
        old_files = graphene.List(graphene.String)
        anonymous = graphene.Boolean()
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
            IdeaSchema(), ['title', 'text', 'keywords', 'attached_files', 'anonymous'])
        args = dict(args)
        request = get_current_request()
        old_files = []
        context_oid = args.pop('context')
        for of in args.pop('old_files'):
            try:
                old_files.append(get_obj(int(of)))
            except Exception as e:
                log.warning(e)
                continue

        old_files = [f.copy() for f in old_files]
        args['attached_files'] = extract_files('attached_files', request)
        args = idea_schema.deserialize(args)
        args['attached_files'] = [f['_object_data']
                                  for f in args['attached_files']]
        args['attached_files'].extend(old_files)
        if context_oid: args['context'] = context_oid
        context, request, action, args = get_execution_data(
            CreateAndPublishIdea.action_id, args)
        new_idea = None
        if action:
            anonymous = args.pop('anonymous', False)
            new_idea = IdeaClass(**args)
            appstruct = {
                '_object_data': new_idea,
                'anonymous': anonymous
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
    user = graphene.Field('novaideo.graphql.schema.Person')
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

        return Support(user=request.user, idea=context, status=status)


class Oppose(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    user = graphene.Field('novaideo.graphql.schema.Person')
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

        return Oppose(user=request.user, idea=context, status=status)


class WithdrawToken(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    user = graphene.Field('novaideo.graphql.schema.Person')
    idea = graphene.Field('novaideo.graphql.schema.Idea')
    action_id = 'ideamanagement.withdraw_token'

    @staticmethod
    def mutate(root, args, context, info):
        context, request, action, args = get_execution_data(
            WithdrawToken.action_id, args)
        status = False
        if action:
            action.execute(context, request, {})
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return WithdrawToken(user=request.user, idea=context, status=status)


class DeleteIdea(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    action_id = 'ideamanagement.delidea'

    @staticmethod
    def mutate(root, args, context, info):
        context, request, action, args = get_execution_data(
            DeleteIdea.action_id, args)
        status = False
        if action:
            action.execute(context, request, {})
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return DeleteIdea(status=status)


class Publish(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    idea = graphene.Field('novaideo.graphql.schema.Idea')
    action_id = 'ideamanagement.publish'

    @staticmethod
    def mutate(root, args, context, info):
        context, request, action, args = get_execution_data(
            Publish.action_id, args)
        status = False
        if action:
            action.execute(context, request, {})
            request.invalidate_cache = True
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return Publish(idea=context, status=status)


class MakeItsOpinion(graphene.Mutation):

    class Input:
        context = graphene.String()
        opinion = graphene.String()
        explanation = graphene.String()

    status = graphene.Boolean()
    idea = graphene.Field('novaideo.graphql.schema.Idea')
    action_id = 'ideamanagement.makeitsopinion'

    @staticmethod
    def mutate(root, args, context, info):
        context, request, action, args = get_execution_data(
            MakeItsOpinion.action_id, args)
        status = False
        if action:
            action.execute(context, request, args)
            request.invalidate_cache = True
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return MakeItsOpinion(idea=context, status=status)


class Abandon(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    idea = graphene.Field('novaideo.graphql.schema.Idea')
    action_id = 'ideamanagement.abandon'

    @staticmethod
    def mutate(root, args, context, info):
        context, request, action, args = get_execution_data(
            Abandon.action_id, args)
        status = False
        if action:
            action.execute(context, request, {})
            request.invalidate_cache = True
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return Abandon(idea=context, status=status)


class Recuperate(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    idea = graphene.Field('novaideo.graphql.schema.Idea')
    action_id = 'ideamanagement.recuperate'

    @staticmethod
    def mutate(root, args, context, info):
        context, request, action, args = get_execution_data(
            Recuperate.action_id, args)
        status = False
        if action:
            action.execute(context, request, {})
            request.invalidate_cache = True
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return Recuperate(idea=context, status=status)


class Archive(graphene.Mutation):

    class Input:
        context = graphene.String()
        explanation = graphene.String()

    status = graphene.Boolean()
    idea = graphene.Field('novaideo.graphql.schema.Idea')
    action_id = 'ideamanagement.moderationarchive'

    @staticmethod
    def mutate(root, args, context, info):
        context, request, action, args = get_execution_data(
            Archive.action_id, args)
        status = False
        if action:
            action.execute(context, request, args)
            request.invalidate_cache = True
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return Archive(idea=context, status=status)


class Share(graphene.Mutation):

    class Input:
        context = graphene.String()
        message = graphene.String()
        subject = graphene.String()
        members = graphene.List(graphene.String)

    idea = graphene.Field('novaideo.graphql.schema.Idea')
    action_id = 'ideamanagement.present'

    @staticmethod
    def mutate(root, args, context, info):
        context, request, action, args = get_execution_data(
            Share.action_id, args)
        args['send_to_me'] = True
        args['members'] = [get_obj(int(member)) for member in args['members']]
        if action:
            action.execute(context, request, args)
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return Share(idea=context)


