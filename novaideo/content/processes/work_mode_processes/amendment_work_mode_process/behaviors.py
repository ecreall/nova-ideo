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
from pyramid import renderers

import html_diff_wrapper
from dace.util import (
    getSite,
    get_obj)
from dace.objectofcollaboration.principal.util import (
    has_role,
    grant_roles,
    get_current)
from dace.processinstance.activity import (
    InfiniteCardinality, ElementaryAction, ActionType)

from novaideo.content.interface import IProposal
from ...user_management.behaviors import global_user_processsecurity
from novaideo import _
from novaideo.content.amendment import Amendment
from novaideo.content.processes.amendment_management.behaviors import (
    get_text_amendment_diff)
from novaideo.content.alert import InternalAlertKind
from novaideo.utilities.alerts_utility import (
    alert, get_user_data, get_entity_data, alert_comment_nia)
from novaideo.utilities.util import diff_analytics


VOTE_AMENDMENTS_MESSAGE = _("You are invited to vote on amendments. Each group of amendments opposes "
                            "various submitted amendments to the original text, when they bear on the same "
                            "segments of the text or on the same ideas.")

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
        #improvement_cycle TODO no improve
        members = context.working_group.members
        root = request.root
        mail_template = root.get_mail_template('alert_amendment')
        subject = mail_template['subject'].format(subject_title=context.title)
        alert('internal', [root], members,
              internal_kind=InternalAlertKind.working_group_alert,
              subjects=[context], alert_kind='no_amendment')
        subject_data = get_entity_data(context, 'subject', request)
        for member in members:
            if getattr(member, 'email', ''):
                email_data = get_user_data(member, 'recipient', request)
                email_data.update(subject_data)
                message = mail_template['template'].format(
                    novaideo_title=request.root.title,
                    **email_data
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
    return global_user_processsecurity()


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
        context._amendments_counter = getattr(
            context, '_amendments_counter', 1) + 1
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
        context.state = PersistentList(['votes for amendments', 'published'])
        wg = context.working_group
        if 'closed' not in wg.state:
            wg.state.append('closed')

        context.reindex()
        members = wg.members
        root = request.root
        mail_template = root.get_mail_template('start_vote_amendments')
        subject = mail_template['subject'].format(subject_title=context.title)
        alert('internal', [root], members,
              internal_kind=InternalAlertKind.working_group_alert,
              subjects=[context], alert_kind='voting_amendment')
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
    return has_role(role=('SiteAdmin',))


def ar_state_validation(process, context):
    working_group = context.working_group
    return working_group and 'active' in working_group.state and \
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
        root = request.root
        mail_template = root.get_mail_template('vote_amendment_result')
        subject = mail_template['subject'].format(
            subject_title=context.title)
        for member in members:
            if getattr(member, 'email', ''):
                recipientdata = get_user_data(member, 'recipient', request)
                message = mail_template['template'].format(
                    message_result=result_body,
                    novaideo_title=root.title,
                    **recipientdata
                )
                alert('email', [root.get_site_sender()], [member.email],
                      subject=subject, html=message)

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
        if amendments:
            merged_text = html_diff_wrapper.merge(
                context.text, [a.text for a in amendments])
            merged_text = html_diff_wrapper.normalize_text(merged_text)
            #TODO merged_keywords + merged_description
            version = context.get_version(
                user, (context, 'version'))
            for amendment in version.amendments:
                amendment.state = PersistentList(['archived'])
                amendment.reindex()

            self._send_ballot_result(context, request,
                                     result, members)
            context.text = merged_text
            related_ideas = [a.related_ideas for a in amendments]
            related_ideas = [item for sublist in related_ideas
                             for item in sublist]
            related_ideas.extend(context.related_ideas)
            related_ideas = list(set(related_ideas))
            context.set_related_ideas(related_ideas, user)
            context.working_group.init_nonproductive_cycle()
            context.reindex()
            alert('internal', [root], members,
                  internal_kind=InternalAlertKind.working_group_alert,
                  subjects=[context], alert_kind='amendments_result')
            # Add Nia comment
            alert_comment_nia(
                context, request, root,
                internal_kind=InternalAlertKind.working_group_alert,
                subject_type='proposal',
                alert_kind='new_version',
                diff=diff_analytics(
                    version, context, ['title', 'text', 'description'])
                )
        else:
            context.state = PersistentList(['amendable', 'published'])
            alert('internal', [root], members,
                  internal_kind=InternalAlertKind.working_group_alert,
                  subjects=[context])
            for amendment in context.amendments:
                amendment.state = PersistentList(['archived'])
                amendment.reindex()

        context.reindex()
        return {'newcontext': context}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


#TODO behaviors
