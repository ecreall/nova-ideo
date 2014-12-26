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
from bs4 import BeautifulSoup
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_registry
from pyramid import renderers
from substanced.util import get_oid

from dace.util import (
    getSite,
    copy,
    get_obj)
from dace.objectofcollaboration.principal.util import (
    has_role, 
    grant_roles, 
    get_current, 
    revoke_roles)
#from dace.objectofcollaboration import system
from dace.processinstance.activity import (
    InfiniteCardinality, ElementaryAction, ActionType)
from daceui.interfaces import IDaceUIAPI

from novaideo.ips.mailer import mailer_send
from novaideo.content.interface import (
    INovaIdeoApplication, 
    IProposal, 
    ICorrection, 
    Iidea)
from ..user_management.behaviors import global_user_processsecurity
from novaideo.mail import (
    ALERT_SUBJECT,
    ALERT_MESSAGE,
    RESULT_VOTE_AMENDMENT_SUBJECT,
    RESULT_VOTE_AMENDMENT_MESSAGE,
    PUBLISHPROPOSAL_SUBJECT,
    PUBLISHPROPOSAL_MESSAGE,
    VOTINGPUBLICATION_SUBJECT,
    VOTINGPUBLICATION_MESSAGE,
    VOTINGAMENDMENTS_SUBJECT,
    VOTINGAMENDMENTS_MESSAGE,
    WITHDRAW_SUBJECT,
    WITHDRAW_MESSAGE,
    PARTICIPATE_SUBJECT,
    PARTICIPATE_MESSAGE,
    RESIGN_SUBJECT,
    RESIGN_MESSAGE,
    WATINGLIST_SUBJECT,
    WATINGLIST_MESSAGE,
    AMENDABLE_SUBJECT,
    AMENDABLE_MESSAGE,
    PROOFREADING_SUBJECT,
    PROOFREADING_MESSAGE,
    ALERTOPINION_SUBJECT,
    ALERTOPINION_MESSAGE,
    PROPOSALREMOVED_SUBJECT,
    PROPOSALREMOVED_MESSAGE)

from novaideo import _
from novaideo.content.proposal import Proposal
from ..comment_management.behaviors import VALIDATOR_BY_CONTEXT
from novaideo.content.correlation import CorrelationType
from novaideo.content.token import Token
from novaideo.content.amendment import Amendment
from novaideo.content.working_group import WorkingGroup
from novaideo.content.processes.idea_management.behaviors import (
    PresentIdea, 
    CommentIdea,
    Associate as AssociateIdea)
from novaideo.utilities.text_analyzer import ITextAnalyzer, normalize_text
from novaideo.utilities.util import connect, disconnect
from novaideo.core import to_localized_time
from novaideo.event import ObjectPublished, CorrelableRemoved


try:
    basestring
except NameError:
    basestring = str


def close_votes(context, request, vote_processes):
    vote_actions = [process.get_actions('vote') \
                    for process in vote_processes]
    vote_actions = [action for actions in vote_actions \
                   for action in actions]
    for action in vote_actions:
        action.close_vote(context, request)


AMENDMENTS_CYCLE_DEFAULT_DURATION = {
              "Three minutes": datetime.timedelta(minutes=3),
              "Five minutes": datetime.timedelta(minutes=5),
              "Ten minutes": datetime.timedelta(minutes=10),
              "Twenty minutes": datetime.timedelta(minutes=20),
              "One hour": datetime.timedelta(hours=1),
              "Four hours": datetime.timedelta(hours=4),
              "One day": datetime.timedelta(days=1),
              "Three days": datetime.timedelta(days=3),
              "One week": datetime.timedelta(weeks=1),
              "Two weeks": datetime.timedelta(weeks=2)}


def calculate_amendments_cycle_duration(process):
    duration_ballot = getattr(process, 'duration_configuration_ballot', None)
    if duration_ballot is not None:
        electeds = duration_ballot.report.get_electeds()
        if electeds:
            return AMENDMENTS_CYCLE_DEFAULT_DURATION[electeds[0]] + \
                   datetime.datetime.today()

    return AMENDMENTS_CYCLE_DEFAULT_DURATION["One week"] + \
           datetime.datetime.today()


DEFAULT_NB_CORRECTORS = 1

def createproposal_roles_validation(process, context):
    return has_role(role=('Member',))


def createproposal_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def include_ideas_texts(proposal, related_ideas):
    proposal.text = getattr(proposal, 'text', '') +\
                    ''.join(['<div>' + idea.text + '</div>' \
                             for idea in related_ideas])

class CreateProposal(ElementaryAction):
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = createproposal_roles_validation
    processsecurity_validation = createproposal_processsecurity_validation


    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        keywords_ids = appstruct.pop('keywords')
        related_ideas = appstruct.pop('related_ideas')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nkw in newkeywords:
            root.addtoproperty('keywords', nkw)

        result.extend(newkeywords)
        proposal = appstruct['_object_data']
        proposal.text = normalize_text(proposal.text)
        root.addtoproperty('proposals', proposal)
        proposal.setproperty('keywords_ref', result)
        proposal.state.append('draft')
        grant_roles(roles=(('Owner', proposal), ))
        grant_roles(roles=(('Participant', proposal), ))
        proposal.setproperty('author', user)
        self.process.execution_context.add_created_entity('proposal', proposal)
        wg = WorkingGroup()
        root.addtoproperty('working_groups', wg)
        wg.setproperty('proposal', proposal)
        wg.addtoproperty('members', get_current())
        wg.state.append('deactivated')
        if related_ideas:
            connect(proposal, 
                    related_ideas,
                    {'comment': _('Add related ideas'),
                     'type': _('Creation')},
                    user,
                    ['related_proposals', 'related_ideas'],
                    CorrelationType.solid)

        proposal.reindex()
        wg.reindex()
        return {'newcontext': proposal}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))
        

def pap_processsecurity_validation(process, context):
    return (('published' in context.state) and has_role(role=('Member',)))


class PublishAsProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    context = Iidea
    submission_title = _('Save')
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-file'
    processsecurity_validation = pap_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        proposal = Proposal()
        proposal.title = appstruct['title']
        proposal.description = appstruct['description']
        root.addtoproperty('proposals', proposal)
        for k in context.keywords_ref:
            proposal.addtoproperty('keywords_ref', k)

        proposal.text = normalize_text(context.text)
        proposal.state.append('draft')
        grant_roles(roles=(('Owner', proposal), ))
        grant_roles(roles=(('Participant', proposal), ))
        proposal.setproperty('author', user)
        self.process.execution_context.add_created_entity('proposal', proposal)
        wg = WorkingGroup()
        root.addtoproperty('working_groups', wg)
        wg.setproperty('proposal', proposal)
        wg.addtoproperty('members', user)
        wg.state.append('deactivated')
        connect(proposal,
                [context],
                {'comment': _('Transform the idea as a proposal'),
                 'type': _('Creation')},
                user,
                ['related_proposals', 'related_ideas'],
                CorrelationType.solid)
        proposal.reindex()
        wg.reindex()
        context.reindex()
        return {'newcontext': proposal}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def del_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def del_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           ((has_role(role=('Owner', context)) and \
           'draft' in context.state) or \
           has_role(role=('Moderator', )))


class DeleteProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_order = 0
    submission_title = _('Continue')
    context = IProposal
    processs_relation_id = 'proposal'
    relation_validation = del_relation_validation
    processsecurity_validation = del_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        explanation = appstruct['explanation']
        root = getSite()
        tokens = [t for t in context.tokens if not t.proposal]
        for token in list(tokens):
            token.owner.addtoproperty('tokens', token)
        wg = context.working_group
        members = list(wg.members)
        for member in members:
            wg.delfromproperty('members', member)

        wg.delfromproperty('proposal', context)
        root.delfromproperty('working_groups', wg)
        request.registry.notify(CorrelableRemoved(object=context))
        root.delfromproperty('proposals', context)
        subject = PROPOSALREMOVED_SUBJECT.format(subject_title=context.title)
        localizer = request.localizer
        for member in members:
            message = PROPOSALREMOVED_MESSAGE.format(
                recipient_title=localizer.translate(_(getattr(member, 
                                                    'user_title',''))),
                recipient_first_name=getattr(member, 'first_name', member.name),
                recipient_last_name=getattr(member, 'last_name',''),
                subject_title=context.title,
                explanation=explanation,
                novaideo_title=request.root.title
                 )
            mailer_send(subject=subject, 
                recipients=[member.email], 
                body=message)
        return {'newcontext': root}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], ""))

def submit_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def submit_roles_validation(process, context):
    return has_role(role=('Owner', context))


def submit_processsecurity_validation(process, context):
    user = get_current()
    root = getSite()
    return len(user.active_working_groups) < root.participations_maxi and \
           global_user_processsecurity(process, context)
          

def submit_state_validation(process, context):
    return "draft" in context.state


class SubmitProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 1
    submission_title = _('Continue')
    context = IProposal
    processs_relation_id = 'proposal'
    relation_validation = submit_relation_validation
    roles_validation = submit_roles_validation
    processsecurity_validation = submit_processsecurity_validation
    state_validation = submit_state_validation


    def start(self, context, request, appstruct, **kw):
        context.state.remove('draft')
        root = getSite()
        if root.participants_mini > 1:
            context.state.append('open to a working group')
        else:
            context.state.append('votes for publishing')

        for idea in [i for i in context.related_ideas.keys() \
                     if not('published' in i.state)]:
            idea.state = PersistentList(['published'])
            idea.reindex()

        context.reindex()
        request.registry.notify(ObjectPublished(object=context))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def duplicate_processsecurity_validation(process, context):
    return not ('draft' in context.state) and \
           global_user_processsecurity(process, context)


class DuplicateProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-resize-full'
    style_order = 3
    submission_title = _('Save')
    context = IProposal
    processsecurity_validation = duplicate_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        copy_of_proposal = copy(context, (root, 'proposals'), 
                             omit=('created_at', 'modified_at',
                                   'explanation', 'opinion'))
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nkw in newkeywords:
            root.addtoproperty('keywords', nkw)

        result.extend(newkeywords)
        related_ideas = appstruct.pop('related_ideas')
        appstruct['keywords_ref'] = result
        copy_of_proposal.set_data(appstruct)
        copy_of_proposal.text = normalize_text(copy_of_proposal.text)
        copy_of_proposal.setproperty('originalentity', context)
        copy_of_proposal.state = PersistentList(['draft'])
        grant_roles(roles=(('Owner', copy_of_proposal), ))
        grant_roles(roles=(('Participant', copy_of_proposal), ))
        copy_of_proposal.setproperty('author', user)
        self.process.execution_context.add_created_entity(
                                       'proposal', copy_of_proposal)
        wg = WorkingGroup()
        root.addtoproperty('working_groups', wg)
        wg.setproperty('proposal', copy_of_proposal)
        wg.addtoproperty('members', get_current())
        wg.state.append('deactivated')
        if related_ideas:
            connect(copy_of_proposal, 
                    related_ideas,
                    {'comment': _('Add related ideas'),
                     'type': _('Duplicate')},
                    user,
                    ['related_proposals', 'related_ideas'],
                    CorrelationType.solid)

        wg.reindex()
        copy_of_proposal.reindex()
        context.reindex()
        return {'newcontext': copy_of_proposal}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def edit_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def edit_roles_validation(process, context):
    return has_role(role=('Owner', context))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def edit_state_validation(process, context):
    return "draft" in context.state


class EditProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    submission_title = _('Save')
    context = IProposal
    processs_relation_id = 'proposal'
    relation_validation = edit_relation_validation
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation


    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current
        if 'related_ideas' in appstruct:
            relatedideas = appstruct['related_ideas']
            current_related_ideas = list(context.related_ideas.keys())
            related_ideas_to_add = [i for i in relatedideas \
                                    if not(i in current_related_ideas)]
            related_ideas_to_del = [i for i in current_related_ideas \
                                     if not(i in relatedideas) and \
                                        not (i in related_ideas_to_add)]
            connect(context,
                    related_ideas_to_add,
                    {'comment': _('Add related ideas'),
                     'type': _('Edit the proposal')},
                    user,
                    ['related_proposals', 'related_ideas'],
                    CorrelationType.solid,
                    True)
            disconnect(context, 
                       related_ideas_to_del,
                       'related_ideas',
                       CorrelationType.solid)

        context.text = normalize_text(context.text)
        context.modified_at = datetime.datetime.today()
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nkw in newkeywords:
            root.addtoproperty('keywords', nkw)

        result.extend(newkeywords)
        datas = {'keywords_ref': result}
        context.set_data(datas)
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def proofreading_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def proofreading_roles_validation(process, context):
    return has_role(role=('Participant', context))


def proofreading_processsecurity_validation(process, context):
    correction_in_process = any(('in process' in c.state \
                                 for c in context.corrections))
    return not correction_in_process and \
           not getattr(process, 'first_decision', True) and \
           global_user_processsecurity(process, context)


def proofreading_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'proofreading' in context.state


class ProofreadingDone(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_picto = 'glyphicon glyphicon-ok'
    style_descriminator = 'text-action'
    style_order = 2
    context = IProposal
    processs_relation_id = 'proposal'
    roles_validation = proofreading_roles_validation
    relation_validation = proofreading_relation_validation
    processsecurity_validation = proofreading_processsecurity_validation
    state_validation = proofreading_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('proofreading')
        context.state.append('amendable')
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def pub_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def pub_roles_validation(process, context):
    return has_role(role=('System',))


def pub_state_validation(process, context):
    return 'active' in context.working_group.state and 'votes for publishing' in context.state


class PublishProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-certificate'
    style_order = 2
    context = IProposal
    processs_relation_id = 'proposal'
    actionType = ActionType.system
    roles_validation = pub_roles_validation
    relation_validation = pub_relation_validation
    state_validation = pub_state_validation

    def start(self, context, request, appstruct, **kw):
        wg = context.working_group
        context.state.remove('votes for publishing')
        context.state.append('published')
        wg.state = PersistentList(['archived'])
        members = wg.members
        url = request.resource_url(context, "@@index")
        subject = PUBLISHPROPOSAL_SUBJECT.format(subject_title=context.title)
        localizer = request.localizer
        for member in  members:
            token = Token(title='Token_'+context.title)
            token.setproperty('proposal', context)
            member.addtoproperty('tokens_ref', token)
            member.addtoproperty('tokens', token)
            token.setproperty('owner', member)
            revoke_roles(member, (('Participant', context),))
            message = PUBLISHPROPOSAL_MESSAGE.format(
                recipient_title=localizer.translate(_(getattr(member, 'user_title',''))),
                recipient_first_name=getattr(member, 'first_name', member.name),
                recipient_last_name=getattr(member, 'last_name',''),
                subject_title=context.title,
                subject_url=url,
                novaideo_title=request.root.title
                 )
            mailer_send(subject=subject,
              recipients=[member.email],
              body=message)

        wg.reindex()
        context.reindex()
        #TODO wg desactive, members vide...
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def support_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def support_roles_validation(process, context):
    return has_role(role=('Member',))


def support_processsecurity_validation(process, context):
    user = get_current()
    return user.tokens and  \
           not (user in [t.owner for t in context.tokens]) and \
           global_user_processsecurity(process, context)


def support_state_validation(process, context):
    return 'published' in context.state


class SupportProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-thumbs-up'
    style_order = 2
    context = IProposal
    processs_relation_id = 'proposal'
    roles_validation = support_roles_validation
    relation_validation = support_relation_validation
    processsecurity_validation = support_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        token = None
        for tok in user.tokens:
            if tok.proposal is context:
                token = tok

        if token is None:
            token = user.tokens[-1]

        context.addtoproperty('tokens_support', token)
        context._support_history.append((get_oid(user), datetime.datetime.today(), 1))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class OpposeProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-thumbs-down'
    style_order = 3
    context = IProposal
    processs_relation_id = 'proposal'
    roles_validation = support_roles_validation
    relation_validation = support_relation_validation
    processsecurity_validation = support_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        token = None
        for tok in user.tokens:
            if tok.proposal is context:
                token = tok

        if token is None:
            token = user.tokens[-1]

        context.addtoproperty('tokens_opposition', token)
        context._support_history.append((get_oid(user), datetime.datetime.today(), 0))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def opinion_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def opinion_roles_validation(process, context):
    return has_role(role=('Moderator',))


def opinion_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def opinion_state_validation(process, context):
    return 'published' in context.state or \
           ('examined' in context.state and \
             context.opinion == 'Indifferent')


class MakeOpinion(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    submission_title = _('Save')
    context = IProposal
    processs_relation_id = 'proposal'
    relation_validation = opinion_relation_validation
    roles_validation = opinion_roles_validation
    processsecurity_validation = opinion_processsecurity_validation
    state_validation = opinion_state_validation

    def start(self, context, request, appstruct, **kw):
        context.opinion = appstruct['opinion']
        context.explanation = appstruct['explanation']
        if 'published' in context.state:
            context.state.remove('published')
            context.state.append('examined')

        context.reindex()
        tokens = [t for t in context.tokens if not t.proposal]
        proposal_tokens = [t for t in context.tokens if t.proposal]
        for token in list(tokens):
            token.owner.addtoproperty('tokens', token)

        for token in list(proposal_tokens):
            context.__delitem__(token.__name__)

        members = context.working_group.members
        url = request.resource_url(context, "@@index")
        subject = ALERTOPINION_SUBJECT.format(subject_title=context.title)
        localizer = request.localizer
        for member in members:
            message = ALERTOPINION_MESSAGE.format(
                recipient_title=localizer.translate(_(getattr(member, 
                                                    'user_title',''))),
                recipient_first_name=getattr(member, 'first_name', member.name),
                recipient_last_name=getattr(member, 'last_name',''),
                subject_url=url,
                subject_title=context.title,
                opinion=localizer.translate(_(context.opinion)),
                explanation=context.explanation,
                novaideo_title=request.root.title
                 )
            mailer_send(subject=subject, 
                recipients=[member.email], 
                body=message)
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def withdrawt_processsecurity_validation(process, context):
    user = get_current()
    return any((t.owner is user) and \
                t.proposal is None for t in context.tokens) and \
           global_user_processsecurity(process, context)


class WithdrawToken(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-share-alt'
    style_order = 2
    context = IProposal
    processs_relation_id = 'proposal'
    roles_validation = support_roles_validation
    relation_validation = support_relation_validation
    processsecurity_validation = withdrawt_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        user_tokens = [t for t in context.tokens \
                       if (t.owner is user) and t.proposal is None]
        token = user_tokens[-1]
        context.delfromproperty(token.__property__, token)
        user.addtoproperty('tokens', token)
        context._support_history.append((get_oid(user), datetime.datetime.today(), -1))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def alert_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def alert_roles_validation(process, context):
    return has_role(role=('System',))


def alert_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and any(s in context.state \
                                        for s in ['proofreading', 'amendable'])


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
        subject = ALERT_SUBJECT.format(subject_title=context.title)
        localizer = request.localizer
        for member in members:
            message = ALERT_MESSAGE.format(
                recipient_title=localizer.translate(_(getattr(member, 
                                                    'user_title',''))),
                recipient_first_name=getattr(member, 'first_name', member.name),
                recipient_last_name=getattr(member, 'last_name',''),
                subject_url=url,
                subject_title=context.title,
                novaideo_title=request.root.title
                 )
            mailer_send(subject=subject, 
                recipients=[member.email], 
                body=message)

        return {}

    def after_execution(self, context, request, **kw):
        super(Alert, self).after_execution(context, request, **kw)
        self.process.execute_action(context, request, 'votingpublication', {})

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def comm_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def comm_roles_validation(process, context):
    return has_role(role=('Member',))


def comm_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def comm_state_validation(process, context):
    return  not('draft' in context.state)


class CommentProposal(CommentIdea):
    isSequential = False
    context = IProposal
    processs_relation_id = 'proposal'
    roles_validation = comm_roles_validation
    processsecurity_validation = comm_processsecurity_validation
    state_validation = comm_state_validation


def seea_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def seea_roles_validation(process, context):
    return has_role(role=('Participant', context))


def seea_processsecurity_validation(process, context):
    return any(not('archived' in a.state) for a in context.amendments) and \
          global_user_processsecurity(process, context)


class SeeAmendments(InfiniteCardinality):
    isSequential = False
    context = IProposal
    processs_relation_id = 'proposal'
    relation_validation = seea_relation_validation
    roles_validation = seea_roles_validation
    processsecurity_validation = seea_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def present_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def present_roles_validation(process, context):
    return has_role(role=('Member',))


def present_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def present_state_validation(process, context):
    return not ('draft' in context.state) #TODO ?


class PresentProposal(PresentIdea):
    context = IProposal
    processs_relation_id = 'proposal'
    roles_validation = present_roles_validation
    processsecurity_validation = present_processsecurity_validation
    state_validation = present_state_validation


def associate_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def associate_processsecurity_validation(process, context):
    return (has_role(role=('Owner', context)) or \
           (has_role(role=('Member',)) and \
            not ('draft' in context.state))) and \
           global_user_processsecurity(process, context)


class Associate(AssociateIdea):
    context = IProposal
    processs_relation_id = 'proposal'
    processsecurity_validation = associate_processsecurity_validation
    relation_validation = associate_relation_validation


def seeideas_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def seeideas_state_validation(process, context):
    return not ('draft' in context.state) or \
           ('draft' in context.state and has_role(role=('Owner', context))) 


class SeeRelatedIdeas(InfiniteCardinality):
    context = IProposal
    processs_relation_id = 'proposal'
    #processsecurity_validation = seeideas_processsecurity_validation
    #roles_validation = seeideas_roles_validation
    state_validation = seeideas_state_validation
    relation_validation = seeideas_relation_validation

    def start(self, context, request, appstruct, **kw):
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
    return 'active' in wg.state and 'amendable' in context.state


class ImproveProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-edit'
    style_order = 4
    submission_title = _('Save')
    isSequential = False
    context = IProposal
    processs_relation_id = 'proposal'
    relation_validation = improve_relation_validation
    roles_validation = improve_roles_validation
    processsecurity_validation = improve_processsecurity_validation
    state_validation = improve_state_validation


    def start(self, context, request, appstruct, **kw):
        root = getSite()
        data = {}
        localizer = request.localizer
        data['title'] = context.title + \
                       localizer.translate(_('_Amended version ')) + \
                        str(getattr(context, '_amendments_counter', 1))
        data['text'] = normalize_text(appstruct['text'])
        data['description'] = appstruct['description']
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nkw in newkeywords:
            root.addtoproperty('keywords', nkw)

        result.extend(newkeywords)
        data['keywords_ref'] = result
        amendment = Amendment()
        amendment.set_data(data)
        context.addtoproperty('amendments', amendment)
        amendment.state.append('draft')
        grant_roles(roles=(('Owner', amendment), ))
        amendment.setproperty('author', get_current())
        amendment.reindex()
        context._amendments_counter = getattr(context, '_amendments_counter', 1) + 1
        return {'newcontext': amendment}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def correctitem_relation_validation(process, context):
    return process.execution_context.has_relation(context.proposal, 'proposal')


def correctitem_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal))


def correctitem_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def correctitem_state_validation(process, context):
    return 'active' in context.proposal.working_group.state and \
           'proofreading' in context.proposal.state


class CorrectItem(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = True
    context = ICorrection
    relation_validation = correctitem_relation_validation
    roles_validation = correctitem_roles_validation
    processsecurity_validation = correctitem_processsecurity_validation
    state_validation = correctitem_state_validation

    def _include_to_proposal(self, context, text_to_correct, request, content):
        corrections = [item for item in context.corrections.keys() \
                       if not('included' in context.corrections[item])]
        text = self._include_items(text_to_correct, request, corrections)
        if content == 'description':
            text = text.replace('<p>', '').replace('</p>', '')

        setattr(context.proposal, content, text)

    def _include_items(self, text, request, items, to_add=False):
        text_analyzer = get_current_registry().getUtility(ITextAnalyzer,
                                                          'text_analyzer')
        todel = "ins"
        toins = "del"
        if to_add:
            todel = "del"
            toins = "ins"

        soup = BeautifulSoup(text)
        corrections = []
        for item in items:
            corrections.extend(soup.find_all('span', {'id':'correction', 
                                                      'data-item': item}))

        blocstodel = ('span', {'id':'correction_actions'})
        soup = text_analyzer.include_diffs(soup, corrections,
                        todel, toins, blocstodel)
        return text_analyzer.soup_to_text(soup)

    def _include_vote(self, context, request, item, content, vote, user_oid):
        text_to_correct = getattr(context, content, '')
        context.corrections[item][vote].append(user_oid)
        len_vote = len(context.corrections[item][vote])
        vote_bool = False
        if vote == 'favour':
            len_vote -= 1
            vote_bool = True

        if len_vote >= \
            DEFAULT_NB_CORRECTORS:
            text = self._include_items(text_to_correct, 
                           request, [item], vote_bool)
            setattr(context, content, text)
            text_to_correct = getattr(context, content,'')
            context.corrections[item]['included'] = True
            if not any(not('included' in context.corrections[c]) \
                       for c in context.corrections.keys()):
                context.state.remove('in process')
                context.state.append('processed')

            self._include_to_proposal(context, text_to_correct, 
                                      request, content)

    def start(self, context, request, appstruct, **kw):
        item = appstruct['item']
        content = appstruct['content']
        vote = (appstruct['vote'].lower() == 'true')
        user = get_current()
        user_oid = get_oid(user)
        correction_data = context.corrections[item]
        if not(user_oid in correction_data['favour']) and \
               not(user_oid in correction_data['against']):
            if vote:
                self._include_vote(context, request, 
                                   item, content,
                                   'favour', user_oid)
            else:
                self._include_vote(context, request, 
                                   item, content,
                                   'against', user_oid)
            
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def correct_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def correct_roles_validation(process, context):
    return has_role(role=('Participant', context))


def correct_processsecurity_validation(process, context):
    correction_in_process = any(('in process' in c.state \
                                 for c in context.corrections))
    return not correction_in_process and \
           not getattr(process, 'first_decision', True) and \
           global_user_processsecurity(process, context)


def correct_state_validation(process, context):
    return 'active' in context.working_group.state and\
           'proofreading' in context.state


class CorrectProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-check'
    style_order = 2
    submission_title = _('Save')
    correction_item_template = 'novaideo:views/proposal_management/templates/correction_item.pt'
    isSequential = True
    context = IProposal
    processs_relation_id = 'proposal'
    relation_validation = correct_relation_validation
    roles_validation = correct_roles_validation
    processsecurity_validation = correct_processsecurity_validation
    state_validation = correct_state_validation

    def _add_vote_actions(self, tag, correction, request):
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,
                                                        'dace_ui_api')
        if not hasattr(self, '_correctitemaction'):
            correctitemnode = self.process['correctitem']
            correctitem_wis = [wi for wi in correctitemnode.workitems \
                               if wi.node is correctitemnode]
            if correctitem_wis:
                self._correctitemaction = correctitem_wis[0].actions[0]

        if hasattr(self, '_correctitemaction'):
            actionurl_update = dace_ui_api.updateaction_viewurl(
                               request=request, 
                               action_uid=str(get_oid(self._correctitemaction)), 
                               context_uid=str(get_oid(correction)))
            values = {'favour_action_url': actionurl_update,
                     'against_action_url': actionurl_update}
            body = renderers.render(
                             self.correction_item_template, values, request)
            correction_item_soup = BeautifulSoup(body)
            tag.append(correction_item_soup.body)
            tag.body.unwrap()

    def _add_actions(self, correction, request, soup):
        corrections_tags = soup.find_all('span', {'id':'correction'})
        for correction_tag in corrections_tags:
            self._add_vote_actions(correction_tag, correction, request)

    def _identify_corrections(self, soup, correction, descriminator, content):
        correction_tags = soup.find_all('span', {'id': "correction"})
        correction_oid = str(get_oid(correction))
        user = get_current()
        user_oid = get_oid(user)
        for correction_tag in correction_tags:
            correction_tag['data-correction'] = correction_oid
            correction_tag['data-item'] = str(descriminator)
            correction_tag['data-content'] = content
            init_vote = {'favour':[user_oid], 'against':[]}
            correction.corrections[str(descriminator)] = init_vote
            descriminator += 1

        return descriminator      

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        correction = appstruct['_object_data']
        correction.setproperty('author', user)
        context.addtoproperty('corrections', correction)
        text_analyzer = get_current_registry().getUtility(
                                                ITextAnalyzer,
                                                'text_analyzer')
        souptextdiff, textdiff = text_analyzer.render_html_diff(
                                       getattr(context, 'text', ''), 
                                       getattr(correction, 'text', ''),
                                       "correction")
        soupdescriptiondiff, descriptiondiff = text_analyzer.render_html_diff(
                                        getattr(context, 'description', ''), 
                                        getattr(correction, 'description', ''), 
                                        "correction")
        descriminator = 0
        descriminator = self._identify_corrections(soupdescriptiondiff, 
                                                   correction, 
                                                   descriminator, 
                                                   'description')
        self._add_actions(correction, request, soupdescriptiondiff)
        self._identify_corrections(souptextdiff, correction, 
                                   descriminator, 'text')
        self._add_actions(correction, request, souptextdiff)
        correction.text = text_analyzer.soup_to_text(souptextdiff)
        context.originaltext = correction.text
        correction.description = text_analyzer.soup_to_text(soupdescriptiondiff)
        if souptextdiff.find_all("span", id="correction") or \
           soupdescriptiondiff.find_all("span", id="correction"):
            correction.state.append('in process')

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def addp_state_validation(process, context):
    return False


class AddParagraph(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_order = 3
    isSequential = False
    context = IProposal
    processs_relation_id = 'proposal'
    relation_validation = correct_relation_validation
    roles_validation = correct_roles_validation
    processsecurity_validation = correct_processsecurity_validation
    state_validation = addp_state_validation#correct_state_validation

    def start(self, context, request, appstruct, **kw):
        #TODO
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def decision_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def decision_roles_validation(process, context):
    return has_role(role=('Admin',))


def decision_state_validation(process, context):
    return 'active' in context.working_group.state and \
           any(s in context.state for s in ['proofreading', 'amendable'])


class VotingPublication(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 5
    context = IProposal
    processs_relation_id = 'proposal'
    #actionType = ActionType.system
    relation_validation = decision_relation_validation
    roles_validation = decision_roles_validation
    state_validation = decision_state_validation

    def start(self, context, request, appstruct, **kw):
        state = context.state[0] 
        context.state.remove(state)
        context.state.append('votes for publishing')
        context.reindex()
        members = context.working_group.members
        url = request.resource_url(context, "@@index")
        subject = VOTINGPUBLICATION_SUBJECT.format(subject_title=context.title)
        localizer = request.localizer
        for member in members:
            message = VOTINGPUBLICATION_MESSAGE.format(
                recipient_title=localizer.translate(_(getattr(member, 'user_title',''))),
                recipient_first_name=getattr(member, 'first_name', member.name),
                recipient_last_name=getattr(member, 'last_name',''),
                subject_title=context.title,
                subject_url=url,
                novaideo_title=request.root.title
                 )
            mailer_send(subject=subject, 
                recipients=[member.email], 
                body=message)

        self.process.iteration = getattr(self.process, 'iteration', 0) + 1
        return {}

    def after_execution(self, context, request, **kw):
        exec_ctx = self.sub_process.execution_context
        vote_processes = exec_ctx.get_involved_collection('vote_processes')
        vote_processes = [process for process in vote_processes \
                          if not process._finished]
        if vote_processes:
            close_votes(context, request, vote_processes)

        super(VotingPublication, self).after_execution(context, request, **kw)

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def withdraw_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def withdraw_roles_validation(process, context):
    return has_role(role=('Member',))


def withdraw_processsecurity_validation(process, context):
    user = get_current()
    return user in context.working_group.wating_list and \
           global_user_processsecurity(process, context)


def withdraw_state_validation(process, context):
    return  any(s in context.state for s in ['proofreading', 'amendable'])


class Withdraw(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'wg-action'
    style_order = 3
    style_css_class = 'btn-warning'
    isSequential = False
    context = IProposal
    processs_relation_id = 'proposal'
    relation_validation = withdraw_relation_validation
    roles_validation = withdraw_roles_validation
    processsecurity_validation = withdraw_processsecurity_validation
    state_validation = withdraw_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        wg = context.working_group
        wg.delfromproperty('wating_list', user)
        localizer = request.localizer
        subject = WITHDRAW_SUBJECT.format(subject_title=context.title)
        message = WITHDRAW_MESSAGE.format(
                recipient_title=localizer.translate(_(getattr(user, 'user_title',''))),
                recipient_first_name=getattr(user, 'first_name', user.name),
                recipient_last_name=getattr(user, 'last_name',''),
                subject_title=context.title,
                subject_url=request.resource_url(context, "@@index"),
                novaideo_title=request.root.title
                 )
        mailer_send(subject=subject, 
            recipients=[user.email], 
            body=message)
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def resign_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def resign_roles_validation(process, context):
    return has_role(role=('Participant', context))


def resign_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def resign_state_validation(process, context):
    return  any(s in context.state for s in \
                ['proofreading', 'amendable', 'open to a working group'])


class Resign(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'wg-action'
    style_order = 2
    style_css_class = 'btn-danger'
    isSequential = False
    context = IProposal
    processs_relation_id = 'proposal'
    relation_validation = resign_relation_validation
    roles_validation = resign_roles_validation
    processsecurity_validation = resign_processsecurity_validation
    state_validation = resign_state_validation

    def _get_next_user(self, users, root):
        for user in users:
            wgs = user.active_working_groups
            if 'active' in user.state and len(wgs) < root.participations_maxi:
                return user

        return None 

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        wg = context.working_group
        wg.delfromproperty('members', user)
        revoke_roles(user, (('Participant', context),))
        url = request.resource_url(context, "@@index")
        localizer = request.localizer
        if wg.wating_list:
            next_user = self._get_next_user(wg.wating_list, root)
            if next_user is not None:
                wg.delfromproperty('wating_list', next_user)
                wg.addtoproperty('members', next_user)
                grant_roles(next_user, (('Participant', context),))
                subject = PARTICIPATE_SUBJECT.format(subject_title=context.title)
                message = PARTICIPATE_MESSAGE.format(
                        recipient_title=localizer.translate(_(getattr(next_user, 'user_title',''))),
                        recipient_first_name=getattr(next_user, 
                                               'first_name', next_user.name),
                        recipient_last_name=getattr(next_user, 'last_name',''),
                        subject_title=context.title,
                        subject_url=url,
                        novaideo_title=request.root.title
                 )
                mailer_send(subject=subject, 
                    recipients=[next_user.email], 
                    body=message)

        participants = wg.members
        len_participants = len(participants)
        if len_participants < root.participants_mini and \
            not ('open to a working group' in context.state):
            context.state = PersistentList(['open to a working group'])
            wg.state = PersistentList(['deactivated'])
            wg.reindex()
            context.reindex()

        subject = RESIGN_SUBJECT.format(subject_title=context.title)
        message = RESIGN_MESSAGE.format(
                recipient_title=localizer.translate(_(getattr(user, 'user_title',''))),
                recipient_first_name=getattr(user, 'first_name', user.name),
                recipient_last_name=getattr(user, 'last_name',''),
                subject_title=context.title,
                subject_url=url,
                novaideo_title=request.root.title
                 )
        mailer_send(subject=subject, 
             recipients=[user.email], 
             body=message)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def participate_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def participate_roles_validation(process, context):
    return has_role(role=('Member',)) and not has_role(role=('Participant', context))


def participate_processsecurity_validation(process, context):
    user = get_current()
    root = getSite()
    wgs = user.active_working_groups
    return not(user in context.working_group.wating_list) and \
           len(wgs) < root.participations_maxi and \
           global_user_processsecurity(process, context)


def participate_state_validation(process, context):
    wg = context.working_group
    return  not('closed' in wg.state) and \
            any(s in context.state for s in \
                ['proofreading', 'amendable', 'open to a working group']) 


class Participate(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'wg-action'
    style_order = 1
    style_css_class = 'btn-success'
    isSequential = False
    context = IProposal
    processs_relation_id = 'proposal'
    relation_validation = participate_relation_validation
    roles_validation = participate_roles_validation
    processsecurity_validation = participate_processsecurity_validation
    state_validation = participate_state_validation

    def _send_mail_to_user(self, subject_template, message_template, user, context, request):
        localizer = request.localizer
        subject = subject_template.format(subject_title=context.title)
        message = message_template.format(
                recipient_title=localizer.translate(_(getattr(user, 'user_title',''))),
                recipient_first_name=getattr(user, 'first_name', user.name),
                recipient_last_name=getattr(user, 'last_name',''),
                subject_title=context.title,
                subject_url=request.resource_url(context, "@@index"),
                novaideo_title=request.root.title
                 )
        mailer_send(subject=subject, recipients=[user.email], body=message)

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        wg = context.working_group
        participants = wg.members
        len_participants = len(participants)
        first_decision = False
        if len_participants < root.participants_maxi:
            wg.addtoproperty('members', user)
            grant_roles(user, (('Participant', context),))
            if (len_participants+1) == root.participants_mini:
                context.state = PersistentList()
                wg.state = PersistentList(['active'])
                if not hasattr(self.process, 'first_decision'):
                    self.process.first_decision = True
                    first_decision = True

                if any(not('archived' in a.state) for a in context.amendments):
                    context.state.append('amendable')
                else:
                    context.state.append('proofreading')

                wg.reindex()
                context.reindex()

            self._send_mail_to_user(PARTICIPATE_SUBJECT, PARTICIPATE_MESSAGE,
                                    user, context, request)
            if first_decision:
                self.process.execute_action(
                       context, request, 'votingpublication', {})
        else:
            wg.addtoproperty('wating_list', user)
            wg.reindex()
            self._send_mail_to_user(WATINGLIST_SUBJECT, WATINGLIST_MESSAGE,
                 user, context, request)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


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
        subject = VOTINGAMENDMENTS_SUBJECT.format(subject_title=context.title)
        for member in members:
            message = VOTINGAMENDMENTS_MESSAGE.format(
                recipient_title=localizer.translate(_(getattr(member, 'user_title',''))),
                recipient_first_name=getattr(member, 'first_name', member.name),
                recipient_last_name=getattr(member, 'last_name',''),
                subject_title=context.title,
                subject_url=url,
                novaideo_title=request.root.title
                 )
            mailer_send(subject=subject, 
                 recipients=[member.email], 
                 body=message)

        return {}

    def after_execution(self, context, request, **kw):
        proposal = self.process.execution_context.involved_entity('proposal')
        exec_ctx = self.sub_process.execution_context
        vote_processes = exec_ctx.get_involved_collection('vote_processes')
        vote_processes = [process for process in vote_processes \
                          if not process._finished]
        if vote_processes:
            close_votes(context, request, vote_processes)

        super(VotingAmendments, self).after_execution(proposal, request, **kw)
        self.process.execute_action(
                  proposal, request, 'amendmentsresult', {})

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


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
    roles_validation = decision_roles_validation
    state_validation = ar_state_validation

    def _get_newversion(self, context, root, wg):
        contextname = context.__name__
        copy_of_proposal = copy(context, 
                                (root, 'proposals'), 
                                new_name=context.__name__,
                                omit=('created_at','modified_at'),
                                roles=True)
        copy_keywords, newkeywords = root.get_keywords(context.keywords)
        copy_of_proposal.setproperty('keywords_ref', copy_keywords)
        copy_of_proposal.setproperty('version', context)
        copy_of_proposal.setproperty('originalentity', context.originalentity)
        root.rename(copy_of_proposal.__name__, contextname)
        copy_of_proposal.state = PersistentList(['proofreading'])
        copy_of_proposal.setproperty('author', context.author)
        copy_of_proposal.setproperty('comments', context.comments)
        self.process.execution_context.add_created_entity('proposal', 
                                                          copy_of_proposal)
        wg.setproperty('proposal', copy_of_proposal)
        return copy_of_proposal

    def _send_ballot_result(self, context, request, electeds, members):
        group_nb = 0
        amendments_vote_result = []
        for ballot in self.process.amendments_ballots: 
            group_nb += 1
            judgments = ballot.report.ballottype.judgments
            sorted_judgments = sorted(list(judgments.keys()), 
                                key=lambda o: judgments[o])
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
        subject = RESULT_VOTE_AMENDMENT_SUBJECT.format(
                        subject_title=context.title)
        for member in members:
            message = RESULT_VOTE_AMENDMENT_MESSAGE.format(
                recipient_title=localizer.translate(_(getattr(member, 'user_title',''))),
                recipient_first_name=getattr(member, 'first_name', member.name),
                recipient_last_name=getattr(member, 'last_name',''),
                message_result=result_body,
                novaideo_title=request.root.title
                 )
            mailer_send(subject=subject, 
                 recipients=[member.email], 
                 html=message)
        
    def start(self, context, request, appstruct, **kw):
        result = set()
        for ballot in self.process.amendments_ballots:
            electeds = ballot.report.get_electeds()
            if electeds is not None:
                result.update(electeds)

        amendments = [a for a in result if isinstance(a, Amendment)]
        wg = context.working_group
        root = getSite()
        user = get_current()
        newcontext = context 
        if amendments:
            text_analyzer = get_current_registry().getUtility(
                                            ITextAnalyzer,'text_analyzer')
            merged_text = text_analyzer.merge(context.text, 
                                 [a.text for a in amendments])
            merged_text = normalize_text(merged_text)
            #TODO merged_keywords + merged_description
            copy_of_proposal = self._get_newversion(context, root, wg)
            self._send_ballot_result(copy_of_proposal, request, 
                                     result, wg.members)
            context.state = PersistentList(['archived'])
            copy_of_proposal.text = merged_text
            #correlation idea of replacement ideas... del replaced_idea
            related_ideas = [a.related_ideas for a in amendments]
            related_ideas = [item for sublist in related_ideas \
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
        else:
            context.state = PersistentList(['proofreading'])
            for amendment in context.amendments:
                amendment.state = PersistentList(['archived'])
                amendment.reindex()

        context.reindex()
        return {'newcontext': newcontext}

    def after_execution(self, context, request, **kw):
        super(AmendmentsResult, self).after_execution(context, request, **kw)
        self.process.execute_action(kw['newcontext'], request, 'votingpublication', {})

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def ta_state_validation(process, context):
    return 'active' in context.working_group.state and \
           'votes for publishing' in context.state


class Amendable(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 8
    context = IProposal
    processs_relation_id = 'proposal'
    actionType = ActionType.system
    relation_validation = va_relation_validation
    roles_validation = va_roles_validation
    state_validation = ta_state_validation

    def _send_mails(self, context, request, subject_template, message_template):
        working_group = context.working_group
        duration = to_localized_time(
                     calculate_amendments_cycle_duration(self.process))
        isclosed = 'closed' in working_group.state
        members = working_group.members
        url = request.resource_url(context, "@@index")
        subject = subject_template.format(subject_title=context.title)
        localizer = request.localizer
        for member in members:
            message = message_template.format(
                recipient_title=localizer.translate(_(getattr(member, 
                                                            'user_title',''))),
                recipient_first_name=getattr(member, 'first_name', member.name),
                recipient_last_name=getattr(member, 'last_name',''),
                subject_title=context.title,
                subject_url=url,
                duration=duration,
                isclosed=localizer.translate((isclosed and _('closed')) or\
                                             _('open')),
                novaideo_title=request.root.title
                 )
            mailer_send(subject=subject, 
                recipients=[member.email], 
                body=message)

    def start(self, context, request, appstruct, **kw):
        context.state.remove('votes for publishing')
        wg = context.working_group
        if self.process.first_decision:
            self.process.first_decision = False

        reopening_ballot = getattr(self.process, 
                            'reopening_configuration_ballot', None)
        if reopening_ballot is not None:
            report = reopening_ballot.report
            voters_len = len(report.voters)
            electors_len = len(report.electors)
            report.calculate_votes()
            #absolute majority
            if (voters_len == electors_len) and \
               (report.result['False'] == 0) and \
               'closed' in wg.state:
                wg.state.remove('closed')
                wg.reindex()

        if any(not('archived' in a.state) for a in context.amendments):
            context.state.append('amendable')
            self._send_mails(context, request, 
                             AMENDABLE_SUBJECT, AMENDABLE_MESSAGE)

        else:
            context.state.append('proofreading')
            self._send_mails(context, request,
                             PROOFREADING_SUBJECT, PROOFREADING_MESSAGE)

        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def compare_processsecurity_validation(process, context):
    return getattr(context, 'version', None) is not None and \
           (has_role(role=('Owner', context)) or \
           (has_role(role=('Member',)) and\
            not ('draft' in context.state))) and \
           global_user_processsecurity(process, context)


class CompareProposal(InfiniteCardinality):
    title = _('Compare')
    context = IProposal
    relation_validation = associate_relation_validation
    processsecurity_validation = compare_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#TODO behaviors

VALIDATOR_BY_CONTEXT[Proposal] = CommentProposal
