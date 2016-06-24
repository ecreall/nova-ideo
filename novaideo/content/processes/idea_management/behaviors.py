# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the
Idea management process definition.
"""
import datetime
import pytz
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_request

from substanced.util import get_oid

from dace.util import (
    getSite,
    getBusinessAction,
    copy)
from dace.objectofcollaboration.principal.util import (
    has_role,
    has_any_roles,
    grant_roles,
    get_current)
from dace.processinstance.activity import InfiniteCardinality, ActionType
from dace.processinstance.core import ActivityExecuted

import html_diff_wrapper

from novaideo.content.interface import INovaIdeoApplication, Iidea
from ..user_management.behaviors import (
    global_user_processsecurity,
    access_user_processsecurity)
from novaideo import _
from novaideo.content.idea import Idea
from ..comment_management.behaviors import VALIDATOR_BY_CONTEXT
from novaideo.core import access_action, serialize_roles
from novaideo.utilities.util import connect
from novaideo.event import (
    ObjectPublished, CorrelableRemoved,
    ObjectModified)
from novaideo.utilities.alerts_utility import alert
from novaideo.content.alert import InternalAlertKind
from novaideo.views.filter import get_users_by_preferences
from novaideo.content.proposal import Proposal
from novaideo.content.working_group import WorkingGroup
from novaideo.content.correlation import CorrelationType
from novaideo.content.processes.proposal_management import (
    init_proposal_ballots, add_attached_files)


try:
    basestring
except NameError:
    basestring = str


def createidea_roles_validation(process, context):
    return has_role(role=('Member',))


def createidea_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class CreateIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'lateral-action'
    style_interaction = 'modal-action'
    style_picto = 'icon novaideo-icon icon-idea'
    style_order = 0
    title = _('Create an idea')
    unavailable_link = 'docanonymous'
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = createidea_roles_validation
    processsecurity_validation = createidea_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        idea = appstruct['_object_data']
        root.merge_keywords(idea.keywords)
        root.addtoproperty('ideas', idea)
        idea.state.append('to work')
        grant_roles(user=user, roles=(('Owner', idea), ))
        idea.setproperty('author', user)
        idea.reindex()
        request.registry.notify(ActivityExecuted(self, [idea], user))
        return {'newcontext': idea}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


class CrateAndPublish(InfiniteCardinality):
    style_picto = 'icon novaideo-icon icon-idea'
    style_order = 1
    title = _('Create and publish')
    # submission_title = _('Save and publish')
    context = INovaIdeoApplication
    roles_validation = createidea_roles_validation
    processsecurity_validation = createidea_processsecurity_validation

    @property
    def submission_title(self):
        request = get_current_request()
        if getattr(request, 'moderate_ideas', False):
            return _('Save and submit')

        return _('Save and publish')

    def start(self, context, request, appstruct, **kw):
        create_actions = self.process.get_actions('creat')
        create_action = create_actions[0] if create_actions else None
        idea = None
        if create_action:
            result = create_action.start(context, request, appstruct, **kw)
            idea = result.get('newcontext', None)
            if request.moderate_ideas:
                submit_actions = self.process.get_actions('submit')
                submit_action = submit_actions[0] if submit_actions else None
                if submit_action:
                    submit_action.start(idea, request, {})
            else:
                publish_actions = self.process.get_actions('publish')
                publish_action = publish_actions[0] if publish_actions else None
                if publish_action:
                    publish_action.start(idea, request, {})

            return {'newcontext': idea, 'state': True}

        return {'newcontext': getSite(), 'state': False}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


class CrateAndPublishAsProposal(CrateAndPublish):
    style_picto = 'icon novaideo-icon icon-idea'
    style_order = 2
    title = _('Create a working group')
    submission_title = _('Create a working group')

    def start(self, context, request, appstruct, **kw):
        result = super(CrateAndPublishAsProposal, self).start(context, request, appstruct, **kw)
        root = getSite()
        state = result.get('state', False)
        if state:
            idea = result.get('newcontext', None)
            if idea:
                user = get_current()
                related_ideas = [idea]
                localizer = request.localizer
                title = idea.title + \
                    localizer.translate(_(" (the proposal)"))
                proposal = Proposal(
                    title=title,
                    description=idea.text[:600],
                    text='<p>'+idea.text.replace('\n', '<br/>')+'</p>',
                    keywords=list(idea.keywords)
                    )
                proposal.text = html_diff_wrapper.normalize_text(proposal.text)
                root.addtoproperty('proposals', proposal)
                proposal.state.append('draft')
                grant_roles(user=user, roles=(('Owner', proposal), ))
                grant_roles(user=user, roles=(('Participant', proposal), ))
                proposal.setproperty('author', user)
                wg = WorkingGroup()
                root.addtoproperty('working_groups', wg)
                wg.init_workspace()
                wg.setproperty('proposal', proposal)
                wg.addtoproperty('members', user)
                wg.state.append('deactivated')
                if related_ideas:
                    connect(proposal,
                            related_ideas,
                            {'comment': _('Add related ideas'),
                             'type': _('Creation')},
                            user,
                            ['related_proposals', 'related_ideas'],
                            CorrelationType.solid)
                try:
                    files = {
                        'add_files': {
                            'attached_files': [{'_object_data': f.copy()} for
                                               f in idea.attached_files]
                        }
                    }
                    add_attached_files(files, proposal)
                except Exception:
                    pass

                proposal.reindex()
                init_proposal_ballots(proposal)
                wg.reindex()
                request.registry.notify(
                    ActivityExecuted(self, [idea, proposal, wg], user))
                return {'newcontext': proposal}

        return {'newcontext': root}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def duplicate_processsecurity_validation(process, context):
    return ((has_role(role=('Owner', context)) and \
            'archived' not in context.state or \
            'version' in context.state) or \
            'published' in context.state) and \
        global_user_processsecurity(process, context)


class DuplicateIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-resize-full'
    style_order = 2
    submission_title = _('Save')
    context = Iidea
    processsecurity_validation = duplicate_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        copy_of_idea = copy(
            context, (root, 'ideas'),
            omit=('created_at', 'modified_at',
                  'opinion', 'examined_at', 'published_at'))
        copy_of_idea.opinion = {}
        root.merge_keywords(appstruct['keywords'])
        files = [f['_object_data'] for f in appstruct.pop('attached_files')]
        appstruct['attached_files'] = files
        copy_of_idea.setproperty('originalentity', context)
        copy_of_idea.state = PersistentList(['to work'])
        copy_of_idea.setproperty('author', user)
        grant_roles(user=user, roles=(('Owner', copy_of_idea), ))
        copy_of_idea.set_data(appstruct)
        copy_of_idea.modified_at = datetime.datetime.now(tz=pytz.UTC)
        copy_of_idea.reindex()
        context.reindex()
        request.registry.notify(ActivityExecuted(
            self, [context, copy_of_idea], user))
        return {'newcontext': copy_of_idea}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def del_roles_validation(process, context):
    return has_role(role=('Owner', context))


def del_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def del_state_validation(process, context):
    return 'archived' in context.state and \
        'version' not in context.state


class DelIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_order = 6
    submission_title = _('Continue')
    context = Iidea
    roles_validation = del_roles_validation
    processsecurity_validation = del_processsecurity_validation
    state_validation = del_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        request.registry.notify(CorrelableRemoved(object=context))
        root.delfromproperty('ideas', context)
        return {}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def edit_roles_validation(process, context):
    return has_role(role=('Owner', context))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def edit_state_validation(process, context):
    return "to work" in context.state


class EditIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    submission_title = _('Save')
    context = Iidea
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        last_version = context.version
        copy_of_idea = copy(
            context,
            (context, 'version'),
            new_name=context.__name__,
            select=('modified_at',),
            omit=('created_at',),
            roles=True)
        copy_of_idea.keywords = context.keywords
        copy_of_idea.setproperty('version', last_version)
        copy_of_idea.setproperty('originalentity', context.originalentity)
        if last_version is not None:
            grant_roles(user=user, roles=(('Owner', last_version), ))

        files = [f['_object_data'] for f in appstruct.pop('attached_files')]
        appstruct['attached_files'] = files
        root.merge_keywords(appstruct['keywords'])
        copy_of_idea.state = PersistentList(['version', 'archived'])
        copy_of_idea.setproperty('author', user)
        note = appstruct.pop('note', '')
        context.note = note
        context.set_data(appstruct)
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        copy_of_idea.reindex()
        context.reindex()
        if 'archived' in context.state:
            recuperate_actions = getBusinessAction(context,
                                                   request,
                                                   'ideamanagement',
                                                   'recuperate')
            if recuperate_actions:
                recuperate_actions[0].execute(context, request, appstruct, **kw)

        request.registry.notify(ActivityExecuted(self, [context], user))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def submit_roles_validation(process, context):
    return has_role(role=('Owner', context))


def submit_processsecurity_validation(process, context):
    request = get_current_request()
    if not request.moderate_ideas:
        return False

    if getattr(context, 'originalentity', None):
        originalentity = getattr(context, 'originalentity')
        if originalentity.text == context.text:
            return False

    return global_user_processsecurity(process, context)


def submit_state_validation(process, context):
    return 'to work' in context.state


class SubmitIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 6
    submission_title = _('Continue')
    context = Iidea
    roles_validation = submit_roles_validation
    processsecurity_validation = submit_processsecurity_validation
    state_validation = submit_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state = PersistentList(['submitted'])
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def decision_roles_validation(process, context):
    return has_role(role=('Moderator',))


def decision_processsecurity_validation(process, context):
    request = get_current_request()
    if not request.moderate_ideas:
        return False

    return global_user_processsecurity(process, context)


def decision_state_validation(process, context):
    return 'submitted' in context.state


class ArchiveIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-inbox'
    style_order = 4
    submission_title = _('Continue')
    context = Iidea
    roles_validation = decision_roles_validation
    processsecurity_validation = decision_processsecurity_validation
    state_validation = decision_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        explanation = appstruct['explanation']
        context.state = PersistentList(['archived'])
        context.reindex()
        user = context.author
        alert('internal', [root], [user],
              internal_kind=InternalAlertKind.moderation_alert,
              subjects=[context])

        if getattr(user, 'email', ''):
            mail_template = root.get_mail_template('archive_idea_decision')
            localizer = request.localizer
            subject = mail_template['subject'].format(subject_title=context.title)
            message = mail_template['template'].format(
                recipient_title=localizer.translate(
                    _(getattr(user, 'user_title', ''))),
                recipient_first_name=getattr(user, 'first_name', user.name),
                recipient_last_name=getattr(user, 'last_name', ''),
                subject_title=context.title,
                subject_url=request.resource_url(context, "@@index"),
                explanation=explanation,
                novaideo_title=root.title
            )
            alert('email', [root.get_site_sender()], [user.email],
                  subject=subject, body=message)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class PublishIdeaModeration(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 5
    submission_title = _('Continue')
    context = Iidea
    roles_validation = decision_roles_validation
    processsecurity_validation = decision_processsecurity_validation
    state_validation = decision_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        if 'idea' in getattr(root, 'content_to_support', []):
            context.state = PersistentList(['submitted_support', 'published'])
        else:
            context.state = PersistentList(['published', 'submitted_support'])

        context.init_published_at()
        context.reindex()
        user = context.author
        alert('internal', [root], [user],
              internal_kind=InternalAlertKind.moderation_alert,
              subjects=[context])
        if getattr(user, 'email', ''):
            localizer = request.localizer
            mail_template = root.get_mail_template('publish_idea_decision')
            subject = mail_template['subject'].format(subject_title=context.title)
            message = mail_template['template'].format(
                recipient_title=localizer.translate(
                    _(getattr(user, 'user_title', ''))),
                recipient_first_name=getattr(user, 'first_name', user.name),
                recipient_last_name=getattr(user, 'last_name', ''),
                subject_title=context.title,
                subject_url=request.resource_url(context, "@@index"),
                novaideo_title=root.title
            )
            alert('email', [root.get_site_sender()], [user.email],
                  subject=subject, body=message)

        request.registry.notify(ObjectPublished(object=context))
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def pub_roles_validation(process, context):
    return has_role(role=('Owner', context))


def pub_processsecurity_validation(process, context):
    request = get_current_request()
    if request.moderate_ideas:
        return False

    if getattr(context, 'originalentity', None):
        originalentity = getattr(context, 'originalentity')
        if originalentity.text == context.text:
            return False

    return global_user_processsecurity(process, context)


def pub_state_validation(process, context):
    return 'to work' in context.state or \
           'submitted' in context.state


class PublishIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 5
    submission_title = _('Continue')
    context = Iidea
    roles_validation = pub_roles_validation
    processsecurity_validation = pub_processsecurity_validation
    state_validation = pub_state_validation

    def start(self, context, request, appstruct, **kw):
        root = request.root
        if 'idea' in getattr(root, 'content_to_support', []):
            context.state = PersistentList(['submitted_support', 'published'])
        else:
            context.state = PersistentList(['published', 'submitted_support'])

        context.init_published_at()
        context.reindex()
        request.registry.notify(ObjectPublished(object=context))
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def ab_roles_validation(process, context):
    return has_role(role=('Owner', context))


def ab_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def ab_state_validation(process, context):
    return 'to work' in context.state


class AbandonIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-stop'
    style_order = 4
    context = Iidea
    roles_validation = ab_roles_validation
    processsecurity_validation = ab_processsecurity_validation
    state_validation = ab_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state = PersistentList(['archived'])
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def re_roles_validation(process, context):
    return has_role(role=('Owner', context))


def re_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def re_state_validation(process, context):
    return 'archived' in context.state and \
        'version' not in context.state


class RecuperateIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-play'
    style_order = 8
    context = Iidea
    roles_validation = re_roles_validation
    processsecurity_validation = re_processsecurity_validation
    state_validation = re_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state = PersistentList(['to work'])
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def comm_roles_validation(process, context):
    return has_role(role=('Member',))


def comm_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def comm_state_validation(process, context):
    return 'published' in context.state


class CommentIdea(InfiniteCardinality):
    isSequential = False
    style_descriminator = 'communication-action'
    style_interaction = 'modal-action'
    style_picto = 'ion-chatbubble'
    style_order = 0
    style_activate = True
    context = Iidea
    roles_validation = comm_roles_validation
    processsecurity_validation = comm_processsecurity_validation
    state_validation = comm_state_validation

    def get_nb(self, context, request):
        return context.channel.len_comments

    def get_title(self, context, request):
        len_comments = context.channel.len_comments
        return _("${title} (${nember})",
                 mapping={'nember': len_comments,
                          'title': request.localizer.translate(self.title)})

    def _get_users_to_alerts(self, context, request):
        users = list(get_users_by_preferences(context))
        author = getattr(context, 'author', None)
        context_authors = getattr(
            context, 'authors', [author] if author else [])
        users.extend(context_authors)
        return list(set(users))

    def _alert_users(self, context, request, user, comment):
        root = getSite()
        users = self._get_users_to_alerts(context, request)
        if user in users:
            users.remove(user)

        mail_template = root.get_mail_template('alert_comment')
        comment_oid = getattr(comment, '__oid__', 'None')
        localizer = request.localizer
        author_title = localizer.translate(
            _(getattr(user, 'user_title', '')))
        author_first_name = getattr(
            user, 'first_name', user.name)
        author_last_name = getattr(user, 'last_name', '')
        alert('internal', [root], users,
              internal_kind=InternalAlertKind.comment_alert,
              subjects=[context],
              comment_oid=comment_oid,
              author_title=author_title,
              author_first_name=author_first_name,
              author_last_name=author_last_name)
        subject_type = localizer.translate(
            _("The " + context.__class__.__name__.lower()))
        subject = mail_template['subject'].format(
            subject_title=context.title,
            subject_type=subject_type)
        for user_to_alert in [u for u in users if getattr(u, 'email', '')]:
            message = mail_template['template'].format(
                recipient_title=localizer.translate(
                    _(getattr(user_to_alert, 'user_title', ''))),
                recipient_first_name=getattr(
                    user_to_alert, 'first_name', user_to_alert.name),
                recipient_last_name=getattr(user_to_alert, 'last_name', ''),
                subject_title=context.title,
                subject_url=request.resource_url(context, "@@index") + '#comment-' + str(comment_oid),
                subject_type=subject_type,
                author_title=author_title,
                author_first_name=author_first_name,
                author_last_name=author_last_name,
                novaideo_title=root.title
            )
            alert('email', [root.get_site_sender()], [user_to_alert.email],
                  subject=subject, body=message)

    def start(self, context, request, appstruct, **kw):
        comment = appstruct['_object_data']
        channel = context.channel
        if channel:
            channel.addtoproperty('comments', comment)
            comment.format(request)
            user = get_current()
            comment.setproperty('author', user)
            if appstruct['related_contents']:
                related_contents = appstruct['related_contents']
                correlation = connect(
                    context,
                    list(related_contents),
                    {'comment': comment.comment,
                     'type': comment.intention},
                    user,
                    unique=True)
                comment.setproperty('related_correlation', correlation[0])

            self._alert_users(context, request, user, comment)
            context.reindex()

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def present_roles_validation(process, context):
    return has_role(role=('Member',))


def present_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def present_state_validation(process, context):
    return 'published' in context.state


class PresentIdea(InfiniteCardinality):
    style_descriminator = 'communication-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-share-alt'
    style_order = 1
    submission_title = _('Send')
    context = Iidea
    roles_validation = present_roles_validation
    processsecurity_validation = present_processsecurity_validation
    state_validation = present_state_validation

    def get_title(self, context, request):
        len_members = context.len_contacted
        return _("${title} (${nember})",
                 mapping={'nember': len_members,
                          'title': request.localizer.translate(self.title)})

    def start(self, context, request, appstruct, **kw):
        send_to_me = appstruct['send_to_me']
        members = list(appstruct['members'])
        root = request.root
        user = get_current()
        if send_to_me:
            members.append(user)

        localizer = request.localizer
        user_title = localizer.translate(_(getattr(user, 'user_title', '')))
        user_first_name = getattr(user, 'first_name', user.name)
        user_last_name = getattr(user, 'last_name', '')
        url = request.resource_url(context, "@@index")
        presentation_subject = appstruct['subject']
        presentation_message = appstruct['message']
        subject = presentation_subject.format(subject_title=context.title)
        users = [m for m in members if not isinstance(m, basestring)]
        alert('internal', [root], users,
              internal_kind=InternalAlertKind.content_alert,
              subjects=[context], alert_kind='present')
        for member in members:
            recipient_title = ''
            recipient_first_name = ''
            recipient_last_name = ''
            member_email = ''
            if not isinstance(member, basestring):
                member_email = getattr(member, 'email', '')
                recipient_title = localizer.translate(
                    _(getattr(member, 'user_title', '')))
                recipient_first_name = getattr(
                    member, 'first_name', member.name)
                recipient_last_name = getattr(
                    member, 'last_name', '')
            else:
                member_email = member

            if member_email:
                message = presentation_message.format(
                    recipient_title=recipient_title,
                    recipient_first_name=recipient_first_name,
                    recipient_last_name=recipient_last_name,
                    subject_url=url,
                    subject_title=getattr(context, 'title', context.name),
                    my_title=user_title,
                    my_first_name=user_first_name,
                    my_last_name=user_last_name,
                    novaideo_title=root.title
                )
                alert('email', [root.get_site_sender()], [member_email],
                      subject=subject, body=message)

            if member is not user and member_email \
               and member_email not in context._email_persons_contacted:
                context._email_persons_contacted.append(
                    member_email)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def associate_processsecurity_validation(process, context):
    return (has_role(role=('Owner', context)) or \
           (has_role(role=('Member',)) and 'published' in context.state)) and \
           global_user_processsecurity(process, context)


class Associate(InfiniteCardinality):
    context = Iidea
    processsecurity_validation = associate_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        correlation = appstruct['_object_data']
        correlation.setproperty('source', context)
        correlation.setproperty('author', user)
        root = getSite()
        root.addtoproperty('correlations', correlation)
        objects = list(correlation.targets)
        objects.append(context)
        request.registry.notify(ActivityExecuted(self, objects, user))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def get_access_key(obj):
    if 'published' in obj.state:
        return ['always']
    elif 'submitted' in obj.state:
        return serialize_roles(
            (('Owner', obj), 'Admin', 'Moderator'))
    else:
        return serialize_roles(
            (('Owner', obj), 'Admin'))


def seeidea_processsecurity_validation(process, context):
    return access_user_processsecurity(process, context) and \
           ('published' in context.state or\
            has_any_roles(roles=(('Owner', context), 'Admin')) or\
            ('submitted' in context.state and has_role(role=('Moderator',)))
            )


@access_action(access_key=get_access_key)
class SeeIdea(InfiniteCardinality):
    """SeeIdea is the behavior allowing access to context"""
    title = _('Details')
    context = Iidea
    actionType = ActionType.automatic
    processsecurity_validation = seeidea_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def compare_roles_validation(process, context):
    return has_role(role=('Owner', context))


def compare_processsecurity_validation(process, context):
    return getattr(context, 'version', None) is not None


class CompareIdea(InfiniteCardinality):
    title = _('Compare')
    context = Iidea
    roles_validation = compare_roles_validation
    processsecurity_validation = compare_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def opinion_roles_validation(process, context):
    return has_role(role=('Examiner',))


def opinion_processsecurity_validation(process, context):
    request = get_current_request()
    if 'idea' not in request.content_to_examine:
        return False

    return global_user_processsecurity(process, context)


def opinion_state_validation(process, context):
    return 'published' in context.state and 'examined' not in context.state


class MakeOpinion(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 10
    submission_title = _('Save')
    context = Iidea
    roles_validation = opinion_roles_validation
    processsecurity_validation = opinion_processsecurity_validation
    state_validation = opinion_state_validation

    def start(self, context, request, appstruct, **kw):
        appstruct.pop('_csrf_token_')
        context.opinion = PersistentDict(appstruct)
        old_state = context.state[0]
        context.state = PersistentList(
            ['examined', 'published', context.opinion['opinion']])
        context.init_examined_at()
        context.reindex()
        for token in list(context.tokens):
            token.owner.addtoproperty('tokens', token)

        member = context.author
        root = getSite()
        users = list(get_users_by_preferences(context))
        users.append(member)
        alert('internal', [root], users,
              internal_kind=InternalAlertKind.examination_alert,
              subjects=[context])

        if getattr(member, 'email', ''):
            url = request.resource_url(context, "@@index")
            mail_template = root.get_mail_template('opinion_idea')
            subject = mail_template['subject'].format(subject_title=context.title)
            localizer = request.localizer
            message = mail_template['template'].format(
                recipient_title=localizer.translate(
                    _(getattr(member, 'user_title', ''))),
                recipient_first_name=getattr(member, 'first_name', member.name),
                recipient_last_name=getattr(member, 'last_name', ''),
                subject_url=url,
                subject_title=context.title,
                opinion=localizer.translate(_(context.opinion_value)),
                explanation=context.opinion['explanation'],
                novaideo_title=root.title
            )
            alert('email', [root.get_site_sender()], [member.email],
                  subject=subject, body=message)

        request.registry.notify(ObjectModified(
            object=context,
            args={
                'state_source': old_state,
                'state_target': 'examined'
            }))
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def support_roles_validation(process, context):
    return has_role(role=('Member',))


def support_processsecurity_validation(process, context):
    user = get_current()
    request = get_current_request()
    if 'idea' not in request.content_to_support:
        return False

    return getattr(user, 'tokens', []) and  \
           not (user in [t.owner for t in context.tokens]) and \
           global_user_processsecurity(process, context)


def support_state_validation(process, context):
    return 'published' in context.state and \
        'examined' not in context.state


class SupportIdea(InfiniteCardinality):
    # style = 'button' #TODO add style abstract class
    # style_descriminator = 'text-action'
    # style_picto = 'glyphicon glyphicon-thumbs-up'
    # style_order = 4
    context = Iidea
    roles_validation = support_roles_validation
    processsecurity_validation = support_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        token = user.tokens[-1]
        context.addtoproperty('tokens_support', token)
        context.init_support_history()
        context._support_history.append(
            (get_oid(user), datetime.datetime.now(tz=pytz.UTC), 1))
        request.registry.notify(ActivityExecuted(self, [context], user))
        if user is not context.author:
            alert('internal', [request.root], [context.author],
              internal_kind=InternalAlertKind.support_alert,
              subjects=[context], support_kind='support')

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class OpposeIdea(InfiniteCardinality):
    # style = 'button' #TODO add style abstract class
    # style_descriminator = 'text-action'
    # style_picto = 'glyphicon glyphicon-thumbs-down'
    # style_order = 5
    context = Iidea
    roles_validation = support_roles_validation
    processsecurity_validation = support_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        token = user.tokens[-1]
        context.addtoproperty('tokens_opposition', token)
        context.init_support_history()
        context._support_history.append(
            (get_oid(user), datetime.datetime.now(tz=pytz.UTC), 0))
        request.registry.notify(ActivityExecuted(self, [context], user))
        if user is not context.author:
            alert('internal', [request.root], [context.author],
                  internal_kind=InternalAlertKind.support_alert,
                  subjects=[context], support_kind='oppose')

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def withdrawt_processsecurity_validation(process, context):
    user = get_current()
    return any((t.owner is user) for t in context.tokens) and \
           global_user_processsecurity(process, context)


class WithdrawToken(InfiniteCardinality):
    # style = 'button' #TODO add style abstract class
    # style_descriminator = 'text-action'
    # style_picto = 'glyphicon glyphicon-share-alt'
    # style_order = 6
    context = Iidea
    roles_validation = support_roles_validation
    processsecurity_validation = withdrawt_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        user_tokens = [t for t in context.tokens
                       if t.owner is user]
        token = user_tokens[-1]
        context.delfromproperty(token.__property__, token)
        user.addtoproperty('tokens', token)
        context.init_support_history()
        context._support_history.append(
            (get_oid(user), datetime.datetime.now(tz=pytz.UTC), -1))
        request.registry.notify(ActivityExecuted(self, [context], user))
        if user is not context.author:
            alert('internal', [request.root], [context.author],
                  internal_kind=InternalAlertKind.support_alert,
                  subjects=[context], support_kind='withdraw')

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def seewgs_state_validation(process, context):
    request = get_current_request()
    if getattr(request, 'is_idea_box', False):
        return False

    condition = False
    if 'idea' in request.content_to_examine:
        condition = 'favorable' in context.state
    else:
        condition = 'published' in context.state

    return condition and has_role(role=('Member',))


class SeeRelatedWorkingGroups(InfiniteCardinality):
    style_descriminator = 'primary-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-link'
    style_order = 2
    context = Iidea
    #processsecurity_validation = seeideas_processsecurity_validation
    #roles_validation = seeideas_roles_validation
    state_validation = seewgs_state_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))
#TODO behaviors

VALIDATOR_BY_CONTEXT[Idea] = CommentIdea
