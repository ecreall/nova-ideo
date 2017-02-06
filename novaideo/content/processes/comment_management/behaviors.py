# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the
Comment management process definition.
"""
import datetime
import pytz
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    get_current,
    grant_roles,
    has_role,
    has_any_roles)
from dace.processinstance.activity import (
    InfiniteCardinality, ActionType)

from novaideo.content.processes import global_user_processsecurity
from novaideo.content.interface import IComment
from novaideo import _, nothing
from novaideo.utilities.util import disconnect
from novaideo.utilities.alerts_utility import (
    alert, get_user_data, get_entity_data)
from novaideo.content.alert import InternalAlertKind
from novaideo.content.processes.idea_management.behaviors import CreateIdea
from novaideo.content.processes.question_management.behaviors import AskQuestion
from . import VALIDATOR_BY_CONTEXT
from novaideo.core import access_action, serialize_roles


def respond_relation_validation(process, context):
    subject = context.channel.get_subject(get_current())
    comment_action = VALIDATOR_BY_CONTEXT.get(
        subject.__class__, {}).get('action', None)
    relation_validation = getattr(comment_action, 'relation_validation', None)
    if relation_validation and relation_validation is not NotImplemented:
        return relation_validation(process, subject)

    return True


def respond_roles_validation(process, context):
    subject = context.channel.get_subject(get_current())
    comment_action = VALIDATOR_BY_CONTEXT.get(
        subject.__class__, {}).get('action', None)
    roles_validation = getattr(comment_action, 'roles_validation', None)
    if roles_validation and roles_validation is not NotImplemented:
        return roles_validation(process, subject)

    return True


def respond_processsecurity_validation(process, context):
    subject = context.channel.get_subject(get_current())
    comment_action = VALIDATOR_BY_CONTEXT.get(
        subject.__class__, {}).get('action', None)
    processsecurity_validation = getattr(
        comment_action, 'processsecurity_validation', None)
    if processsecurity_validation and \
       processsecurity_validation is not NotImplemented:
        return processsecurity_validation(process, subject)

    return True


def respond_state_validation(process, context):
    if 'published' not in context.state:
        return False

    subject = context.channel.get_subject(get_current())
    comment_action = VALIDATOR_BY_CONTEXT.get(
        subject.__class__, {}).get('action', None)
    state_validation_ = getattr(
        comment_action, 'state_validation', None)
    if state_validation_ and state_validation_ is not NotImplemented:
        return state_validation_(process, subject)

    return True


class Respond(InfiniteCardinality):
    style_picto = 'ion-chatbubbles'
    style_descriminator = 'primary-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'comment-replay'
    style_action_class = 'comment-inline-toggle'
    style_interaction_contextual = True
    style_order = 0
    title = _('Reply')
    access_controled = True
    context = IComment
    relation_validation = respond_relation_validation
    roles_validation = respond_roles_validation
    processsecurity_validation = respond_processsecurity_validation
    state_validation = respond_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        comment = appstruct['_object_data']
        context.addtoproperty('comments', comment)
        comment.format(request)
        user = get_current()
        comment.setproperty('author', user)
        comment.state = PersistentList(['published'])
        grant_roles(user=user, roles=(('Owner', comment), ))
        content = comment.subject
        channel = comment.channel
        is_discuss = channel.is_discuss()
        channel.add_comment(comment)
        comment.reindex()
        if not is_discuss and content and content is not root:
            content.subscribe_to_channel(user)

        if appstruct.get('associated_contents', []):
            comment.set_associated_contents(
                appstruct['associated_contents'], user)

        author = getattr(content, 'author', None)
        authors = getattr(content, 'authors', [author] if author else [])
        comment_author = getattr(context, 'author', None)

        if user in authors:
            authors.remove(user)

        if comment_author in authors:
            authors.remove(comment_author)

        comment_kind = 'general_discuss' if not channel.get_subject(user) \
            else 'discuss' if is_discuss else 'comment'
        author_data = get_user_data(user, 'author', request)
        alert_data = get_entity_data(comment, 'comment', request)
        alert_data.update(author_data)
        alert('internal', [root], authors,
              internal_kind=InternalAlertKind.comment_alert,
              subjects=[channel],
              comment_kind=comment_kind,
              **alert_data)
        subject_data = get_entity_data(content, 'subject', request)
        alert_data.update(subject_data)
        mail_template = root.get_mail_template(
            'alert_discuss' if is_discuss else 'alert_comment')
        subject = mail_template['subject'].format(
            **subject_data)
        for user_to_alert in [u for u in authors if getattr(u, 'email', '')]:
            email_data = get_user_data(user_to_alert, 'recipient', request)
            email_data.update(alert_data)
            message = mail_template['template'].format(
                novaideo_title=root.title,
                **email_data
            )
            alert('email', [root.get_site_sender()], [user_to_alert.email],
                  subject=subject, body=message)

        if comment_author is not user:
            alert('internal', [root], [comment_author],
                  internal_kind=InternalAlertKind.comment_alert,
                  subjects=[channel], is_respons=True,
                  comment_kind=comment_kind,
                  **alert_data
                  )
            if getattr(comment_author, 'email', ''):
                email_data = get_user_data(comment_author, 'recipient', request)
                email_data.update(alert_data)
                mail_template = root.get_mail_template(
                    'alert_discuss' if is_discuss else 'alert_respons')
                subject = mail_template['subject'].format(
                    **subject_data)
                message = mail_template['template'].format(
                    novaideo_title=root.title,
                    **email_data
                )
                alert('email', [root.get_site_sender()], [comment_author.email],
                      subject=subject, body=message)

        user.set_read_date(channel, datetime.datetime.now(tz=pytz.UTC))
        return {'newcontext': comment.subject}

    def redirect(self, context, request, **kw):
        return nothing


def state_validation(process, context):
    return 'published' in context.state


def edit_roles_validation(process, context):
    return has_role(role=('Owner', context))


class Edit(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_interaction = 'ajax-action'
    style_interaction_type = 'comment-replay'
    style_action_class = 'comment-edit-action comment-inline-toggle'
    style_interaction_contextual = True
    style_order = 2
    submission_title = _('Continue')
    context = IComment
    roles_validation = edit_roles_validation
    state_validation = state_validation

    def start(self, context, request, appstruct, **kw):
        context.edited = True
        user = get_current()
        if appstruct.get('associated_contents', []):
            context.set_associated_contents(
                appstruct['associated_contents'], user)

        context.format(request)
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def rm_processsecurity_validation(process, context):
    return not context.comments and\
        global_user_processsecurity()


class Remove(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_action_class = 'comment-ajax-action comment-remove-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_order = 5
    submission_title = _('Continue')
    context = IComment
    roles_validation = edit_roles_validation
    processsecurity_validation = rm_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        content = context.subject
        current_correlation = context.related_correlation
        if current_correlation:
            targets = getattr(current_correlation, 'targets', [])
            disconnect(content, targets)

        context.channel.remove_comment(context)
        context.__parent__.delfromproperty('comments', context)
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def pin_processsecurity_validation(process, context):
    return not getattr(context, 'pinned',  False) and\
        global_user_processsecurity()


class Pin(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_action_class = 'comment-ajax-action comment-un-pin-action'
    style_picto = 'typcn typcn-pin'
    style_order = 1
    submission_title = _('Continue')
    context = IComment
    roles_validation = pin_processsecurity_validation
    state_validation = state_validation

    def start(self, context, request, appstruct, **kw):
        context.pinned = True
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def unpin_processsecurity_validation(process, context):
    return getattr(context, 'pinned',  False) and\
        global_user_processsecurity()


class Unpin(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_action_class = 'comment-ajax-action comment-un-pin-action'
    style_picto = 'typcn typcn-pin-outline'
    style_order = 2
    submission_title = _('Continue')
    context = IComment
    roles_validation = unpin_processsecurity_validation
    state_validation = state_validation

    def start(self, context, request, appstruct, **kw):
        context.pinned = False
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


class TransformToIdea(CreateIdea):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'icon novaideo-icon icon-idea'
    style_order = 3
    title = _('Transform into an idea')
    context = IComment
    state_validation = state_validation


class TransformToQuestion(AskQuestion):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'icon md md-live-help'
    style_order = 4
    title = _('Transform into a question')
    context = IComment
    state_validation = state_validation


def get_access_key(obj):
    if 'published' in obj.state:
        subject = obj.subject
        access_key = VALIDATOR_BY_CONTEXT.get(
            subject.__class__, {}).get('access_key', None)
        return access_key(subject) if access_key else ['always']
    else:
        return serialize_roles(
            (('Owner', obj), 'SiteAdmin', 'Admin', 'Moderator'))


def seecomment_processsecurity_validation(process, context):
    if 'published' in context.state:
        subject = context.subject
        see_action = VALIDATOR_BY_CONTEXT.get(
            subject.__class__, {}).get('see', None)
        return see_action.processsecurity_validation(
            process, subject) if see_action else True
    else:
        return has_any_roles(
            roles=(('Owner', context), 'Moderator'))


@access_action(access_key=get_access_key)
class SeeComment(InfiniteCardinality):
    """SeeComment is the behavior allowing access to context"""
    context = IComment
    processsecurity_validation = seecomment_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors
