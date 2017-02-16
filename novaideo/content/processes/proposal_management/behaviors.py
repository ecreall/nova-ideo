# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the 
Proposal management process definition. 
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
    copy,
    find_service,
    get_obj)
from dace.objectofcollaboration.principal.util import (
    has_role,
    grant_roles,
    get_current,
    revoke_roles,
    has_any_roles)
#from dace.objectofcollaboration import system
import html_diff_wrapper
from dace.processinstance.activity import (
    InfiniteCardinality, ElementaryAction, ActionType)
from dace.processinstance.core import ActivityExecuted
from pontus.file import OBJECT_DATA
from pontus.interfaces import IFile

from novaideo.content.interface import (
    INovaIdeoApplication,
    IProposal,
    Iidea,
    IWorkspace)
from ..user_management.behaviors import (
    global_user_processsecurity,
    access_user_processsecurity)
from novaideo import _, nothing
from novaideo.content.proposal import Proposal
from ..comment_management import VALIDATOR_BY_CONTEXT
from novaideo.content.correlation import CorrelationType
from novaideo.content.token import Token
from novaideo.content.working_group import WorkingGroup
from novaideo.content.processes.idea_management.behaviors import (
    PresentIdea,
    CommentIdea,
    Associate as AssociateIdea)
from novaideo.utilities.util import (
    connect, to_localized_time)
from novaideo.event import (
    ObjectPublished, CorrelableRemoved)
from novaideo.content.processes.proposal_management import WORK_MODES
from novaideo.core import access_action, serialize_roles
from novaideo.content.alert import InternalAlertKind
from novaideo.content.workspace import Workspace
from novaideo.views.filter import get_users_by_preferences
from novaideo.utilities.alerts_utility import (
    alert, get_user_data, get_entity_data, alert_comment_nia)
from . import (
    AMENDMENTS_CYCLE_DEFAULT_DURATION,
    init_proposal_ballots,
    add_files_to_workspace,
    add_attached_files,
    end_work,
    remove_participant_from_ballots
    )

VOTE_PUBLISHING_MESSAGE = _("Each participant in the working group votes for or against continuing the improvement of the proposal. "
                            "If the majority is \"In favour\", a new improvement cycle begins. "
                            "If not, the proposal is submitted as is to the evaluation of the other "
                            "members of the platform.")


VOTE_DURATION_MESSAGE = _("Voting results regarding the further improvement of the proposal will not be known until the end of the ballot. "
                          "If the majority happens to vote for continuing to improve the "
                          "proposal, your vote on the duration of the improvement cycle is needed.")

VOTE_MODEWORK_MESSAGE = _("Voting results regarding the further improvement of the proposal will not be known until the end of the ballot. "
                          "If the majority happens to vote for continuing to improve the "
                          "proposal before submitting it to the other members of the platform,"
                          " your vote on the operating method of the working group is needed.")


VOTE_REOPENING_MESSAGE = _("Voting results regarding the further improvement of the proposal will not be known until the end of the ballot. "
                           "If the majority happens to vote for continuing to improve the "
                           "proposal before submitting it to the other members of the platform,"
                          " your vote on reopening the working group is needed.")


def confirm_proposal(
    context, request, user, submitted_appstruct, root):
    working_group = context.working_group
    if context.originalentity:
        # Add Nia comment
        alert_comment_nia(
            context.originalentity, request, root,
            internal_kind=InternalAlertKind.content_alert,
            subject_type='proposal',
            alert_kind='duplicated',
            duplication=context
            )
    
    proposal_state = 'amendable'
    if submitted_appstruct.get('vote', False):
        proposal_state = 'published'
        if root.support_proposals:
            proposal_state = 'submitted_support'
            context.state = PersistentList(
                ['submitted_support', 'published'])
            # Add Nia comment
            alert_comment_nia(
                context, request, root,
                internal_kind=InternalAlertKind.working_group_alert,
                subject_type='proposal',
                alert_kind='submitted_support',
                duplication=context
                )
        else:
            context.state = PersistentList(
                ['published', 'submitted_support'])

        working_group.state = PersistentList(['archived'])
        context.reindex()
        working_group.reindex()
    else:
        default_mode = root.get_default_work_mode()
        participants_mini = root.participants_mini
        mode_id = submitted_appstruct.get(
            'work_mode', default_mode.work_id)
        if mode_id:
            working_group.work_mode_id = mode_id
            participants_mini = WORK_MODES[mode_id].participants_mini

        #Only the vote of the author is considered
        first_vote_registration(
            user, working_group, submitted_appstruct)
        if participants_mini > 1:
            context.state = PersistentList(
                ['open to a working group', 'published'])
            context.reindex()
            # Add Nia comment
            alert_comment_nia(
                context, request, root,
                internal_kind=InternalAlertKind.working_group_alert,
                subject_type='proposal',
                alert_kind='open_to_a_working_group',
                duplication=context
                )
        else:
            context.state = PersistentList(['amendable', 'published'])
            working_group.state = PersistentList(['active'])
            context.reindex()
            working_group.reindex()
            if not hasattr(working_group, 'first_improvement_cycle'):
                working_group.first_improvement_cycle = True

            if not working_group.improvement_cycle_proc:
                improvement_cycle_proc = start_improvement_cycle(context)
                working_group.setproperty(
                    'improvement_cycle_proc', improvement_cycle_proc)

            working_group.improvement_cycle_proc.execute_action(
                context, request, 'votingpublication', {})

            # Add Nia comment
            alert_comment_nia(
                context, request, root,
                internal_kind=InternalAlertKind.working_group_alert,
                subject_type='proposal',
                alert_kind='start_work',
                duplication=context
                )

    related_ideas = context.related_ideas
    for idea in related_ideas:
        # Add Nia comment
        alert_comment_nia(
            idea, request, root,
            internal_kind=InternalAlertKind.working_group_alert,
            subject_type='idea',
            alert_kind='new_proposal',
            proposal_state=proposal_state,
            proposal=context
            )

    root.merge_keywords(context.keywords)
    context.modified_at = datetime.datetime.now(tz=pytz.UTC)
    context.init_published_at()
    not_published_ideas = []
    if not getattr(root, 'moderate_ideas', False) and\
       'idea' not in getattr(root, 'content_to_examine', []):
        not_published_ideas = [i for i in context.related_ideas
                               if 'published' not in i.state]
        publish_ideas(not_published_ideas, request)

    not_published_ideas.extend(context)
    return not_published_ideas


def publish_ideas(ideas, request):
    for idea in ideas:
        idea.state = PersistentList(['published'])
        idea.modified_at = datetime.datetime.now(tz=pytz.UTC)
        idea.reindex()
        request.registry.notify(ObjectPublished(object=idea))


def publish_condition(process):
    proposal = process.execution_context.created_entity('proposal')
    if proposal:
        working_group = proposal.working_group
        report = working_group.vp_ballot.report
        if not getattr(working_group, 'first_vote', True):
            electeds = report.get_electeds()
            if electeds is None:
                return False
            else:
                return True

        report.calculate_votes()
        if report.result['False'] != 0:
            return False

    return True


def exclude_participant_from_wg(context, request,  user, root, kind='resign'):
    working_group = context.working_group
    working_group.delfromproperty('members', user)
    remove_participant_from_ballots(context, request, user)
    members = working_group.members
    mode = getattr(working_group, 'work_mode', root.get_default_work_mode())
    revoke_roles(user, (('Participant', context),))
    subject_data = get_entity_data(context, 'subject', request)
    if members:
        alert_data = get_user_data(user, 'participant', request)
        alert_data.update(get_entity_data(user, 'participant', request))
        alert_data.update(subject_data)
        alert(
            'internal', [root], members,
            internal_kind=InternalAlertKind.working_group_alert,
            subjects=[context], alert_kind=kind,
            **alert_data)

    sender = root.get_site_sender()
    if working_group.wating_list:
        def _get_next_user(users):
            for user in users:
                wgs = user.active_working_groups
                if 'active' in user.state and \
                   len(wgs) < root.participations_maxi:
                    return user

            return None

        next_user = _get_next_user(working_group.wating_list)
        if next_user is not None:
            mail_template = root.get_mail_template(
                'wg_wating_list_participation')
            working_group.delfromproperty('wating_list', next_user)
            working_group.addtoproperty('members', next_user)
            grant_roles(next_user, (('Participant', context),))
            if members:
                alert('internal', [root], members,
                      internal_kind=InternalAlertKind.working_group_alert,
                      subjects=[context],
                      alert_kind='wg_wating_list_participation')

            if getattr(next_user, 'email', ''):
                subject = mail_template['subject'].format(
                    subject_title=context.title)
                email_data = get_user_data(next_user, 'recipient', request)
                email_data.update(subject_data)
                message = mail_template['template'].format(
                    novaideo_title=root.title,
                    **email_data
                )
                alert('email', [sender], [next_user.email],
                      subject=subject, body=message)

    participants = working_group.members
    len_participants = len(participants)
    if len_participants < mode.participants_mini and \
       'open to a working group' not in context.state:
        context.state = PersistentList(
            ['open to a working group', 'published'])
        working_group.state = PersistentList(['deactivated'])
        working_group.reindex()
        context.reindex()
        alert('internal', [root], participants,
              internal_kind=InternalAlertKind.working_group_alert,
              subjects=[context], alert_kind=kind+'_to_wg_open')
        # Add Nia comment
        alert_comment_nia(
            context, request, root,
            internal_kind=InternalAlertKind.working_group_alert,
            subject_type='proposal',
            alert_kind='exclusion_open_to_a_wg',
            duplication=context
            )

    if getattr(user, 'email', ''):
        mail_template = root.get_mail_template('wg_'+kind)
        subject = mail_template['subject'].format(
            subject_title=context.title)
        email_data = get_user_data(user, 'recipient', request)
        email_data.update(subject_data)
        message = mail_template['template'].format(
            novaideo_title=root.title,
            **email_data
        )
        alert('email', [sender], [user.email],
              subject=subject, body=message)


def start_improvement_cycle(proposal):
    def_container = find_service('process_definition_container')
    runtime = find_service('runtime')
    pd = def_container.get_definition('proposalimprovementcycle')
    proc = pd()
    proc.__name__ = proc.id
    runtime.addtoproperty('processes', proc)
    proc.defineGraph(pd)
    proc.execution_context.add_created_entity('proposal', proposal)
    proc.execute()
    return proc


def close_votes(context, request, vote_processes):
    vote_actions = [process.get_actions('vote')
                    for process in vote_processes]
    vote_actions = [action for actions in vote_actions
                    for action in actions]
    for action in vote_actions:
        action.close_vote(context, request)


def first_vote_registration(user, working_group, appstruct):
    #duration vote
    ballot = working_group.duration_configuration_ballot
    report = ballot.report
    if user not in report.voters:
        elected_id = appstruct['elected']
        try:
            subject_id = get_oid(elected_id[OBJECT_DATA])
        except Exception:
            subject_id = elected_id
        votefactory = report.ballottype.vote_factory
        vote = votefactory(subject_id)
        vote.user_id = get_oid(user)
        ballot.ballot_box.addtoproperty('votes', vote)
        report.addtoproperty('voters', user)
    #publication vote
    ballot = working_group.vp_ballot
    report = ballot.report
    if user not in report.voters:
        vote = appstruct['vote']
        votefactory = report.ballottype.vote_factory
        vote = votefactory(vote)
        vote.user_id = get_oid(user)
        ballot.ballot_box.addtoproperty('votes', vote)
        report.addtoproperty('voters', user)


def first_vote_remove(user, working_group):
    user_oid = get_oid(user)
    #duration vote
    ballot = working_group.duration_configuration_ballot
    votes = [v for v in ballot.ballot_box.votes
             if getattr(v, 'user_id', 0) == user_oid]
    if votes:
        ballot.ballot_box.delfromproperty('votes', votes[0])
        ballot.report.delfromproperty('voters', user)

    #publication vote
    ballot = working_group.vp_ballot
    votes = [v for v in ballot.ballot_box.votes
             if getattr(v, 'user_id', 0) == user_oid]
    if votes:
        ballot.ballot_box.delfromproperty('votes', votes[0])
        ballot.report.delfromproperty('voters', user)


def calculate_improvement_cycle_duration(process):
    if getattr(process, 'attachedTo', None):
        process = process.attachedTo.process

    proposal = process.execution_context.created_entity('proposal')
    working_group = proposal.working_group
    duration_ballot = getattr(
        working_group, 'duration_configuration_ballot', None)
    if duration_ballot is not None and duration_ballot.report.voters:
        electeds = duration_ballot.report.get_electeds()
        if electeds:
            return AMENDMENTS_CYCLE_DEFAULT_DURATION[electeds[0]]

    return AMENDMENTS_CYCLE_DEFAULT_DURATION["One week"]


def calculate_improvement_cycle_date(process):
    return calculate_improvement_cycle_duration(process) + \
        datetime.datetime.now()


def createproposal_roles_validation(process, context):
    return has_role(role=('SiteAdmin',))


def createproposal_processsecurity_validation(process, context):
    request = get_current_request()
    if getattr(request, 'is_idea_box', False):
        return False

    return global_user_processsecurity()


def include_ideas_texts(proposal, related_ideas):
    proposal.text = getattr(proposal, 'text', '') +\
                    ''.join(['<div>' + idea.text + '</div>' \
                             for idea in related_ideas])


class CreateProposal(InfiniteCardinality):
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = createproposal_roles_validation
    processsecurity_validation = createproposal_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current(request)
        related_ideas = appstruct.pop('related_ideas')
        proposal = appstruct['_object_data']
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

        #TODO Add Nia comment to related ideas
        add_attached_files(appstruct, proposal)
        proposal.reindex()
        init_proposal_ballots(proposal)
        wg.reindex()
        proposal.subscribe_to_channel(user)
        request.registry.notify(ActivityExecuted(self, [proposal, wg], user))
        return {'newcontext': proposal}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def pap_processsecurity_validation(process, context):
    request = get_current_request()
    if getattr(request, 'is_idea_box', False):
        return False

    condition = False
    if 'idea' in request.content_to_examine:
        condition = 'favorable' in context.state
    else:
        condition = 'published' in context.state

    return condition and has_role(role=('Member',))


class PublishAsProposal(CreateProposal):
    style = 'button' #TODO add style abstract class
    context = Iidea
    submission_title = _('Save')
    style_order = 0
    style_descriminator = 'primary-action'
    style_picto = 'novaideo-icon icon-wg'
    processsecurity_validation = pap_processsecurity_validation
    roles_validation = NotImplemented


def del_processsecurity_validation(process, context):
    return global_user_processsecurity() and \
           (has_role(role=('Owner', context)) and \
           'draft' in context.state)


class DeleteProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_order = 12
    submission_title = _('Continue')
    context = IProposal
    processsecurity_validation = del_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        not_draft_owner = 'draft' not in context.state or \
                          not has_role(role=('Owner', context))
        context.remove_tokens()
        wg = context.working_group
        members = list(wg.members)
        for member in members:
            wg.delfromproperty('members', member)

        wg.delfromproperty('proposal', context)
        root.delfromproperty('working_groups', wg)
        request.registry.notify(CorrelableRemoved(object=context))
        root.delfromproperty('proposals', context)
        if not_draft_owner:
            mail_template = root.get_mail_template('delete_proposal')
            explanation = appstruct['explanation']
            subject = mail_template['subject'].format(
                subject_title=context.title)
            alert('internal', [root], members,
                  internal_kind=InternalAlertKind.moderation_alert,
                  subjects=[], removed=True, subject_title=context.title)
            subject_data = get_entity_data(context, 'subject', request)
            for member in members:
                if getattr(member, 'email', ''):
                    email_data = get_user_data(member, 'recipient', request)
                    email_data.update(subject_data)
                    message = mail_template['template'].format(
                        explanation=explanation,
                        novaideo_title=root.title,
                        **email_data
                    )
                    alert('email', [root.get_site_sender()], [member.email],
                          subject=subject, body=message)

        return {'newcontext': root}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], ""))


def pu_sub_processsecurity_validation(process, context):
    user = get_current()
    root = getSite()
    not_published_ideas = False
    if getattr(root, 'moderate_ideas', False):
        not_published_ideas = any('published' not in i.state
                                  for i in context.related_ideas)

    not_favorable_ideas = False
    if 'idea' in getattr(root, 'content_to_examine', []):
        not_favorable_ideas = any('favorable' not in i.state
                                  for i in context.related_ideas)

    return not (not_published_ideas or not_favorable_ideas) and \
           len(user.active_working_groups) < root.participations_maxi and \
           global_user_processsecurity()


def submit_roles_validation(process, context):
    return has_role(role=('Owner', context))


def submit_processsecurity_validation(process, context):
    request = get_current_request()
    if not request.moderate_proposals:
        return False

    return pu_sub_processsecurity_validation(process, context)


def submit_state_validation(process, context):
    return 'draft' in context.state


class SubmitProposalModeration(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 6
    submission_title = _('Continue')
    context = IProposal
    roles_validation = submit_roles_validation
    processsecurity_validation = submit_processsecurity_validation
    state_validation = submit_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state = PersistentList(['submitted'])
        context.submitted_appstruct = PersistentDict(appstruct)
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def decision_roles_validation(process, context):
    return has_role(role=('Moderator',))


def decision_processsecurity_validation(process, context):
    request = get_current_request()
    if not request.moderate_proposals:
        return False

    return global_user_processsecurity()


def decision_state_validation(process, context):
    return 'submitted' in context.state


class ArchiveProposalModeration(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-inbox'
    style_order = 4
    submission_title = _('Continue')
    context = IProposal
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
              subjects=[context], alert_kind='moderation')
        if getattr(user, 'email', ''):
            mail_template = root.get_mail_template('archive_proposal_decision')
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


class PublishProposalModeration(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 5
    submission_title = _('Continue')
    context = IProposal
    roles_validation = decision_roles_validation
    processsecurity_validation = decision_processsecurity_validation
    state_validation = decision_state_validation

    def start(self, context, request, appstruct, **kw):
        user = context.author
        root = getSite()
        context.state.remove('submitted')
        submitted_appstruct = getattr(context, 'submitted_appstruct', {})
        not_published_ideas = confirm_proposal(
            context, request, user, submitted_appstruct, root)
        alert('internal', [root], [user],
              internal_kind=InternalAlertKind.moderation_alert,
              subjects=[context], alert_kind='moderation')
        if getattr(user, 'email', ''):
            mail_template = root.get_mail_template('publish_proposal_decision')
            subject = mail_template['subject'].format(
                subject_title=context.title)
            email_data = get_user_data(user, 'recipient', request)
            email_data.update(get_entity_data(context, 'subject', request))
            message = mail_template['template'].format(
                novaideo_title=root.title,
                **email_data
            )
            alert('email', [root.get_site_sender()], [user.email],
                  subject=subject, body=message)

        request.registry.notify(ObjectPublished(object=context))
        request.registry.notify(ActivityExecuted(
            self, not_published_ideas, user))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def publish_roles_validation(process, context):
    return has_role(role=('Owner', context))


def publish_processsecurity_validation(process, context):
    request = get_current_request()
    if request.moderate_proposals:
        return False
    return pu_sub_processsecurity_validation(process, context)


def publish_state_validation(process, context):
    return "draft" in context.state


class PublishProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 13
    submission_title = _('Continue')
    context = IProposal
    roles_validation = publish_roles_validation
    processsecurity_validation = publish_processsecurity_validation
    state_validation = publish_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current(request)
        root = getSite()
        context.state.remove('draft')
        not_published_ideas = confirm_proposal(
            context, request, user, appstruct, root)
        request.registry.notify(ObjectPublished(object=context))
        request.registry.notify(ActivityExecuted(
            self, not_published_ideas, user))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def duplicate_processsecurity_validation(process, context):
    return 'draft' not in context.state and \
           global_user_processsecurity()


class DuplicateProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'octicon octicon-git-branch'
    style_order = 7
    submission_title = _('Save')
    context = IProposal
    processsecurity_validation = duplicate_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        related_ideas = appstruct.pop('related_ideas')
        copy_of_proposal = copy(
            context, (root, 'proposals'),
            omit=('created_at', 'modified_at',
                  'examined_at', 'published_at',
                  'opinion', 'attached_files',
                  'len_selections', 'graph'))
        copy_of_proposal.opinion = PersistentDict({})
        copy_of_proposal.init_graph()
        copy_of_proposal.set_data(appstruct)
        copy_of_proposal.text = html_diff_wrapper.normalize_text(
            copy_of_proposal.text)
        copy_of_proposal.setproperty('originalentity', context)
        copy_of_proposal.state = PersistentList(['draft'])
        grant_roles(user=user, roles=(('Owner', copy_of_proposal), ))
        grant_roles(user=user, roles=(('Participant', copy_of_proposal), ))
        copy_of_proposal.setproperty('author', user)
        wg = WorkingGroup()
        root.addtoproperty('working_groups', wg)
        wg.init_workspace()
        wg.setproperty('proposal', copy_of_proposal)
        wg.addtoproperty('members', user)
        wg.state.append('deactivated')
        if related_ideas:
            connect(copy_of_proposal,
                    related_ideas,
                    {'comment': _('Add related ideas'),
                     'type': _('Duplicate')},
                    user,
                    ['related_proposals', 'related_ideas'],
                    CorrelationType.solid)

        add_attached_files(appstruct, copy_of_proposal)
        wg.reindex()
        copy_of_proposal.reindex()
        init_proposal_ballots(copy_of_proposal)
        context.reindex()
        request.registry.notify(ActivityExecuted(
            self, [copy_of_proposal, wg], user))
        copy_of_proposal.subscribe_to_channel(user)
        return {'newcontext': copy_of_proposal}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def edit_roles_validation(process, context):
    return has_role(role=('Owner', context))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity()


def edit_state_validation(process, context):
    return "draft" in context.state


class EditProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    submission_title = _('Save')
    context = IProposal
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current(request)
        if 'related_ideas' in appstruct:
            context.set_related_ideas(
                appstruct['related_ideas'], user)

        add_attached_files(appstruct, context)
        context.text = html_diff_wrapper.normalize_text(context.text)
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        request.registry.notify(ActivityExecuted(self, [context], user))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def support_roles_validation(process, context):
    return has_role(role=('Member',))


def support_processsecurity_validation(process, context):
    request = get_current_request()
    if not request.support_proposals:
        return False

    user = get_current()
    return context.get_token(user) and  \
           not (user in [t.owner for t in context.tokens]) and \
           global_user_processsecurity()


def support_state_validation(process, context):
    return 'submitted_support' in context.state


class SupportProposal(InfiniteCardinality):
    # style = 'button' #TODO add style abstract class
    # style_descriminator = 'text-action'
    # style_picto = 'glyphicon glyphicon-thumbs-up'
    # style_order = 4
    context = IProposal
    roles_validation = support_roles_validation
    processsecurity_validation = support_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        token = context.get_token(user)
        context.addtoproperty('tokens_support', token)
        context.init_support_history()
        context._support_history.append(
            (get_oid(user), datetime.datetime.now(tz=pytz.UTC), 1))
        context.reindex()
        request.registry.notify(ActivityExecuted(self, [context], user))
        users = list(get_users_by_preferences(context))
        users.extend(context.working_group.members)
        alert('internal', [request.root], users,
              internal_kind=InternalAlertKind.support_alert,
              subjects=[context], support_kind='support')
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class OpposeProposal(InfiniteCardinality):
    # style = 'button' #TODO add style abstract class
    # style_descriminator = 'text-action'
    # style_picto = 'glyphicon glyphicon-thumbs-down'
    # style_order = 5
    context = IProposal
    roles_validation = support_roles_validation
    processsecurity_validation = support_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        token = context.get_token(user)
        context.addtoproperty('tokens_opposition', token)
        context.init_support_history()
        context._support_history.append(
            (get_oid(user), datetime.datetime.now(tz=pytz.UTC), 0))
        context.reindex()
        request.registry.notify(ActivityExecuted(self, [context], user))
        users = list(get_users_by_preferences(context))
        users.extend(context.working_group.members)
        alert('internal', [request.root], users,
              internal_kind=InternalAlertKind.support_alert,
              subjects=[context], support_kind='oppose')
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def opinion_roles_validation(process, context):
    return has_role(role=('Examiner',))


def opinion_processsecurity_validation(process, context):
    request = get_current_request()
    if 'proposal' not in request.content_to_examine:
        return False

    return global_user_processsecurity()


def opinion_state_validation(process, context):
    return 'submitted_support' in context.state and 'examined' not in context.state


class MakeOpinion(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'octicon octicon-checklist'
    style_order = 10
    submission_title = _('Save')
    context = IProposal
    roles_validation = opinion_roles_validation
    processsecurity_validation = opinion_processsecurity_validation
    state_validation = opinion_state_validation

    def start(self, context, request, appstruct, **kw):
        appstruct.pop('_csrf_token_')
        context.opinion = PersistentDict(appstruct)
        context.state = PersistentList(
            ['examined', 'published', context.opinion['opinion']])
        context.init_examined_at()
        context.reindex()
        context.remove_tokens()
        members = context.working_group.members
        root = getSite()
        mail_template = root.get_mail_template('opinion_proposal')
        subject = mail_template['subject'].format(subject_title=context.title)
        localizer = request.localizer
        users = list(get_users_by_preferences(context))
        users.extend(members)
        alert('internal', [root], users,
              internal_kind=InternalAlertKind.examination_alert,
              subjects=[context])
        # Add Nia comment
        alert_comment_nia(
            context, request, root,
            internal_kind=InternalAlertKind.examination_alert,
            subject_type='proposal'
            )
        subject_data = get_entity_data(context, 'subject', request)
        for member in members:
            if getattr(member, 'email', ''):
                email_data = get_user_data(member, 'recipient', request)
                email_data.update(subject_data)
                message = mail_template['template'].format(
                    opinion=localizer.translate(_(context.opinion_value)),
                    explanation=context.opinion['explanation'],
                    novaideo_title=request.root.title,
                    **email_data
                )
                alert('email', [root.get_site_sender()], [member.email],
                      subject=subject, body=message)

        request.registry.notify(ActivityExecuted(
            self, [context], get_current(request)))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def withdrawt_processsecurity_validation(process, context):
    user = get_current()
    return any((t.owner is user) for t in context.tokens) and \
           global_user_processsecurity()


class WithdrawToken(InfiniteCardinality):
    # style = 'button' #TODO add style abstract class
    # style_descriminator = 'text-action'
    # style_picto = 'glyphicon glyphicon-share-alt'
    # style_order = 6
    context = IProposal
    roles_validation = support_roles_validation
    processsecurity_validation = withdrawt_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current(request)
        user_tokens = [t for t in context.tokens
                       if t.owner is user]
        token = user_tokens[-1]
        context.delfromproperty(token.__property__, token)
        user.addtoproperty('tokens', token)
        context.init_support_history()
        context._support_history.append(
            (get_oid(user), datetime.datetime.now(tz=pytz.UTC), -1))
        context.reindex()
        request.registry.notify(ActivityExecuted(self, [context], user))
        users = list(get_users_by_preferences(context))
        users.extend(context.working_group.members)
        alert('internal', [request.root], users,
              internal_kind=InternalAlertKind.support_alert,
              subjects=[context], support_kind='withdraw')
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def comm_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def comm_roles_validation(process, context):
    return has_role(role=('Member',))


def comm_processsecurity_validation(process, context):
    return global_user_processsecurity()


def comm_state_validation(process, context):
    return 'draft' not in context.state and \
        'censored' not in context.state


class CommentProposal(CommentIdea):
    context = IProposal
    roles_validation = comm_roles_validation
    processsecurity_validation = comm_processsecurity_validation
    state_validation = comm_state_validation


def comma_roles_validation(process, context):
    return has_role(role=('Anonymous',), ignore_superiors=True)


def comma_processsecurity_validation(process, context):
    return True


class CommentProposalAnonymous(CommentProposal):
    roles_validation = comma_roles_validation
    processsecurity_validation = comma_processsecurity_validation
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'

    def start(self, context, request, appstruct, **kw):
        return {}


def seea_roles_validation(process, context):
    return has_role(role=('Participant', context))


def seea_processsecurity_validation(process, context):
    return any(not('archived' in a.state) for a in context.amendments) and \
          global_user_processsecurity()


class SeeAmendments(InfiniteCardinality):
    isSequential = False
    context = IProposal
    roles_validation = seea_roles_validation
    processsecurity_validation = seea_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def seem_processsecurity_validation(process, context):
    return global_user_processsecurity()


class SeeMembers(InfiniteCardinality):
    style_descriminator = 'listing-wg-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'slider'
    style_picto = 'fa fa-users'
    isSequential = False
    context = IProposal
    processsecurity_validation = seem_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def present_roles_validation(process, context):
    return has_role(role=('Member',))


def present_processsecurity_validation(process, context):
    return global_user_processsecurity()


def present_state_validation(process, context):
    return 'draft' not in context.state and \
        'censored' not in context.state


class PresentProposal(PresentIdea):
    context = IProposal
    roles_validation = present_roles_validation
    processsecurity_validation = present_processsecurity_validation
    state_validation = present_state_validation


def presenta_roles_validation(process, context):
    return has_role(role=('Anonymous',), ignore_superiors=True)


def presenta_processsecurity_validation(process, context):
    return True


class PresentProposalAnonymous(PresentProposal):
    roles_validation = presenta_roles_validation
    processsecurity_validation = presenta_processsecurity_validation
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'

    def start(self, context, request, appstruct, **kw):
        return {}


def associate_processsecurity_validation(process, context):
    return (has_role(role=('Owner', context)) or \
           (has_role(role=('Member',)) and \
            'draft' not in context.state)) and \
           global_user_processsecurity()


class Associate(AssociateIdea):
    context = IProposal
    processsecurity_validation = associate_processsecurity_validation


def seeideas_state_validation(process, context):
    return 'draft' not in context.state or \
           ('draft' in context.state and has_role(role=('Owner', context)))


class SeeRelatedIdeas(InfiniteCardinality):
    style_descriminator = 'listing-primary-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'slider'
    # style_interaction_container = 'modal-l'
    style_picto = 'glyphicon glyphicon-link'
    context = IProposal
    #processsecurity_validation = seeideas_processsecurity_validation
    #roles_validation = seeideas_roles_validation
    state_validation = seeideas_state_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def withdraw_roles_validation(process, context):
    return has_role(role=('Member',))


def withdraw_processsecurity_validation(process, context):
    user = get_current()
    wg = context.working_group
    return wg and\
           user in wg.wating_list and \
           global_user_processsecurity()


def withdraw_state_validation(process, context):
    return 'amendable' in context.state


class Withdraw(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'wg-action'
    style_order = 3
    style_css_class = 'btn-warning'
    isSequential = False
    context = IProposal
    roles_validation = withdraw_roles_validation
    processsecurity_validation = withdraw_processsecurity_validation
    state_validation = withdraw_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current(request)
        working_group = context.working_group
        working_group.delfromproperty('wating_list', user)
        if getattr(user, 'email', ''):
            root = getSite()
            mail_template = root.get_mail_template('withdeaw')
            subject = mail_template['subject'].format(
                subject_title=context.title)
            email_data = get_user_data(user, 'recipient', request)
            email_data.update(get_entity_data(context, 'subject', request))
            message = mail_template['template'].format(
                novaideo_title=request.root.title,
                **email_data
            )
            alert('email', [root.get_site_sender()], [user.email],
                  subject=subject, body=message)

        request.registry.notify(ActivityExecuted(
            self, [context, working_group], user))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def resign_roles_validation(process, context):
    user = get_current()
    working_group = context.working_group
    return working_group and user in working_group.members


def resign_processsecurity_validation(process, context):
    return global_user_processsecurity()


def resign_state_validation(process, context):
    return any(s in context.state for s in
               ['amendable', 'open to a working group'])


class Resign(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'wg-action'
    style_interaction = 'ajax-action'
    style_order = 2
    style_picto = 'typcn typcn-user-delete'
    style_css_class = 'btn-danger'
    submission_title = _('Continue')
    isSequential = False
    context = IProposal
    roles_validation = resign_roles_validation
    processsecurity_validation = resign_processsecurity_validation
    state_validation = resign_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        exclude_participant_from_wg(context, request, user, root)
        request.registry.notify(ActivityExecuted(
            self, [context, context.working_group], user))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def participate_roles_validation(process, context):
    user = get_current()
    working_group = context.working_group
    return working_group and has_role(role=('Member',)) and \
        user not in working_group.members


def participate_processsecurity_validation(process, context):
    working_group = context.working_group
    user = get_current()
    root = getSite()
    wgs = getattr(user, 'active_working_groups', [])
    return working_group and \
       user not in working_group.wating_list and \
       len(wgs) < root.participations_maxi and \
       global_user_processsecurity()


def participate_state_validation(process, context):
    working_group = context.working_group
    return working_group and \
        not('closed' in working_group.state) and \
        any(s in context.state for s in
            ['amendable', 'open to a working group'])


class Participate(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'wg-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'direct'
    style_order = 1
    style_picto = 'typcn typcn-user-add'
    style_css_class = 'btn-success'
    submission_title = _('Save')
    isSequential = False
    context = IProposal
    roles_validation = participate_roles_validation
    processsecurity_validation = participate_processsecurity_validation
    state_validation = participate_state_validation

    def _send_mail_to_user(self, subject_template,
                           message_template, user,
                           context, request):
        subject = subject_template.format(subject_title=context.title)
        email_data = get_user_data(user, 'recipient', request)
        email_data.update(get_entity_data(context, 'subject', request))
        message = message_template.format(
            novaideo_title=request.root.title,
            **email_data
        )
        alert('email', [request.root.get_site_sender()], [user.email],
              subject=subject, body=message)

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current(request)
        working_group = context.working_group
        participants = working_group.members
        mode = getattr(working_group, 'work_mode', root.get_default_work_mode())
        len_participants = len(participants)
        if len_participants < mode.participants_maxi:
            #Alert new participant
            if participants:
                alert('internal', [root], participants,
                      internal_kind=InternalAlertKind.working_group_alert,
                      subjects=[context], alert_kind='participate')

            working_group.addtoproperty('members', user)
            grant_roles(user, (('Participant', context),))
            #alert maw working groups
            active_wgs = getattr(user, 'active_working_groups', [])
            if len(active_wgs) == root.participations_maxi:
                alert('internal', [root], [user],
                      internal_kind=InternalAlertKind.working_group_alert,
                      subjects=[user], alert_kind='participations_maxi')

            if (len_participants+1) == mode.participants_mini:
                working_group.state = PersistentList(['active'])
                context.state = PersistentList(['amendable', 'published'])
                working_group.reindex()
                context.reindex()
                #Only if is the first improvement cycle
                if not hasattr(working_group, 'first_improvement_cycle'):
                    working_group.first_improvement_cycle = True
                    if not working_group.improvement_cycle_proc:
                        improvement_cycle_proc = start_improvement_cycle(
                            context)
                        working_group.setproperty(
                            'improvement_cycle_proc', improvement_cycle_proc)

                    #Run the improvement cycle proc
                    working_group.improvement_cycle_proc.execute_action(
                        context, request, 'votingpublication', {})

                #Alert start of the improvement cycle proc
                alert('internal', [root], participants,
                      internal_kind=InternalAlertKind.working_group_alert,
                      subjects=[context], alert_kind='amendable')
                # Add Nia comment
                alert_comment_nia(
                    context, request, root,
                    internal_kind=InternalAlertKind.working_group_alert,
                    subject_type='proposal',
                    alert_kind='start_work',
                    duplication=context
                    )

            #Send Mail alert to user
            if getattr(user, 'email', ''):
                mail_template = root.get_mail_template('wg_participation')
                self._send_mail_to_user(
                    mail_template['subject'], mail_template['template'],
                    user, context, request)
        else:
            working_group.addtoproperty('wating_list', user)
            working_group.reindex()
            users = list(participants)
            users.append(user)
            alert('internal', [root], users,
                  internal_kind=InternalAlertKind.working_group_alert,
                  subjects=[context], alert_kind='wg_participation_max')

            if getattr(user, 'email', ''):
                mail_template = root.get_mail_template('wating_list')
                self._send_mail_to_user(
                    mail_template['subject'], mail_template['template'],
                    user, context, request)

        request.registry.notify(ActivityExecuted(
            self, [context, working_group], user))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def compare_processsecurity_validation(process, context):
    return getattr(context, 'version', None) is not None and \
           (has_role(role=('Owner', context)) or \
           (has_role(role=('Member',)) and\
            'draft' not in context.state)) and \
           global_user_processsecurity()


class CompareProposal(InfiniteCardinality):
    title = _('Compare')
    context = IProposal
    processsecurity_validation = compare_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def attach_roles_validation(process, context):
    return has_role(role=('Participant', context))


def attach_processsecurity_validation(process, context):
    return global_user_processsecurity()


def attach_state_validation(process, context):
    wg = context.working_group
    return wg and 'active' in wg.state and 'amendable' in context.state


class AttachFiles(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-paperclip'
    style_order = 3
    submission_title = _('Save')
    context = IProposal
    roles_validation = attach_roles_validation
    processsecurity_validation = attach_processsecurity_validation
    state_validation = attach_state_validation

    def start(self, context, request, appstruct, **kw):
        add_attached_files({'add_files': appstruct}, context)
        context.reindex()
        request.registry.notify(ActivityExecuted(
            self, [context], get_current(request)))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def get_access_key(obj):
    if 'draft' not in obj.state:
        challenge = getattr(obj, 'challenge', None)
        is_restricted = getattr(challenge, 'is_restricted', False)
        if is_restricted:
            return serialize_roles(
                (('ChallengeParticipant', challenge),
                 'SiteAdmin', 'Admin', 'Moderator'))

        return ['always']
    else:
        return serialize_roles(
            (('Owner', obj), 'SiteAdmin', 'Admin', 'Moderator'))


def seeproposal_processsecurity_validation(process, context):
    challenge = getattr(context, 'challenge', None)
    is_restricted = getattr(challenge, 'is_restricted', False)
    can_access = True
    if is_restricted:
        can_access = has_role(role=('ChallengeParticipant', challenge))

    return can_access and access_user_processsecurity(process, context) and \
           ('draft' not in context.state or \
            has_any_roles(roles=(('Owner', context), 'SiteAdmin', 'Moderator')))


@access_action(access_key=get_access_key)
class SeeProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'access-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'sidebar'
    style_picto = 'glyphicon glyphicon-eye-open'
    title = _('Details')
    context = IProposal
    actionType = ActionType.automatic
    processsecurity_validation = seeproposal_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#*************************** ProposalImprovementCycle process **********************************#


def decision_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def decision_roles_validation(process, context):
    return has_role(role=('SiteAdmin',))


def decision_state_validation(process, context):
    wg = context.working_group
    return wg and 'active' in wg.state and \
           'amendable' in context.state


class VotingPublication(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_order = 5
    context = IProposal
    processs_relation_id = 'proposal'
    #actionType = ActionType.system
    relation_validation = decision_relation_validation
    roles_validation = decision_roles_validation
    state_validation = decision_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove(context.state[0])
        context.state.insert(0, 'votes for publishing')
        context.reindex()
        working_group = context.working_group
        duration = getattr(working_group, 'work_duration', None)
        working_group.inc_iteration()
        if duration and duration >= datetime.timedelta(weeks=1):
            working_group.inc_nonproductive_cycle()

        if not getattr(working_group, 'first_vote', True):
            members = working_group.members
            root = getSite()
            alert('internal', [root], members,
                  internal_kind=InternalAlertKind.working_group_alert,
                  subjects=[context], alert_kind='end_work')
            mail_template = root.get_mail_template('start_vote_publishing')
            subject = mail_template['subject'].format(
                subject_title=context.title)
            subject_data = get_entity_data(context, 'subject', request)
            for member in members:
                if getattr(member, 'email', ''):
                    email_data = get_user_data(member, 'recipient', request)
                    email_data.update(subject_data)
                    message = mail_template['template'].format(
                        novaideo_title=root.title,
                        **email_data
                    )
                    alert('email', [root.get_site_sender()], [member.email],
                          subject=subject, body=message)

        request.registry.notify(ActivityExecuted(
            self, [context], get_current(request)))
        return {}

    def after_execution(self, context, request, **kw):
        process = self.process
        proposal = process.execution_context.created_entity(
            'proposal')
        if self.sub_process:
            exec_ctx = self.sub_process.execution_context
            vote_processes = exec_ctx.get_involved_collection('vote_processes')
            opened_vote_processes = [proc for proc in vote_processes
                                     if not proc._finished]
            if opened_vote_processes:
                close_votes(proposal, request, opened_vote_processes)

        setattr(process, 'new_cycle_date', datetime.datetime.now())
        setattr(process, 'previous_alert', -1)
        super(VotingPublication, self).after_execution(proposal, request, **kw)
        is_published = publish_condition(process)
        proposal.working_group.work_duration = calculate_improvement_cycle_duration(
            process)
        if is_published:
            process.execute_action(proposal, request, 'submit', {})
        else:
            process.execute_action(proposal, request, 'work', {})

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def work_state_validation(process, context):
    return 'active' in getattr(context.working_group, 'state', []) and \
           'votes for publishing' in context.state


class Work(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_order = 5
    context = IProposal
    processs_relation_id = 'proposal'
    #actionType = ActionType.system
    relation_validation = decision_relation_validation
    roles_validation = decision_roles_validation
    state_validation = work_state_validation

    def _send_mails(self, context, request, subject_template, message_template):
        working_group = context.working_group
        duration = to_localized_time(
            calculate_improvement_cycle_date(self.process),
            translate=True)
        isclosed = 'closed' in working_group.state
        members = working_group.members
        subject = subject_template.format(subject_title=context.title)
        localizer = request.localizer
        root = request.root
        alert('internal', [root], members,
              internal_kind=InternalAlertKind.working_group_alert,
              subjects=[context], alert_kind='start_work')
        subject_data = get_entity_data(context, 'subject', request)
        for member in [m for m in members if getattr(m, 'email', '')]:
            email_data = get_user_data(member, 'recipient', request)
            email_data.update(subject_data)
            message = message_template.format(
                duration=duration,
                isclosed=localizer.translate(
                    (isclosed and _('closed')) or _('open')),
                novaideo_title=root.title,
                **email_data
            )
            alert('email', [root.get_site_sender()], [member.email],
                  subject=subject, body=message)

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        working_group = context.working_group
        context.state.remove('votes for publishing')
        #Only for amendments work mode
        reopening_ballot = getattr(
            working_group, 'reopening_configuration_ballot', None)
        if reopening_ballot is not None:
            report = reopening_ballot.report
            voters_len = len(report.voters)
            electors_len = len(report.electors)
            report.calculate_votes()
            #absolute majority
            if (voters_len == electors_len) and \
               (report.result['False'] == 0) and \
               'closed' in working_group.state:
                working_group.state.remove('closed')

        context.state.insert(0, 'amendable')
        #The first improvement cycle is started
        if working_group.first_improvement_cycle:
            mail_template = root.get_mail_template('first_start_work')
            self._send_mails(
                context, request,
                mail_template['subject'], mail_template['template'])
            working_group.first_improvement_cycle = False
        else:
            mail_template = root.get_mail_template('start_work')
            self._send_mails(
                context, request,
                mail_template['subject'], mail_template['template'])

        context.reindex()
        working_group.reindex()
        request.registry.notify(ActivityExecuted(
            self, [context, working_group], get_current(request)))
        return {}

    def after_execution(self, context, request, **kw):
        proposal = self.process.execution_context.created_entity('proposal')
        super(Work, self).after_execution(proposal, request, **kw)
        working_group = proposal.working_group
        root = request.root
        nonproductive_cycle = root.get_nonproductive_cycle_nb()
        if getattr(working_group, 'nonproductive_cycle', 1) >= nonproductive_cycle:
            end_work(proposal, request)
            proposal.state = PersistentList(
                ['open to a working group', 'published'])
            members = working_group.members
            working_group.empty(False)
            working_group.state = PersistentList(['deactivated'])
            proposal.reindex()
            working_group.reindex()
            alert(
                'internal', [request.root], members,
                internal_kind=InternalAlertKind.moderation_alert,
                subjects=[proposal], alert_kind='object_closed')
            mail_template = root.get_mail_template('close_proposal')
            subject_data = get_entity_data(proposal, 'subject', request)
            subject = mail_template['subject'].format(
                **subject_data)
            for member in [m for m in members if getattr(m, 'email', '')]:
                email_data = get_user_data(member, 'recipient', request)
                email_data.update(subject_data)
                message = mail_template['template'].format(
                    novaideo_title=root.title,
                    **email_data
                )
                alert('email', [root.get_site_sender()], [member.email],
                      subject=subject, body=message)
        else:
            self.process.execute_action(proposal, request, 'votingpublication', {})

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def submit_roles_validation(process, context):
    return has_role(role=('SiteAdmin',))


def submit_state_validation(process, context):
    wg = context.working_group
    return wg and 'active' in context.working_group.state and \
           'votes for publishing' in context.state


class SubmitProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-certificate'
    style_order = 2
    context = IProposal
    processs_relation_id = 'proposal'
    #actionType = ActionType.system
    relation_validation = decision_relation_validation
    roles_validation = submit_roles_validation
    state_validation = submit_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        working_group = context.working_group
        if root.support_proposals:
            context.state = PersistentList(['submitted_support', 'published'])
            # Add Nia comment
            alert_comment_nia(
                context, request, root,
                internal_kind=InternalAlertKind.working_group_alert,
                subject_type='proposal',
                alert_kind='submitted_support',
                duplication=context
                )
        else:
            context.state = PersistentList(['published', 'submitted_support'])

        working_group.state = PersistentList(['archived'])
        working_group.setproperty('wating_list', [])
        members = working_group.members
        for member in members:
            token = Token(title='Token_'+context.title)
            token.setproperty('proposal', context)
            member.addtoproperty('tokens_ref', token)
            member.addtoproperty('tokens', token)
            token.setproperty('owner', member)
            revoke_roles(member, (('Participant', context),))

        #Alert users
        users = list(get_users_by_preferences(context))
        users.extend(members)
        users = set(users)
        alert('internal', [root], users,
              internal_kind=InternalAlertKind.working_group_alert,
              subjects=[context], alert_kind='submit_proposal')
        mail_template = root.get_mail_template('publish_proposal')
        subject = mail_template['subject'].format(
            subject_title=context.title)
        subject_data = get_entity_data(context, 'subject', request)
        for member in [m for m in users if getattr(m, 'email', '')]:
            email_data = get_user_data(member, 'recipient', request)
            email_data.update(subject_data)
            message = mail_template['template'].format(
                novaideo_title=root.title,
                **email_data
            )
            alert('email', [root.get_site_sender()], [member.email],
                  subject=subject, body=message)

        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        working_group.reindex()
        context.reindex()
        request.registry.notify(ActivityExecuted(
            self, [context, working_group], get_current(request)))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def alert_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def alert_roles_validation(process, context):
    return has_role(role=('System',))


class AlertEnd(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 4
    context = IProposal
    actionType = ActionType.system
    processs_relation_id = 'proposal'
    roles_validation = alert_roles_validation
    relation_validation = alert_relation_validation

    def start(self, context, request, appstruct, **kw):
        working_group = context.working_group
        previous_alert = getattr(self.process, 'previous_alert', -1)
        setattr(self.process, 'previous_alert', previous_alert + 1)
        if 'active' in working_group.state and 'amendable' in context.state:
            members = working_group.members
            root = request.root
            alert('internal', [root], members,
                  internal_kind=InternalAlertKind.working_group_alert,
                  subjects=[context], alert_kind='alert_end_work')
            mail_template = root.get_mail_template('alert_end')
            subject = mail_template['subject'].format(
                subject_title=context.title)
            subject_data = get_entity_data(context, 'subject', request)
            for member in [m for m in members if getattr(m, 'email', '')]:
                email_data = get_user_data(member, 'recipient', request)
                email_data.update(subject_data)
                message = mail_template['template'].format(
                    novaideo_title=root.title,
                    **email_data
                )
                alert('email', [root.get_site_sender()], [member.email],
                      subject=subject, body=message)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#**********************************************Workspace***************************************************


def get_access_key_ws(obj):
    return serialize_roles(
        (('Participant', obj.proposal), 'SiteAdmin', 'Admin'))


def seeworkspace_processsecurity_validation(process, context):
    return has_any_roles(
        roles=(('Participant', context.proposal), 'SiteAdmin'))


@access_action(access_key=get_access_key_ws)
class SeeWorkspace(InfiniteCardinality):
    title = _('Details')
    context = IWorkspace
    actionType = ActionType.automatic
    processsecurity_validation = seeworkspace_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def addfiles_state_validation(process, context):
    wg = context.working_group
    return wg and 'active' in wg.state and 'amendable' in context.proposal.state


class AddFiles(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-import'
    style_order = 4
    submission_title = _('Save')
    context = IWorkspace
    roles_validation = seeworkspace_processsecurity_validation
    processsecurity_validation = attach_processsecurity_validation
    state_validation = addfiles_state_validation

    def start(self, context, request, appstruct, **kw):
        add_files_to_workspace(appstruct.get('files', []), context)
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def rmfile_relation_validation(process, context):
    parent = context.__parent__
    return isinstance(parent, Workspace)


def rmfile_roles_validation(process, context):
    workspace = context.__parent__
    return has_any_roles(
        roles=(('Participant', workspace.proposal), 'SiteAdmin'))


def rmfile_state_validation(process, context):
    workspace = context.__parent__
    wg = workspace.working_group
    return wg and 'active' in wg.state and \
        'amendable' in workspace.proposal.state


class RemoveFile(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'primary-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_order = 2
    submission_title = _('Continue')
    context = IFile
    roles_validation = rmfile_roles_validation
    processsecurity_validation = attach_processsecurity_validation
    state_validation = rmfile_state_validation
    relation_validation = rmfile_relation_validation

    def start(self, context, request, appstruct, **kw):
        workspace = context.__parent__
        if context in workspace.files:
            workspace.delfromproperty('files', context)

        return {'newcontext': workspace}

    def redirect(self, context, request, **kw):
        return nothing


#TODO behaviors

VALIDATOR_BY_CONTEXT[Proposal] = {
    'action': CommentProposal,
    'see': SeeProposal,
    'access_key': get_access_key
}
