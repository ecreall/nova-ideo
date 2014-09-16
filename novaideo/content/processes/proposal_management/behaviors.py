# -*- coding: utf8 -*-
import datetime
from datetime import timedelta
import htmldiff
from bs4 import BeautifulSoup
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_request, get_current_registry
from pyramid import renderers
from substanced.util import get_oid

from dace.util import (
    getSite,
    getBusinessAction,
    copy,
    find_entities,
    get_obj)
from dace.objectofcollaboration.principal.util import has_any_roles, grant_roles, get_current, revoke_roles
from dace.processinstance.activity import InfiniteCardinality, ActionType, LimitedCardinality, ElementaryAction
from pontus.dace_ui_extension.interfaces import IDaceUIAPI

from novaideo.ips.mailer import mailer_send
from novaideo.content.interface import INovaIdeoApplication, IProposal, ICorrelableEntity, ICorrection, Iidea
from ..user_management.behaviors import global_user_processsecurity
from novaideo.mail import ALERT_SUBJECT, ALERT_MESSAGE,  RESULT_VOTE_AMENDMENT_SUBJECT,  RESULT_VOTE_AMENDMENT_MESSAGE
from novaideo import _
from novaideo.content.proposal import Proposal
from ..comment_management.behaviors import validation_by_context
from novaideo.core import acces_action
from novaideo.content.correlation import Correlation
from novaideo.content.idea import Idea
from novaideo.content.token import Token
from novaideo.content.amendment import Amendment
from novaideo.content.working_group import WorkingGroup
from novaideo.content.ballot import Ballot
from novaideo.content.processes.idea_management.behaviors import PresentIdea, Associate as AssociateIdea
from novaideo.utilities.text_analyzer import ITextAnalyzer


try:
      basestring
except NameError:
      basestring = str

default_nb_correctors = 1

def createproposal_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def createproposal_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def associate_to_proposal(related_ideas, proposal, add_idea_text=True):
    root = getSite()
    datas = {'author': get_current(),
             'source': proposal,
             'comment': '',
             'intention': 'Creation'}
    for idea in related_ideas:
        correlation = Correlation()
        datas['targets'] = [idea]
        correlation.set_data(datas)
        correlation.tags.extend(['related_proposals', 'related_ideas'])
        correlation.type = 1
        root.addtoproperty('correlations', correlation)
        if add_idea_text:
            proposal.text = getattr(proposal, 'text', '') + '<div>'+idea.text+'</div>'


class CreateProposal(ElementaryAction):
    context = INovaIdeoApplication
    roles_validation = createproposal_roles_validation
    processsecurity_validation = createproposal_processsecurity_validation


    def start(self, context, request, appstruct, **kw):
        root = getSite()
        appstruct_proposal = appstruct.pop('proposal')
        appstruct_related_ideas = appstruct.pop('related_ideas')
        keywords_ids = appstruct_proposal.pop('keywords')
        related_ideas = appstruct_related_ideas.pop('related_ideas')
        
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        proposal = appstruct_proposal['_object_data']
        root.addtoproperty('proposals', proposal)
        proposal.setproperty('keywords_ref', result)
        proposal.state.append('draft')
        grant_roles(roles=(('Owner', proposal), ))
        grant_roles(roles=(('Participant', proposal), ))
        proposal.setproperty('author', get_current())
        self.process.execution_context.add_created_entity('proposal', proposal)
        wg = WorkingGroup()
        root.addtoproperty('working_groups', wg)
        wg.setproperty('proposal', proposal)
        wg.addtoproperty('members', get_current())
        wg.state.append('deactivated')
        if related_ideas:
            associate_to_proposal(related_ideas, proposal)

        proposal.reindex()
        wg.reindex()
        self.newcontext = proposal
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(self.newcontext, "@@index"))


def pap_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context),))


def pap_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def pap_state_validation(process, context):
    return "to work" in context.state


class PublishAsProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    context = Iidea
    style_descriminator = 'global-action'
    roles_validation = pap_roles_validation
    processsecurity_validation = pap_processsecurity_validation
    state_validation = pap_state_validation

    def _associate(self, related_ideas, proposal):
        root = getSite()
        datas = {'author': get_current(),
                 'source': proposal,
                 'comment': _('Publish the idea as a proposal'),
                 'intention': 'Creation'}
        for idea in related_ideas:
            correlation = Correlation()
            datas['targets'] = [idea]
            correlation.set_data(datas)
            correlation.tags.extend(['related_proposals', 'related_ideas'])
            correlation.type = 1
            root.addtoproperty('correlations', correlation)

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        proposal = Proposal()
        root.addtoproperty('proposals', proposal)
        for k in context.keywords_ref:
            proposal.addtoproperty('keywords_ref', k)

        proposal.title = context.title
        proposal.description = context.description
        proposal.text = context.text
        proposal.state.append('draft')
        context.state = PersistentList(['published'])
        grant_roles(roles=(('Owner', proposal), ))
        grant_roles(roles=(('Participant', proposal), ))
        proposal.setproperty('author', get_current())
        self.process.execution_context.add_created_entity('proposal', proposal)
        wg = WorkingGroup()
        root.addtoproperty('working_groups', wg)
        wg.setproperty('proposal', proposal)
        wg.addtoproperty('members', get_current())
        wg.state.append('deactivated')
        self._associate([context], proposal)
        proposal.reindex()
        wg.reindex()
        context.reindex()
        self.newcontext = proposal
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(self.newcontext, "@@index"))


def submit_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def submit_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context),))


def submit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def submit_state_validation(process, context):
    return "draft" in context.state


class SubmitProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 1
    context = IProposal
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
        
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

def duplicate_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           not ('draft' in context.state)


class DuplicateProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 3
    context = IProposal
    processsecurity_validation = duplicate_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        copy_of_proposal = copy(context, (root, 'proposals'))
        #copy_of_proposal.created_at = datetime.datetime.today()
        #copy_of_proposal.modified_at = datetime.datetime.today()
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        appstruct['keywords_ref'] = result
        copy_of_proposal.set_data(appstruct)
        #root.addtoproperty('proposals', copy_of_proposal)
        copy_of_proposal.setproperty('originalentity', context)
        copy_of_proposal.state = PersistentList(['draft'])
        copy_of_proposal.setproperty('author', get_current())
        grant_roles(roles=(('Owner', copy_of_proposal), ))
        grant_roles(roles=(('Participant', copy_of_proposal), ))
        copy_of_proposal.setproperty('author', get_current())
        self.process.execution_context.add_created_entity('proposal', copy_of_proposal)
        wg = WorkingGroup()
        root.addtoproperty('working_groups', wg)
        wg.setproperty('proposal', copy_of_proposal)
        wg.addtoproperty('members', get_current())
        wg.state.append('deactivated')
        if context.related_ideas:
            associate_to_proposal(context.related_ideas, copy_of_proposal, False)

        wg.reindex()
        copy_of_proposal.reindex()
        context.reindex()
        self.newcontext = copy_of_proposal
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(self.newcontext, "@@index"))


def edit_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def edit_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context),))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def edit_state_validation(process, context):
    return "draft" in context.state


class EditProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_order = 1
    context = IProposal
    relation_validation = edit_relation_validation
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        context.modified_at = datetime.datetime.today()
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        datas = {'keywords_ref': result}
        context.set_data(datas)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

def pub_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')

def pub_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),)) #System

def pub_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'votes for publishing' in context.state


class PublishProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 2
    context = IProposal
    roles_validation = pub_roles_validation
    relation_validation = pub_relation_validation
    state_validation = pub_state_validation

    def start(self, context, request, appstruct, **kw):
        #TODO wg desactive, members vide...
        wg = context.working_group
        context.state.remove('votes for publishing')
        context.state.append('published')
        wg.state = PersistentList(['archived'])
        for member in  wg.members:
            token = Token(title='Token_'+context.title)
            token.setproperty('proposal', context)
            member.setproperty('tokens', token)
            token.setproperty('owner', member)

        wg.reindex()
        context.reindex()
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def support_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def support_roles_validation(process, context):
    return has_any_roles(roles=('Member',)) #System


def support_processsecurity_validation(process, context):
    user = get_current()
    return global_user_processsecurity(process, context) and \
           user.tokens and  \
           not (user in [t.owner for t in context.tokens])

def support_state_validation(process, context):
    return 'published' in context.state


class SupportProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 2
    context = IProposal
    roles_validation = support_roles_validation
    relation_validation = support_relation_validation
    processsecurity_validation = support_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        token = None
        for t in user.tokens:
            if t.proposal is context:
                token = t

        if token is None:
            token = user.tokens[-1]

        context.addtoproperty('tokens_support', token)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))



class OpposeProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 3
    context = IProposal
    roles_validation = support_roles_validation
    relation_validation = support_relation_validation
    processsecurity_validation = support_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        token = None
        for t in user.tokens:
            if t.proposal is context:
                token = t

        if token is None:
            token = user.tokens[-1]

        context.addtoproperty('tokens_opposition', token)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def withdrawt_processsecurity_validation(process, context):
    user = get_current()
    return global_user_processsecurity(process, context) and \
           [t for t in context.tokens if (t.owner is user) and t.proposal is None]


class WithdrawToken(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 2
    context = IProposal
    roles_validation = support_roles_validation
    relation_validation = support_relation_validation
    processsecurity_validation = withdrawt_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        user_tokens = [t for t in context.tokens if (t.owner is user) and t.proposal is None]
        token = user_tokens[-1]
        context.delproperty(token.__property__, token)
        user.addtoproperty('tokens', token)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))



def alert_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def alert_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),)) #System


def alert_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'amendable' in context.state


class Alert(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 4
    context = IProposal
    roles_validation = alert_roles_validation
    relation_validation = alert_relation_validation
    state_validation = alert_state_validation

    def start(self, context, request, appstruct, **kw):
        members = context.working_group.members
        url = request.resource_url(context, "@@index")
        subject = ALERT_SUBJECT.format(subject_title=context.title)
        for member in members:
            recipient_title = getattr(member, 'user_title','')
            recipient_first_name = getattr(member, 'first_name', member.name)
            recipient_last_name = getattr(member, 'last_name','')
            member_email = member.email
            message = ALERT_MESSAGE.format(
                recipient_title=recipient_title,
                recipient_first_name=recipient_first_name,
                recipient_last_name=recipient_last_name,
                subject_url=url
                 )
            mailer_send(subject=subject, recipients=[member_email], body=message)

        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def comm_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def comm_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def comm_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def comm_state_validation(process, context):
    return  not('draft' in context.state)


class CommentProposal(InfiniteCardinality):
    isSequential = False
    context = IProposal
    roles_validation = comm_roles_validation
    processsecurity_validation = comm_processsecurity_validation
    state_validation = comm_state_validation

    def start(self, context, request, appstruct, **kw):
        comment = appstruct['_object_data']
        context.addtoproperty('comments', comment)
        user = get_current()
        comment.setproperty('author', user)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def edita_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def edita_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def edita_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           context.amendments


class EditAmendments(InfiniteCardinality):
    isSequential = False
    context = IProposal
    relation_validation = edita_relation_validation
    roles_validation = edita_roles_validation
    processsecurity_validation = edita_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def present_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def present_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def present_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def present_state_validation(process, context):
    return not ('draft' in context.state) #TODO ?


class PresentProposal(PresentIdea):
    context = IProposal
    roles_validation = present_roles_validation
    processsecurity_validation = present_processsecurity_validation
    state_validation = present_state_validation


def associate_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def associate_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def associate_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           (has_any_roles(roles=(('Owner', context),)) or \
           (has_any_roles(roles=('Member',)) and not ('draft' in context.state)))

class Associate(AssociateIdea):
    context = IProposal
    processsecurity_validation = associate_processsecurity_validation
    roles_validation = associate_roles_validation
    relation_validation = associate_relation_validation


def addideas_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def addideas_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),)) 


def addideas_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) 


def addideas_state_validation(process, context):
    wg = context.working_group
    return ('active' in wg.state and 'amendable' in context.state) or \
           ('draft' in context.state and has_any_roles(roles=(('Owner', context),))) 


class AddIdeas(InfiniteCardinality):
    context = IProposal
    processsecurity_validation = addideas_processsecurity_validation
    roles_validation = addideas_roles_validation
    state_validation = addideas_state_validation
    relation_validation = addideas_relation_validation

    def start(self, context, request, appstruct, **kw):
        ideas = appstruct['targets']
        root = getSite()
        datas = {'author': get_current(),
                 'targets': ideas,
                 'comment': appstruct['comment'],
                 'intention': appstruct['intention'],
                 'source': context}
        correlation = Correlation()
        correlation.set_data(datas)
        correlation.tags.extend(['related_proposals', 'related_ideas'])
        correlation.type = 1
        root.addtoproperty('correlations', correlation)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def improve_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def improve_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),))


def improve_processsecurity_validation(process, context):
    correction_in_process = any(('in process' in c.state for c in context.corrections))
    return global_user_processsecurity(process, context) and not correction_in_process


def improve_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'amendable' in context.state


class ImproveProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_order = 4
    isSequential = False
    context = IProposal
    relation_validation = improve_relation_validation
    roles_validation = improve_roles_validation
    processsecurity_validation = improve_processsecurity_validation
    state_validation = improve_state_validation


    def start(self, context, request, appstruct, **kw):
        root = getSite()
        data = {}
        data['title'] = appstruct['title']
        data['text'] = appstruct['text']
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        data['keywords_ref'] = result
        data['description'] = appstruct['description']
        data['comment'] = appstruct['confirmation']['comment']
        data['intention'] = appstruct['confirmation']['intention']
        not_identified = appstruct['confirmation']['replaced_idea']['not_identified']
        new_idea = appstruct['confirmation']['idea_of_replacement']['new_idea']
        amendment = Amendment()
        self.newcontext = amendment
        if not not_identified:
            data['replaced_idea'] = appstruct['confirmation']['replaced_idea']['replaced_idea']

        if not new_idea:
            data['idea_of_replacement'] = appstruct['confirmation']['idea_of_replacement']['idea_of_replacement']
        else:
            newidea = Idea(title='Idea for '+context.title)
            root.addtoproperty('ideas', newidea)
            newidea.state.append('to work')
            grant_roles(roles=(('Owner', newidea), ))
            newidea.setproperty('author', get_current())
            data['idea_of_replacement'] = newidea
            newidea.reindex()
            self.newcontext = newidea

        amendment.set_data(data)
        context.addtoproperty('amendments', amendment)
        amendment.state.append('draft')
        grant_roles(roles=(('Owner', amendment), ))
        amendment.setproperty('author', get_current())
        return True

    def redirect(self, context, request, **kw):
        if isinstance(self.newcontext, Amendment):
            return HTTPFound(request.resource_url(context, "@@index"))
        else:
            return HTTPFound(request.resource_url(self.newcontext, "@@editidea"))


def correctitem_relation_validation(process, context):
    return process.execution_context.has_relation(context.proposal, 'proposal')


def correctitem_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context.proposal),))


def correctitem_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def correctitem_state_validation(process, context):
    wg = context.proposal.working_group
    return 'active' in wg.state and 'amendable' in context.proposal.state


def _normalize_text(soup, first=True):
    corrections = soup.find_all("span", id="correction")
    text =  str(soup.body.contents[0])
    if first:
        for correction in corrections:
            index = text.find(str(correction))
            index += str(correction).__len__()
            if text[index] == ' ':
                text = text[:index]+text[index+1:]

    return text.replace('\xa0', '')


class CorrectItem(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = True
    context = ICorrection
    relation_validation = correctitem_relation_validation
    roles_validation = correctitem_roles_validation
    processsecurity_validation = correctitem_processsecurity_validation
    state_validation = correctitem_state_validation

    def _include_to_proposal(self, context, request):
        text, in_process = self. _include_items(context, request, [item for item in context.corrections.keys() if not('included' in context.corrections[item])])
        soup = BeautifulSoup(text)
        diff_tags = soup.find_all("div", {'class': 'diff'})
        if diff_tags:
            diff_tags[0].unwrap()
          
        context.proposal.text = _normalize_text(soup, False)
                
    def _include_items(self, context, request, items, to_add=False):
        tag_type = "del"
        if to_add:
            tag_type = "ins"

        soup = BeautifulSoup(context.text)
        for item in items:
            correction_item = soup.find_all('span',{'id':'correction', 'data-item':item})[0]
            tags = correction_item.find_all(tag_type)
            if tags: 
                tag = correction_item.find_all(tag_type)[0]
                correction_item.clear()
                correction_item.replace_with(tag)
                tag.unwrap()
            else:
                correction_item.extract()

        return _normalize_text(soup, False), (len(soup.find_all("span", id="correction")) > 0)

    def start(self, context, request, appstruct, **kw):
        item = appstruct['item']
        vote = (appstruct['vote'].lower() == 'true')
        user = get_current()
        user_oid = get_oid(user)
        correction_data = context.corrections[item]
        if not(user_oid in correction_data['favour']) and not(user_oid in correction_data['against']):
            if vote:
                context.corrections[item]['favour'].append(get_oid(user))
                if (len(context.corrections[item]['favour'])-1) >= default_nb_correctors:
                    context.text, in_process = self._include_items(context, request, [item], True)
                    if not in_process:
                        context.state.remove('in process')
                        context.state.append('processed')

                    context.corrections[item]['included'] = True
                    self._include_to_proposal(context, request)
            else:
                context.corrections[item]['against'].append(get_oid(user))
                if len(context.corrections[item]['against']) >= default_nb_correctors:
                    context.text, in_process= self._include_items(context, request, [item])
                    if not in_process:
                        context.state.remove('in process')
                        context.state.append('processed')

                    context.corrections[item]['included'] = True
                    self._include_to_proposal(context, request)
            
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def correct_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def correct_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),))


def correct_processsecurity_validation(process, context):
    correction_in_process = any(('in process' in c.state for c in context.corrections))
    return global_user_processsecurity(process, context) and not correction_in_process


def correct_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'amendable' in context.state


class CorrectProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_order = 2
    isSequential = True
    context = IProposal
    relation_validation = correct_relation_validation
    roles_validation = correct_roles_validation
    processsecurity_validation = correct_processsecurity_validation
    state_validation = correct_state_validation

    def _add_vote_actions(self, tag, correction, request):
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,'dace_ui_api')
        if not hasattr(self, 'correctitemaction'):
            correctitemnode = self.process['correctitem']
            correctitem_wis = [wi for wi in correctitemnode.workitems if wi.node is correctitemnode]
            if correctitem_wis:
                self.correctitemaction = correctitem_wis[0].actions[0]
        if hasattr(self, 'correctitemaction'):
            actionurl_update = dace_ui_api.updateaction_viewurl(request=request, action_uid=str(get_oid(self.correctitemaction)), context_uid=str(get_oid(correction)))
            values= {'favour_action_url':actionurl_update,
                     'against_action_url':actionurl_update}
            template = 'novaideo:views/proposal_management/templates/correction_item.pt'
            body = renderers.render(template, values, request)
            correction_item_soup = BeautifulSoup(body)
            correction_item_soup.body
            tag.append(correction_item_soup.body)
            tag.body.unwrap()

    def _identify_corrections(self, diff, correction, descriminator, request):
        correction_oid = str(get_oid(correction))
        user = get_current()
        user_oid = get_oid(user)
        soup = BeautifulSoup(diff)
        ins_tags = soup.find_all('ins')
        del_tags = soup.find_all('del')
        del_included = []

        for ins_tag in ins_tags:
            new_correction_tag = soup.new_tag("span", id="correction")
            new_correction_tag['data-correction'] = correction_oid
            new_correction_tag['data-item'] = str(descriminator)
            init_vote = {'favour':[user_oid], 'against':[]}
            previous_del_tag = ins_tag.find_previous_sibling('del')
            correct_exist = False
            inst_string = ins_tag.string
            if previous_del_tag is not None:
                previous_del_tag_string = previous_del_tag.string
                del_included.append(previous_del_tag)
                if previous_del_tag_string != inst_string:
                    tofind = str(previous_del_tag) +' '+str(ins_tag)
                    correction_exist = (diff.find(tofind) >=0)
                    if correction_exist:
                        correction.corrections[str(descriminator)] = init_vote
                        descriminator += 1 
                        previous_del_tag.wrap(new_correction_tag)
                        new_correction_tag.append(ins_tag)
                        self._add_vote_actions(new_correction_tag, correction, request)
                        continue
                else:
                    ins_tag.unwrap()
                    previous_del_tag.extract()

            if ins_tag.parent is not None:
                correction.corrections[str(descriminator)] = init_vote
                descriminator += 1
                ins_tag.wrap(new_correction_tag)
                self._add_vote_actions(new_correction_tag, correction, request)

        for del_tag in del_tags:
            if not(del_tag in del_included):
                if del_tag.string is not None:
                    new_correction_tag = soup.new_tag("span", id="correction")
                    new_correction_tag['data-correction'] = correction_oid
                    new_correction_tag['data-item'] = str(descriminator)
                    init_vote = {'favour':[user_oid], 'against':[]}
                    correction.corrections[str(descriminator)] = init_vote
                    descriminator += 1
                    del_tag.wrap(new_correction_tag)
                    self._add_vote_actions(new_correction_tag, correction, request)
                else:
                    del_tag.extract()        

        return soup
        
    def start(self, context, request, appstruct, **kw):
        user = get_current()
        correction = appstruct['_object_data']
        correction.setproperty('author', user)
        context.addtoproperty('corrections', correction)
        textdiff = htmldiff.render_html_diff(getattr(context, 'text', '').replace('&nbsp;', ''), getattr(correction, 'text', '').replace('&nbsp;', ''))
        descriptiondiff = htmldiff.render_html_diff(getattr(correction, 'description', ''), getattr(context, 'description', ''))
        descriminator = 0
        souptextdiff = self._identify_corrections(textdiff, correction, descriminator, request)
        soupdescriptiondiff = self._identify_corrections(descriptiondiff, correction, descriminator, request)
        correction.text = _normalize_text(souptextdiff)
        context.originaltext = str(correction.text)
        correction.description = _normalize_text(soupdescriptiondiff)
        if souptextdiff.find_all("span", id="correction"):
            correction.state.append('in process')
        return True

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
     #has_first_decision = hasattr(process, 'first_decision')
     #return (has_first_decision and has_any_roles(roles=(('Participant', context),))) or \
     #       (has_first_decision and has_any_roles(roles=('System',)))
    return has_any_roles(roles=('Member',))


def decision_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'amendable' in context.state


class VotingPublication(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 5
    context = IProposal
    relation_validation = decision_relation_validation
    roles_validation = decision_roles_validation
    state_validation = decision_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('amendable')
        context.state.append('votes for publishing')
        context.reindex()
        return True


    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def withdraw_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def withdraw_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def withdraw_processsecurity_validation(process, context):
    user = get_current()
    return global_user_processsecurity(process, context) and user in context.working_group.wating_list


def withdraw_state_validation(process, context):
    wg = context.working_group
    return  'amendable' in context.state


class Withdraw(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'wg-action'
    style_order = 3
    style_css_class = 'btn-warning'
    isSequential = False
    context = IProposal
    relation_validation = withdraw_relation_validation
    roles_validation = withdraw_roles_validation
    processsecurity_validation = withdraw_processsecurity_validation
    state_validation = withdraw_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        wg = context.working_group
        wg.delproperty('wating_list', user)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def resign_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def resign_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),))


def resign_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def resign_state_validation(process, context):
    return  'amendable' in context.state or 'open to a working group' in context.state #TODO


class Resign(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'wg-action'
    style_order = 2
    style_css_class = 'btn-danger'
    isSequential = False
    context = IProposal
    relation_validation = resign_relation_validation
    roles_validation = resign_roles_validation
    processsecurity_validation = resign_processsecurity_validation
    state_validation = resign_state_validation

    def _get_next_user(self, users, root):
        for user in users:
            if 'active' in user.state and len(user.working_groups) < root.participations_maxi:
                return user

        return None 

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        wg = context.working_group
        wg.delproperty('members', user)
        revoke_roles(user, (('Participant', context),))
        if wg.wating_list:
            next_user = self._get_next_user(wg.wating_list, root)
            if next_user is not None:
                wg.delproperty('wating_list', next_user)
                wg.addtoproperty('members', next_user)
                grant_roles(next_user, (('Participant', context),))
                #TODO send mail to next_user

        participants = wg.members
        len_participants = len(participants)
        if len_participants < root.participants_mini:
            context.state = PersistentList(['open to a working group'])
            wg.state = PersistentList(['deactivated'])
            wg.reindex()
            context.reindex()

        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def participate_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def participate_roles_validation(process, context):
    return has_any_roles(roles=('Member',)) and not has_any_roles(roles=(('Participant', context),))


def participate_processsecurity_validation(process, context):
    user = get_current()
    root = getSite()
    return global_user_processsecurity(process, context) and \
           not(user in context.working_group.wating_list) and \
           len(user.working_groups) < root.participations_maxi 


def participate_state_validation(process, context):
    wg = context.working_group
    return  'amendable' in context.state or 'open to a working group' in context.state


class Participate(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'wg-action'
    style_order = 1
    style_css_class = 'btn-success'
    isSequential = False
    context = IProposal
    relation_validation = participate_relation_validation
    roles_validation = participate_roles_validation
    processsecurity_validation = participate_processsecurity_validation
    state_validation = participate_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        wg = context.working_group
        participants = wg.members
        len_participants = len(participants)
        if len_participants < root.participants_maxi:
            wg.addtoproperty('members', user)
            grant_roles(user, (('Participant', context),))
            if (len_participants+1) == root.participants_mini:
                context.state = PersistentList()#.remove('open to a working group')
                wg.state = PersistentList(['active'])
                if not hasattr(self.process, 'first_decision'):
                    self.process.first_decision = True

                context.state.append('amendable')
                context.reindex()
        else:
            wg.addtoproperty('wating_list', user)
            wg.reindex()

        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def va_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def va_roles_validation(process, context):
    #return has_any_roles(roles=('System',))
    return has_any_roles(roles=('Member',))


def va_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'amendable' in context.state


class VotingAmendments(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 6
    context = IProposal
    relation_validation = va_relation_validation
    roles_validation = va_roles_validation
    state_validation = va_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state = PersistentList(['votes for amendments'])
        context.reindex()
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def ar_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'votes for amendments' in context.state


class AmendmentsResult(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 7
    context = IProposal
    relation_validation = va_relation_validation
    roles_validation = va_roles_validation
    state_validation = ar_state_validation

    def _get_copy(self, context, root, wg):
        copy_of_proposal = copy(context, (root, 'proposals'), roles=True)
        #copy_of_proposal.created_at = datetime.datetime.today()
        #copy_of_proposal.modified_at = datetime.datetime.today()
        copy_of_proposal.setproperty('originalentity', context)
        #copy_of_proposal.setproperty('version', None)
        #copy_of_proposal.setproperty('nextversion', None)
        copy_of_proposal.state = PersistentList(['amendable'])
        copy_of_proposal.setproperty('author', context.author)
        #root.addtoproperty('proposals', copy_of_proposal)
        #for user in wg.members: #TODO la copy des roles: option de copy
        #    grant_roles(user=user, roles=(('Participant', copy_of_proposal), ))

        #grant_roles(user=context.author, roles=(('Owner', copy_of_proposal), ))#TODO la copy des roles: option de copy
        #grant_roles(user=context.author, roles=(('Owner', context), ))
        self.process.execution_context.add_created_entity('proposal', copy_of_proposal)
        wg.setproperty('proposal', copy_of_proposal)
        return copy_of_proposal

    def _send_ballot_result(self, context, request, electeds, members):
        group_nb = 0
        amendments_vote_result = []
        for ballot in self.process.amendments_ballots: 
            result = []
            group_nb += 1
            result_ballot = "Group " + str(group_nb) + ": \n"
            for oid,result_vote in ballot.report.result.items():
                obj = get_obj(oid)
                result_vote = [judgment+": "+str(result_vote[judgment]) for judgment in ballot.report.ballottype.judgments.keys()]
                result.append(obj.title + " :" + ",".join(result_vote))

            result_ballot += "\n    ".join(result)
            amendments_vote_result.append(result_ballot)

        message_result = "\n \n".join(amendments_vote_result)
        electeds_result = "\n".join([e.title for e in electeds])
        url = request.resource_url(context, "@@index")
        subject = RESULT_VOTE_AMENDMENT_SUBJECT.format(subject_title=context.title)
        for member in members:
            recipient_title = getattr(member, 'user_title','')
            recipient_first_name = getattr(member, 'first_name', member.name)
            recipient_last_name = getattr(member, 'last_name','')
            member_email = member.email
            message = RESULT_VOTE_AMENDMENT_MESSAGE.format(
                recipient_title=recipient_title,
                recipient_first_name=recipient_first_name,
                recipient_last_name=recipient_last_name,
                subject_url=url,
                message_result=message_result,
                electeds_result=electeds_result
                 )
            mailer_send(subject=subject, recipients=[member_email], body=message)
        


    def start(self, context, request, appstruct, **kw):
        result = set()
        for ballot in self.process.amendments_ballots:
            electeds = ballot.report.get_electeds()
            if electeds is not None:
                result.update(electeds)

        #TODO merg result
        amendments = [a for a in result if isinstance(a, Amendment)]
        wg = context.working_group
        root = getSite()
        self.newcontext = context 
        if amendments:
            self._send_ballot_result(context, request, result, wg.members)
            replaced_ideas = [a.replaced_idea for a in amendments if a.replaced_idea is not None]
            ideas_of_replacement = [a.idea_of_replacement for a in amendments if a.idea_of_replacement is not None]
            text_analyzer = get_current_registry().getUtility(ITextAnalyzer,'text_analyzer')
            merged_text = text_analyzer.merge(context.text, [a.text for a in amendments])
            #TODO merged_keywords + merged_description
            copy_of_proposal = self._get_copy(context, root, wg)
            context.state = PersistentList(['deprecated'])
            copy_of_proposal.text = merged_text
            #TODO correlation idea of replacement ideas... del replaced_idea
            self.newcontext = copy_of_proposal
            copy_of_proposal.reindex()
        else:
            context.state = PersistentList(['amendable'])

        context.reindex()
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(self.newcontext, "@@index"))


def ta_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'votes for publishing' in context.state


class Amendable(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 8
    context = IProposal
    relation_validation = va_relation_validation
    roles_validation = va_roles_validation
    state_validation = ta_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('votes for publishing')
        context.state.append('amendable')
        context.reindex()
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors

validation_by_context[Proposal] = CommentProposal
