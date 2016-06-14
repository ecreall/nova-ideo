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
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_registry
from pyramid import renderers

import html_diff_wrapper
from dace.util import (
    getSite,
    copy,
    get_obj)
from dace.objectofcollaboration.principal.util import (
    has_role,
    grant_roles,
    get_current)
#from dace.objectofcollaboration import system
from dace.processinstance.activity import (
    InfiniteCardinality, ElementaryAction, ActionType)

from novaideo.content.interface import IProposal
from ...user_management.behaviors import global_user_processsecurity
from novaideo import _
from novaideo.content.correlation import CorrelationType
from novaideo.content.amendment import Amendment
from novaideo.content.processes.amendment_management.behaviors import (
    get_text_amendment_diff)
from novaideo.utilities.util import connect
from novaideo.content.alert import InternalAlertKind
from novaideo.utilities.alerts_utility import alert

try:
    basestring
except NameError:
    basestring = str


VOTE_AMENDMENTS_MESSAGE = _("Vote for amendments")


AMENDMENTS_VOTE_DEFAULT_DURATION = datetime.timedelta(days=1)


def close_votes(context, request, vote_processes):
    vote_actions = [process.get_actions('vote')
                    for process in vote_processes]
    vote_actions = [action for actions in vote_actions
                    for action in actions]
    for action in vote_actions:
        action.close_vote(context, request)


def alert_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def alert_roles_validation(process, context):
    return has_role(role=('System',))


def alert_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'amendable' in context.state


class Alert(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 4
    context = IProposal
    actionType = ActionType.system
    processs_relation_id = 'proposal'
    roles_validation = alert_roles_validation
    relation_validation = alert_relation_validation
    state_validation = alert_state_validation

    def start(self, context, request, appstruct, **kw):
        members = context.working_group.members
        url = request.resource_url(context, "@@index")
        root = request.root
        mail_template = root.get_mail_template('alert_amendment')
        subject = mail_template['subject'].format(subject_title=context.title)
        localizer = request.localizer
        alert('internal', [root], members,
              internal_kind=InternalAlertKind.working_group_alert,
              subjects=[context], alert_kind='no_amendment')
        for member in members:
            if getattr(member, 'email', ''):
                message = mail_template['template'].format(
                    recipient_title=localizer.translate(
                        _(getattr(member, 'user_title', ''))),
                    recipient_first_name=getattr(
                        member, 'first_name', member.name),
                    recipient_last_name=getattr(
                        member, 'last_name', ''),
                    subject_url=url,
                    subject_title=context.title,
                    novaideo_title=request.root.title
                )
                alert('email', [root.get_site_sender()], [member.email],
                      subject=subject, body=message)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def improve_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def improve_roles_validation(process, context):
    return has_role(role=('Participant', context))


def improve_processsecurity_validation(process, context):
    #correction_in_process = any(('in process' in c.state for c in context.corrections))
    return global_user_processsecurity(process, context)


def improve_state_validation(process, context):
    wg = context.working_group
    return wg and 'active' in wg.state and 'amendable' in context.state


class ImproveProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-edit'
    style_order = 3
    submission_title = _('Save')
    isSequential = False
    context = IProposal
    processs_relation_id = 'proposal'
    relation_validation = improve_relation_validation
    roles_validation = improve_roles_validation
    processsecurity_validation = improve_processsecurity_validation
    state_validation = improve_state_validation

    def start(self, context, request, appstruct, **kw):
        data = {}
        localizer = request.localizer
        data['title'] = localizer.translate(_('Amended version ')) + \
                        str(getattr(context, '_amendments_counter', 1))
        data['text'] = html_diff_wrapper.normalize_text(appstruct['text'])
        # data['description'] = appstruct['description']
        # data['keywords'] = appstruct['keywords']
        amendment = Amendment()
        amendment.set_data(data)
        context.addtoproperty('amendments', amendment)
        amendment.state.append('draft')
        grant_roles(roles=(('Owner', amendment), ))
        amendment.setproperty('author', get_current())
        amendment.text_diff = get_text_amendment_diff(
                                context, amendment)
        amendment.reindex()
        context._amendments_counter = getattr(context, '_amendments_counter', 1) + 1
        return {'newcontext': amendment}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def va_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def va_roles_validation(process, context):
    return has_role(role=('System',))


def va_state_validation(process, context):
    return 'active' in context.working_group.state and \
           'amendable' in context.state


class VotingAmendments(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 6
    context = IProposal
    processs_relation_id = 'proposal'
    actionType = ActionType.system
    relation_validation = va_relation_validation
    roles_validation = va_roles_validation
    state_validation = va_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state = PersistentList(['votes for amendments'])
        wg = context.working_group
        if 'closed' not in wg.state:
            wg.state.append('closed')

        context.reindex()
        members = wg.members
        url = request.resource_url(context, "@@index")
        localizer = request.localizer
        root = request.root
        mail_template = root.get_mail_template('start_vote_amendments')
        subject = mail_template['subject'].format(subject_title=context.title)
        alert('internal', [root], members,
              internal_kind=InternalAlertKind.working_group_alert,
              subjects=[context])
        for member in members:
            if getattr(member, 'email', ''):
                message = mail_template['template'].format(
                    recipient_title=localizer.translate(
                        _(getattr(member, 'user_title', ''))),
                    recipient_first_name=getattr(
                        member, 'first_name', member.name),
                    recipient_last_name=getattr(
                        member, 'last_name', ''),
                    subject_title=context.title,
                    subject_url=url,
                    novaideo_title=root.title
                )
                alert('email', [root.get_site_sender()], [member.email],
                      subject=subject, body=message)

        return {}

    def after_execution(self, context, request, **kw):
        proposal = self.process.execution_context.involved_entity('proposal')
        exec_ctx = self.sub_process.execution_context
        vote_processes = exec_ctx.get_involved_collection('vote_processes')
        vote_processes = [process for process in vote_processes
                          if not process._finished]
        if vote_processes:
            close_votes(context, request, vote_processes)

        super(VotingAmendments, self).after_execution(proposal, request, **kw)
        self.process.execute_action(
            proposal, request, 'amendmentsresult', {})

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def ar_roles_validation(process, context):
    return has_role(role=('Admin',))


def ar_state_validation(process, context):
    return 'active' in context.working_group.state and \
           'votes for amendments' in context.state


class AmendmentsResult(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 7
    amendments_group_result_template = 'novaideo:views/proposal_management/templates/amendments_group_result.pt'
    amendments_vote_result_template = 'novaideo:views/proposal_management/templates/amendments_vote_result.pt'
    context = IProposal
    processs_relation_id = 'proposal'
    relation_validation = va_relation_validation
    roles_validation = ar_roles_validation
    state_validation = ar_state_validation

    def _get_newversion(self, context, root, working_group):
        contextname = context.__name__
        copy_of_proposal = copy(context,
                                (root, 'proposals'),
                                new_name=context.__name__,
                                omit=('created_at', 'modified_at'),
                                roles=True)
        copy_of_proposal.keywords = context.keywords
        copy_of_proposal.setproperty('version', context)
        copy_of_proposal.setproperty('originalentity', context.originalentity)
        root.rename(copy_of_proposal.__name__, contextname)
        copy_of_proposal.state = PersistentList(['amendable', 'published'])
        copy_of_proposal.setproperty('author', context.author)
        copy_of_proposal.setproperty('comments', context.comments)
        self.process.attachedTo.process.execution_context.add_created_entity(
            'proposal', copy_of_proposal)
        working_group.setproperty('proposal', copy_of_proposal)
        return copy_of_proposal

    def _send_ballot_result(self, context, request, electeds, members):
        amendments_vote_result = []
        working_group = context.working_group
        for group_nb, ballot in enumerate(working_group.amendments_ballots):
            judgments = ballot.report.ballottype.judgments
            sorted_judgments = sorted(
                list(judgments.keys()), key=lambda o: judgments[o])
            values = {'group_nb': group_nb,
                      'report': ballot.report,
                      'sorted_judgments': sorted_judgments,
                      'get_obj': get_obj}
            group_body = renderers.render(
                self.amendments_group_result_template, values, request)
            amendments_vote_result.append(group_body)

        values = {'amendments_vote_result': amendments_vote_result,
                  'electeds': electeds,
                  'subject': context}
        result_body = renderers.render(
            self.amendments_vote_result_template, values, request)
        localizer = request.localizer
        root = request.root
        mail_template = root.get_mail_template('vote_amendment_result')
        subject = mail_template['subject'].format(
            subject_title=context.title)
        for member in members:
            if getattr(member, 'email', ''):
                message = mail_template['template'].format(
                    recipient_title=localizer.translate(
                        _(getattr(member, 'user_title', ''))),
                    recipient_first_name=getattr(
                        member, 'first_name', member.name),
                    recipient_last_name=getattr(
                        member, 'last_name', ''),
                    message_result=result_body,
                    novaideo_title=root.title
                )
                alert('email', [root.get_site_sender()], [member.email],
                      subject=subject, body=message)

    def start(self, context, request, appstruct, **kw):
        result = set()
        working_group = context.working_group
        for ballot in working_group.amendments_ballots:
            electeds = ballot.report.get_electeds()
            if electeds is not None:
                result.update(electeds)

        amendments = [a for a in result if isinstance(a, Amendment)]
        members = working_group.members
        root = getSite()
        user = get_current()
        newcontext = context
        if amendments:
            merged_text = html_diff_wrapper.merge(
                context.text, [a.text for a in amendments])
            merged_text = html_diff_wrapper.normalize_text(merged_text)
            #TODO merged_keywords + merged_description
            copy_of_proposal = self._get_newversion(context, root, working_group)
            self._send_ballot_result(copy_of_proposal, request,
                                     result, members)
            context.state = PersistentList(['version', 'archived'])
            copy_of_proposal.text = merged_text
            #correlation idea of replacement ideas... del replaced_idea
            related_ideas = [a.related_ideas for a in amendments]
            related_ideas = [item for sublist in related_ideas
                             for item in sublist]
            related_ideas.extend(context.related_ideas)
            related_ideas = list(set(related_ideas))
            connect(copy_of_proposal,
                    related_ideas,
                    {'comment': _('Add related ideas'),
                     'type': _('New version')},
                    user,
                    ['related_proposals', 'related_ideas'],
                    CorrelationType.solid)
            newcontext = copy_of_proposal
            copy_of_proposal.reindex()
            alert('internal', [root], members,
                  internal_kind=InternalAlertKind.working_group_alert,
                  subjects=[copy_of_proposal], alert_kind='amendments_result')
        else:
            context.state = PersistentList(['amendable', 'published'])
            alert('internal', [root], members,
                  internal_kind=InternalAlertKind.working_group_alert,
                  subjects=[context])
            for amendment in context.amendments:
                amendment.state = PersistentList(['archived'])
                amendment.reindex()

        context.reindex()
        return {'newcontext': newcontext}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


#TODO behaviors
