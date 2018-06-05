import datetime
import pytz
import graphene
import urllib

from dace.util import get_obj
from pontus.schema import select

from novaideo.content.comment import Comment as CommentClass, CommentSchema
from ..util import (
    get_context, get_action, get_execution_data,
    get_current_request, extract_files)
from . import Upload
from novaideo import _, log
from novaideo.core import PrivateChannel


_marker = object()


class AddPrivateChannel(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    channel = graphene.Field('novaideo.graphql.schema.Channel')

    @staticmethod
    def mutate(root, args, context, info):
        data = dict(args)
        member = get_context(data.get('context'), _marker)
        user = context.user
        status = False
        channel= None
        if user and member is not _marker:
            channel = user.get_channel(member)
            if not channel:
                channel = PrivateChannel()
                user.addtoproperty('channels', channel)
                channel.addtoproperty('members', user)
                channel.addtoproperty('members', member)
                user.set_read_date(channel, datetime.datetime.now(tz=pytz.UTC))

            status = True

        return AddPrivateChannel(status=status, channel=channel)


class CommentObject(graphene.Mutation):

    class Input:
        context = graphene.String()
        action = graphene.String()
        comment = graphene.String()
        attached_files = graphene.List(Upload)
        anonymous = graphene.Boolean()
        # the Upload object type deserialization currently doesn't work,
        # it fails silently, so we actually get a list of None.
        # So if we uploaded 3 files, we get attached_files = [None, None, None]
        # We retrieve the files with the hard coded
        # variables.attachedFiles.{0,1,2} below.
        # This code will not work if batched mode is
        # implemented in graphql-wsgi and batched mode is enabled on apollo.

    status = graphene.Boolean()
    is_new_channel = graphene.Boolean() 
    comment = graphene.Field('novaideo.graphql.schema.Comment')

    @staticmethod
    def mutate(root, args, context, info):
        comment_schema = select(
            CommentSchema(), ['comment', 'files', 'anonymous'])
        args = dict(args)
        request = get_current_request()
        action_id = args.pop('action')
        context_oid = args.pop('context')
        args['files'] = extract_files('attached_files', request)
        args = comment_schema.deserialize(args)
        args['files'] = [f['_object_data']
                                  for f in args['files']]
        args['context'] = context_oid
        args['intention'] = 'Remark' # TODO the intention must be submitted by the user
        context, request, action, args = get_execution_data(
            action_id, args)
        new_comment = None
        is_new_channel = False
        if action:
            channel = context.get_channel(request.user)
            is_new_channel = request.user not in channel.members
            anonymous = args.get('anonymous', False)
            new_comment = CommentClass(**args)
            appstruct = {
                '_object_data': new_comment,
                'anonymous': anonymous,
            }
            action.execute(context, request, appstruct)
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        status = new_comment is not None
        return CommentObject(comment=new_comment, is_new_channel=is_new_channel, status=status)


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


class DeleteComment(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    action_id = 'commentmanagement.remove'

    @staticmethod
    def mutate(root, args, context, info):
        args = dict(args)
        context, request, action, args = get_execution_data(
            DeleteComment.action_id, args)
        status = False
        if action:
            action.execute(context, request, {})
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return DeleteComment(status=status)


class Pin(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    context = graphene.Field('novaideo.graphql.schema.Comment')
    action_id = 'commentmanagement.pin'

    @staticmethod
    def mutate(root, args, context, info):
        args = dict(args)
        context, request, action, args = get_execution_data(
            Pin.action_id, args)
        status = False
        if action:
            action.execute(context, request, {})
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return Pin(context=context, status=status)


class Unpin(graphene.Mutation):

    class Input:
        context = graphene.String()

    status = graphene.Boolean()
    context = graphene.Field('novaideo.graphql.schema.Comment')
    action_id = 'commentmanagement.unpin'

    @staticmethod
    def mutate(root, args, context, info):
        args = dict(args)
        context, request, action, args = get_execution_data(
            Unpin.action_id, args)
        status = False
        if action:
            action.execute(context, request, {})
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return Unpin(context=context, status=status)




class Edit(graphene.Mutation):

    class Input:
        context = graphene.String()
        comment = graphene.String()
        old_files = graphene.List(graphene.String)
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
    action_id = 'commentmanagement.edit'

    @staticmethod
    def mutate(root, args, context, info):
        comment_schema = select(
            CommentSchema(), ['comment', 'files'])
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

        args['files'] = extract_files('attached_files', request)
        args = comment_schema.deserialize(args)
        args['files'] = [f['_object_data']
                                  for f in args['files']]
        args['files'].extend(old_files)
        args['context'] = context_oid
        context, request, action, args = get_execution_data(
            Edit.action_id, args)
        if action:
            context.comment = args['comment']
            context.setproperty('files', args['files'])
            action.execute(context, request, {})
            status = True
        else:
            raise Exception(
                request.localizer.translate(_("Authorization failed")))

        return Edit(comment=context, status=status)
