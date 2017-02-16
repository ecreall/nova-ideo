# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the
Challenge management process definition.
"""
import datetime
import pytz
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound

from dace.util import (
    getSite)
from dace.objectofcollaboration.principal.util import (
    has_role,
    has_any_roles,
    grant_roles,
    get_current,
    revoke_roles)
from dace.processinstance.activity import InfiniteCardinality, ActionType
from dace.processinstance.core import ActivityExecuted

from novaideo.content.interface import (
    INovaIdeoApplication, IChallenge)
from ..user_management.behaviors import (
    global_user_processsecurity,
    access_user_processsecurity)
from novaideo import _, nothing
from novaideo.content.challenge import Challenge
from ..comment_management import VALIDATOR_BY_CONTEXT
from novaideo.core import access_action, serialize_roles
from novaideo.utilities.util import connect
from novaideo.event import (
    ObjectPublished, CorrelableRemoved)
from novaideo.utilities.alerts_utility import (
    alert, get_user_data, get_entity_data, alert_comment_nia)
from novaideo.content.alert import InternalAlertKind
from novaideo.content.question import Answer
from novaideo.content.correlation import CorrelationType
from novaideo.content.comment import Comment
from novaideo.content.processes.idea_management.behaviors import (
    PresentIdea,
    CommentIdea,
    Associate as AssociateIdea)


def createchallenge_roles_validation(process, context):
    return has_role(role=('Member',))


def createchallenge_processsecurity_validation(process, context):
    return global_user_processsecurity()


class CreateChallenge(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'lateral-action'
    style_picto = 'ion-trophy'
    style_order = 1
    title = _('Create a challenge')
    unavailable_link = 'docanonymous'
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = createchallenge_roles_validation
    processsecurity_validation = createchallenge_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current(request)
        challenge = appstruct['_object_data']
        root.merge_keywords(challenge.keywords)
        root.addtoproperty('challenges', challenge)
        challenge.state.append('private')
        grant_roles(user=user, roles=(('Owner', challenge), ))
        if challenge.is_restricted:
            invited_users = challenge.invited_users
            invited_users.append(user)
            for invited in invited_users:
                grant_roles(
                    user=invited, roles=(('ChallengeParticipant', challenge), ))

        challenge.setproperty('author', user)
        challenge.subscribe_to_channel(user)
        # if isinstance(context, (Comment, Answer)):
        #     content = context.subject
        #     correlations = connect(
        #         content,
        #         [challenge],
        #         {'comment': context.comment,
        #          'type': getattr(context, 'intention',
        #                          'Transformation from another content')},
        #         user,
        #         ['transformation'],
        #         CorrelationType.solid)
        #     for correlation in correlations:
        #         correlation.setproperty('context', context)

        #     context_type = context.__class__.__name__.lower()
        #     # Add Nia comment
        #     alert_comment_nia(
        #         challenge, request, root,
        #         internal_kind=InternalAlertKind.content_alert,
        #         subject_type='challenge',
        #         alert_kind='transformation_'+context_type,
        #         content=context
        #         )

        challenge.format(request)
        challenge.reindex()
        request.registry.notify(ActivityExecuted(self, [challenge], user))
        return {'newcontext': challenge}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


class CrateAndPublish(InfiniteCardinality):
    style_picto = 'ion-trophy'
    style_order = 1
    title = _('Create and publish')
    context = INovaIdeoApplication
    roles_validation = createchallenge_roles_validation
    processsecurity_validation = createchallenge_processsecurity_validation

    @property
    def submission_title(self):
        is_moderator = has_role(role=('Moderator',))
        if not is_moderator:
            return _('Save and submit')

        return _('Save and publish')

    def start(self, context, request, appstruct, **kw):
        create_actions = self.process.get_actions('creat')
        create_action = create_actions[0] if create_actions else None
        challenge = None
        if create_action:
            result = create_action.start(context, request, appstruct, **kw)
            challenge = result.get('newcontext', None)
            if challenge:
                user = get_current()
                challenge.subscribe_to_channel(user)
                is_moderator = has_role(role=('Moderator',))
                if not is_moderator:
                    submit_actions = self.process.get_actions('submit')
                    submit_action = submit_actions[0] if submit_actions else None
                    if submit_action:
                        submit_action.start(challenge, request, {})
                else:
                    publish_actions = self.process.get_actions('publish')
                    publish_action = publish_actions[0] if publish_actions else None
                    if publish_action:
                        publish_action.start(challenge, request, {})

                return {'newcontext': challenge, 'state': True}

        return {'newcontext': getSite(), 'state': False}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def submit_roles_validation(process, context):
    return has_role(role=('Owner', context))


def submit_processsecurity_validation(process, context):
    return global_user_processsecurity()


def submit_state_validation(process, context):
    return 'private' in context.state


class SubmitChallenge(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 6
    submission_title = _('Continue')
    context = IChallenge
    roles_validation = submit_roles_validation
    processsecurity_validation = submit_processsecurity_validation
    state_validation = submit_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state = PersistentList(['submitted'])
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def archive_roles_validation(process, context):
    return has_role(role=('Moderator',))


def archive_processsecurity_validation(process, context):
    return not context.target_correlations and\
        global_user_processsecurity()


def archive_state_validation(process, context):
    return 'published' in context.state or 'submitted' in context.state


class ArchiveChallenge(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-inbox'
    style_order = 4
    submission_title = _('Continue')
    context = IChallenge
    roles_validation = archive_roles_validation
    processsecurity_validation = archive_processsecurity_validation
    state_validation = archive_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        explanation = appstruct['explanation']
        context.state = PersistentList(['archived'])
        context.reindex()
        user = context.author
        alert('internal', [root], [user],
              internal_kind=InternalAlertKind.moderation_alert,
              subjects=[context], alert_kind='moderation')
        if getattr(user, 'email', ''):
            mail_template = root.get_mail_template('archive_challenge_decision')
            subject = mail_template['subject'].format(
                subject_title=context.title)
            email_data = get_user_data(user, 'recipient', request)
            email_data.update(get_entity_data(context, 'subject', request))
            message = mail_template['template'].format(
                explanation=explanation,
                novaideo_title=root.title,
                **email_data
            )
            alert('email', [root.get_site_sender()], [user.email],
                  subject=subject, body=message)

        return {}

    def redirect(self, context, request, **kw):
        return nothing


def publish_roles_validation(process, context):
    return has_role(role=('Moderator',))


def publish_processsecurity_validation(process, context):
    return global_user_processsecurity()


def publish_state_validation(process, context):
    return 'submitted' in context.state


class PublishChallenge(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 5
    submission_title = _('Continue')
    context = IChallenge
    roles_validation = publish_roles_validation
    processsecurity_validation = publish_processsecurity_validation
    state_validation = publish_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        context.state = PersistentList(['published', 'pending'])
        context.init_published_at()
        context.reindex()
        user = get_current(request)
        author = context.author
        alert('internal', [root], [author],
              internal_kind=InternalAlertKind.moderation_alert,
              subjects=[context], alert_kind='moderation')
        # transformed_from = context.transformed_from
        # if transformed_from:
        #     context_type = transformed_from.__class__.__name__.lower()
        #     # Add Nia comment
        #     alert_comment_nia(
        #         transformed_from, request, root,
        #         internal_kind=InternalAlertKind.content_alert,
        #         subject_type=context_type,
        #         alert_kind='transformation_challenge',
        #         idea=context
        #         )

        if user is not author and getattr(author, 'email', ''):
            mail_template = root.get_mail_template('publish_challenge_decision')
            subject = mail_template['subject'].format(
                subject_title=context.title)
            email_data = get_user_data(author, 'recipient', request)
            email_data.update(get_entity_data(context, 'subject', request))
            message = mail_template['template'].format(
                novaideo_title=root.title,
                **email_data
            )
            alert('email', [root.get_site_sender()], [author.email],
                  subject=subject, body=message)

        request.registry.notify(ObjectPublished(object=context))
        request.registry.notify(ActivityExecuted(
            self, [context], user))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def del_roles_validation(process, context):
    return has_role(role=('Owner', context))


def del_processsecurity_validation(process, context):
    return global_user_processsecurity()


def del_state_validation(process, context):
    return 'archived' in context.state or \
        'private' in context.state


class DelChallenge(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_order = 6
    submission_title = _('Continue')
    context = IChallenge
    roles_validation = del_roles_validation
    processsecurity_validation = del_processsecurity_validation
    state_validation = del_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        request.registry.notify(CorrelableRemoved(object=context))
        root.delfromproperty('challenges', context)
        return {}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def edit_roles_validation(process, context):
    return has_role(role=('Owner', context))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity()


def edit_state_validation(process, context):
    return "private" in context.state


class EditChallenge(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    submission_title = _('Save')
    context = IChallenge
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        if 'attached_files' in appstruct:
            files = [f['_object_data'] for f in appstruct.pop('attached_files')]
            appstruct['attached_files'] = files

        if 'image' in appstruct:
            appstruct['image'] = appstruct.pop('image')['_object_data']

        context.set_data(appstruct)
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.format(request)
        context.reindex()
        request.registry.notify(
            ActivityExecuted(self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def comm_roles_validation(process, context):
    is_restricted = getattr(context, 'is_restricted', False)
    return (is_restricted and has_role(
            role=('ChallengeParticipant', context))) or \
        has_role(role=('Member',))


def comm_processsecurity_validation(process, context):
    return global_user_processsecurity()


def comm_state_validation(process, context):
    return 'published' in context.state


class CommentChallenge(CommentIdea):
    context = IChallenge
    roles_validation = comm_roles_validation
    processsecurity_validation = comm_processsecurity_validation
    state_validation = comm_state_validation
    style_order = 1


def comma_roles_validation(process, context):
    return has_role(role=('Anonymous',), ignore_superiors=True)


def comma_processsecurity_validation(process, context):
    return True


class CommentChallengeAnonymous(CommentChallenge):
    roles_validation = comma_roles_validation
    processsecurity_validation = comma_processsecurity_validation
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'

    def start(self, context, request, appstruct, **kw):
        return {}


def present_roles_validation(process, context):
    return has_role(role=('Member',))


def present_processsecurity_validation(process, context):
    is_restricted = getattr(context, 'is_restricted', False)
    return not is_restricted and global_user_processsecurity()


def present_state_validation(process, context):
    return 'published' in context.state


class PresentChallenge(PresentIdea):
    context = IChallenge
    roles_validation = present_roles_validation
    processsecurity_validation = present_processsecurity_validation
    state_validation = present_state_validation
    style_order = 2


def presenta_roles_validation(process, context):
    return has_role(role=('Anonymous',), ignore_superiors=True)


def presenta_processsecurity_validation(process, context):
    return not getattr(context, 'is_restricted', False)


class PresentChallengeAnonymous(PresentChallenge):
    roles_validation = presenta_roles_validation
    processsecurity_validation = presenta_processsecurity_validation
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'

    def start(self, context, request, appstruct, **kw):
        return {}


def associate_processsecurity_validation(process, context):
    return (has_role(role=('Owner', context)) or
            (has_role(role=('Member',)) and 'published' in context.state)) and \
        global_user_processsecurity()


class Associate(AssociateIdea):
    context = IChallenge
    processsecurity_validation = associate_processsecurity_validation


def get_access_key(obj):
    if 'published' in obj.state:
        is_restricted = getattr(obj, 'is_restricted', False)
        if is_restricted:
            return serialize_roles(
                (('ChallengeParticipant', obj),
                 'SiteAdmin', 'Admin', 'Moderator'))

        return ['always']
    else:
        return serialize_roles(
            (('Owner', obj), 'SiteAdmin', 'Admin', 'Moderator'))


def seechallenge_processsecurity_validation(process, context):
    is_restricted = getattr(context, 'is_restricted', False)
    can_access = True
    if is_restricted:
        can_access = has_role(role=('ChallengeParticipant', context))

    return can_access and access_user_processsecurity(process, context) and \
        ('published' in context.state or 'censored' in context.state or
         has_any_roles(roles=(('Owner', context), 'Moderator')))


@access_action(access_key=get_access_key)
class SeeChallenge(InfiniteCardinality):
    """SeeChallenge is the behavior allowing access to context"""
    style = 'button' #TODO add style abstract class
    style_descriminator = 'access-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'sidebar'
    style_picto = 'glyphicon glyphicon-eye-open'
    title = _('Details')
    context = IChallenge
    actionType = ActionType.automatic
    processsecurity_validation = seechallenge_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class SeeChallenges(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'admin-action'
    style_picto = 'ion-trophy'
    style_order = -10
    isSequential = False
    context = INovaIdeoApplication

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def addmember_roles_validation(process, context):
    return has_role(role=('Moderator',)) or \
        (has_role(role=('Owner', context)) and
         has_role(role=('ChallengeParticipant', context)))


def addmember_processsecurity_validation(process, context):
    return getattr(context, 'is_restricted', False) and \
        global_user_processsecurity()


def addmember_state_validation(process, context):
    return "pending" in context.state


class AddMembers(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'typcn typcn-user-add'
    style_interaction = 'ajax-action'
    style_order = 2
    submission_title = _('Continue')
    context = IChallenge
    roles_validation = addmember_roles_validation
    processsecurity_validation = addmember_processsecurity_validation
    state_validation = addmember_state_validation

    def start(self, context, request, appstruct, **kw):
        members = appstruct['members']
        for member in members:
            if member not in context.invited_users:
                context.addtoproperty('invited_users', member)
                grant_roles(
                    user=member, roles=(('ChallengeParticipant', context),))

            member.reindex()

        context.reindex()
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def rmmembers_processsecurity_validation(process, context):
    return getattr(context, 'is_restricted', False) and context.invited_users and \
        global_user_processsecurity()


class RemoveMembers(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'typcn typcn-user-delete'
    style_interaction = 'ajax-action'
    style_order = 3
    submission_title = _('Continue')
    context = IChallenge
    roles_validation = addmember_roles_validation
    processsecurity_validation = rmmembers_processsecurity_validation
    state_validation = addmember_state_validation

    def start(self, context, request, appstruct, **kw):
        members = appstruct['members']
        for member in members:
            if member in context.invited_users:
                context.delfromproperty('invited_users', member)
                revoke_roles(
                    user=member,
                    roles=(('ChallengeParticipant', context), ))

            member.reindex()

        context.reindex()
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def seemember_roles_validation(process, context):
    return has_role(role=('ChallengeParticipant', context))


def seemember_processsecurity_validation(process, context):
    return getattr(context, 'is_restricted', False) and \
        global_user_processsecurity()


class SeeMembers(InfiniteCardinality):
    style_descriminator = 'listing-primary-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'slider'
    style_picto = 'ion-person-stalker'
    style_order = -1
    isSequential = False
    context = IChallenge
    roles_validation = seemember_roles_validation
    processsecurity_validation = seemember_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))

#TODO behaviors

VALIDATOR_BY_CONTEXT[Challenge] = {
    'action': CommentChallenge,
    'see': SeeChallenge,
    'access_key': get_access_key
}
