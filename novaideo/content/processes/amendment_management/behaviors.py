# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the 
Amendments management process definition. 
"""

from persistent.list import PersistentList
from persistent.dict import PersistentDict
from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_registry
from bs4 import BeautifulSoup

from dace.util import (
    getSite,
    copy)
from dace.objectofcollaboration.principal.util import (
    has_role, 
    grant_roles, 
    get_current)
from dace.processinstance.activity import InfiniteCardinality, ActionType

from novaideo.content.interface import IAmendment
from ..user_management.behaviors import global_user_processsecurity
from novaideo import _
from novaideo.content.amendment import Amendment
from ..comment_management.behaviors import VALIDATOR_BY_CONTEXT
from novaideo.core import acces_action
from novaideo.content.processes.idea_management.behaviors import (
    PresentIdea, 
    CommentIdea, 
    Associate as AssociateIdea)
from novaideo.utilities.text_analyzer import ITextAnalyzer, normalize_text
from novaideo.utilities.amendment_viewer import IAmendmentViewer
from novaideo.event import CorrelableRemoved

try:
    basestring
except NameError:
    basestring = str


def get_text_amendment_diff(proposal, amendment):
    text_analyzer = get_current_registry().getUtility(
                                 ITextAnalyzer,'text_analyzer')
    soup, textdiff =  text_analyzer.render_html_diff(
                            getattr(proposal, 'text', ''), 
                            getattr(amendment, 'text', ''))
    return textdiff


def get_text_amendment_diff_explanation(amendment, request, process):
    text_analyzer = get_current_registry().getUtility(
                             ITextAnalyzer, 'text_analyzer')
    amendment_viewer = get_current_registry().getUtility(
                             IAmendmentViewer, 'amendment_viewer')
    souptextdiff, explanations = amendment_viewer.get_explanation_diff(
                                                        amendment, request)
    amendment_viewer.add_actions(explanations, process, amendment,
                                 request, souptextdiff)
    return explanations, text_analyzer.soup_to_text(souptextdiff)


def get_text_amendment_diff_submitted(amendment, request):
    text_analyzer = get_current_registry().getUtility(
                             ITextAnalyzer, 'text_analyzer')
    amendment_viewer = get_current_registry().getUtility(
                             IAmendmentViewer, 'amendment_viewer')
    souptextdiff, explanations = amendment_viewer.get_explanation_diff(
                                                    amendment, request)
    amendment_viewer.add_details(explanations, amendment, request, souptextdiff)
    return explanations, text_analyzer.soup_to_text(souptextdiff)


def duplicate_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal))


def duplicate_processsecurity_validation(process, context):
    return ('published' in context.state or \
            ('draft' in context.state and \
             has_role(role=('Owner', context)))) and \
           global_user_processsecurity(process, context)


def duplicate_state_validation(process, context):
    return 'amendable' in context.proposal.state and \
           'active' in context.proposal.working_group.state


class DuplicateAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-resize-full'
    style_order = 2
    submission_title = _('Save')
    context = IAmendment
    roles_validation = duplicate_roles_validation
    processsecurity_validation = duplicate_processsecurity_validation
    state_validation = duplicate_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        copy_of_amendment = copy(context, 
                                 (context.proposal, 'amendments'),
                                 omit=('created_at',
                                       'modified_at',
                                       'explanations'))
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nkw in newkeywords:
            root.addtoproperty('keywords', nkw)

        result.extend(newkeywords)
        appstruct['keywords_ref'] = result
        copy_of_amendment.set_data(appstruct)
        copy_of_amendment.text = normalize_text(copy_of_amendment.text)
        copy_of_amendment.setproperty('originalentity', context)
        copy_of_amendment.state = PersistentList(['draft'])
        copy_of_amendment.setproperty('author', get_current())
        localizer = request.localizer
        # copy_of_amendment.title = context.proposal.title + \
        #                         localizer.translate(_('_Amended version ')) + \
        #                         str(getattr(context.proposal,
        #                                    '_amendments_counter', 1)) 
        copy_of_amendment.title = localizer.translate(_('Amended version ')) + \
                                str(getattr(context.proposal,
                                           '_amendments_counter', 1)) 
        grant_roles(roles=(('Owner', copy_of_amendment), ))
        copy_of_amendment.text_diff = get_text_amendment_diff(
                                           context.proposal, copy_of_amendment)
        copy_of_amendment.reindex()
        context.proposal._amendments_counter = getattr(context.proposal, 
                                                 '_amendments_counter', 1) + 1
        context.reindex()
        return {'newcontext': copy_of_amendment}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def del_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal)) and \
           has_role(role=('Owner', context))


def del_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def del_state_validation(process, context):
    return ('draft' in context.state)


class DelAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_order = 4
    context = IAmendment
    roles_validation = del_roles_validation
    processsecurity_validation = del_processsecurity_validation
    state_validation = del_state_validation

    def start(self, context, request, appstruct, **kw):
        proposal = context.proposal
        request.registry.notify(CorrelableRemoved(object=context))
        proposal.delfromproperty('amendments', context)
        return {'newcontext': proposal}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], '@@index'))


def edit_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal)) and \
           has_role(role=('Owner', context))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) 


def edit_state_validation(process, context):
    return 'draft' in context.state and \
           'explanation' not in context.state 


class EditAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    submission_title = _('Save')
    context = IAmendment
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nkw in newkeywords:
            root.addtoproperty('keywords', nkw)

        result.extend(newkeywords)
        appstruct['keywords_ref'] = result
        context.set_data(appstruct)
        context.text = normalize_text(context.text)
        context.text_diff = get_text_amendment_diff(
                                   context.proposal, context)
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

  
def exp_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal)) and \
           has_role(role=('Owner', context))


def exp_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def exp_state_validation(process, context):
    return 'draft' in context.state and \
           'explanation' not in context.state


class ExplanationAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-question-sign'
    style_order = 5
    submission_title = _('Continue')
    context = IAmendment
    roles_validation = exp_roles_validation
    processsecurity_validation = exp_processsecurity_validation
    state_validation = exp_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.append('explanation')
        explanations, text_diff = get_text_amendment_diff_explanation(
                                   context, request, self.process)
        context.explanations = PersistentDict(explanations) 
        context.text_diff = text_diff
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index")) 


def expitem_state_validation(process, context):
    return 'draft' in context.state and \
           'explanation' in context.state


class ExplanationItem(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = True
    context = IAmendment
    roles_validation = exp_roles_validation
    processsecurity_validation = exp_processsecurity_validation
    state_validation = expitem_state_validation

    item_css_on = 'btn-white'
    item_css_off = 'btn-black'

    def _add_css_item(self, context, item):
        text_analyzer = get_current_registry().getUtility(
                                 ITextAnalyzer,'text_analyzer')
        soup = BeautifulSoup(context.text_diff)
        tag_item = soup.find('button', {'data-target': '#'+str(item)})
        if tag_item and self.item_css_off in tag_item['class']:
            tag_item['class'].remove(self.item_css_off)
            tag_item['class'].append(self.item_css_on)

        context.text_diff = text_analyzer.soup_to_text(soup)

    def _remove_css_item(self, context, item):
        text_analyzer = get_current_registry().getUtility(
                                 ITextAnalyzer,'text_analyzer')
        soup = BeautifulSoup(context.text_diff)
        tag_item = soup.find('button', {'data-target': '#'+str(item)})
        if tag_item and self.item_css_on in tag_item['class']:
            tag_item['class'].remove(self.item_css_on)
            tag_item['class'].append(self.item_css_off)

        context.text_diff = text_analyzer.soup_to_text(soup)

    def start(self, context, request, appstruct, **kw):
        if appstruct['intention'] is not None:
            item = appstruct['item']
            intention = appstruct['intention']
            context.explanations[item]['intention'] = PersistentDict(intention)
            self._add_css_item(context, item)
        else:
            item = appstruct['item']
            context.explanations[item]['intention'] = None
            self._remove_css_item(context, item)

        #context.get_used_ideas.invalidate()
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def pub_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal)) and \
           has_role(role=('Owner', context))


def pub_processsecurity_validation(process, context):
    return not context.explanations or \
           not(context.explanations and \
               any(e['intention'] is None 
                   for e in context.explanations.values())) and \
           global_user_processsecurity(process, context)


def pub_state_validation(process, context):
    return ('explanation' in context.state) and ('draft' in context.state)


class SubmitAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 6
    title = _('Prepare amendments')
    submission_title = _('Submit')
    context = IAmendment
    roles_validation = pub_roles_validation
    processsecurity_validation = pub_processsecurity_validation
    state_validation = pub_state_validation
   

    def _get_amendment_text(self, context, group):
        text_analyzer = get_current_registry().getUtility(
                                 ITextAnalyzer, 'text_analyzer')
        items = [str(e['oid']) for e in group]
        soup = BeautifulSoup(context.text_diff)
        allexplanations = soup.find_all('span', {'id':'explanation'})
        explanations = [tag for tag in allexplanations 
                        if not (tag['data-item'] in items)]
        blocstodel = ('span', {'id':'explanation_action'})
        soup = text_analyzer.include_diffs(soup, explanations,
                        "ins", "del", blocstodel)
        explanations = [tag for tag in allexplanations 
                        if (tag['data-item'] in items)]
        soup = text_analyzer.include_diffs(soup, explanations,
                        "del", "ins", blocstodel)
        allmodal = [ m for m in soup.find_all('div', {'class':'modal'}) 
                     if m['id'].endswith("explanation_modal")]
        for modal in allmodal:
            modal.extract()

        text = text_analyzer.soup_to_text(soup)
        return text

    def _get_explanation_data(self, context, group):
        data = {
            'title': group['title'] ,
            'text': self._get_amendment_text(context, group['explanations']),
            'description': context.description,
            'justification': group.get('justification', '')
        }
        return data

    def _add_sub_amendment(self, context, request, group):
        data = self._get_explanation_data(context, group)
        keywords_ref = context.keywords_ref
        amendment = Amendment()
        for k in keywords_ref:
            amendment.addtoproperty('keywords_ref', k)

        amendment.set_data(data)
        context.proposal.addtoproperty('amendments', amendment)
        amendment.state.append('published')
        grant_roles(roles=(('Owner', amendment), ))
        amendment.setproperty('author', get_current())
        #amendment.setproperty('originalentity', context)
        explanations = sorted(group['explanations'], key=lambda e: e['oid'])
        i = 1
        for explanation in explanations:
            explanation['oid'] = i
            amendment.explanations[str(i)] = explanation
            i += 1

        explanations, text_diff = get_text_amendment_diff_submitted(
                                                amendment, request)
        amendment.explanations = PersistentDict(explanations) 
        amendment.text_diff = text_diff
        amendment.reindex()
        self._publish_ideas(amendment)

    def _publish_ideas(self, amendment):
        for idea in [i for i in amendment.get_used_ideas() \
                     if not('published' in i.state)]:
            idea.state = PersistentList(['published'])
            idea.reindex()

    def start(self, context, request, appstruct, **kw):
        single_amendment = appstruct['single_amendment']
        groups = []
        if single_amendment:
            group = {'title': context.title, 
                    'explanations': list(context.explanations.values()),
                    'justification': appstruct.get('justification', '')}
            groups = [group]             
        else:
            groups = appstruct['groups']
            for group in groups:
                group['explanations'] = [context.explanations[e] 
                                         for e in group['explanations']]
            
        context.state.remove('draft')
        context.state.remove('explanation')
        if len(groups) == 1:
            group = groups[0]
            data = self._get_explanation_data(context, group)
            data.pop('description')
            data.pop('text')
            context.set_data(data)
            context.state.append('published')
            explanations, text_diff = get_text_amendment_diff_submitted(
                                                       context, request)
            context.explanations = PersistentDict(explanations) 
            context.text_diff = text_diff
            self._publish_ideas(context)
        else:
            for group in groups:
                self._add_sub_amendment(context, request, group)
                
            context.state.append('archived')

        context.reindex()         
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context.proposal, "@@index"))


def comm_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal))


def comm_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def comm_state_validation(process, context):
    return 'published' in context.state


class CommentAmendment(CommentIdea):
    isSequential = False
    context = IAmendment
    roles_validation = comm_roles_validation
    processsecurity_validation = comm_processsecurity_validation
    state_validation = comm_state_validation


def present_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal))


def present_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def present_state_validation(process, context):
    return 'published' in context.state


class PresentAmendment(PresentIdea):
    context = IAmendment
    roles_validation = present_roles_validation
    processsecurity_validation = present_processsecurity_validation
    state_validation = present_state_validation


def associate_processsecurity_validation(process, context):
    return (has_role(role=('Owner', context)) or \
           ('published' in context.state and has_role(role=('Member',)))) and \
           global_user_processsecurity(process, context) 


class Associate(AssociateIdea):
    context = IAmendment
    processsecurity_validation = associate_processsecurity_validation


def seeamendment_processsecurity_validation(process, context):
    return ('published' in context.state and \
            has_role(role=('Participant', context.proposal))) or \
           ('draft' in context.state and has_role(role=('Owner', context)))


@acces_action()
class SeeAmendment(InfiniteCardinality):
    """SeeAmendment is the behavior allowing access to context"""
    
    title = _('Details')
    context = IAmendment
    actionType = ActionType.automatic
    processsecurity_validation = seeamendment_processsecurity_validation  

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#TODO behaviors

VALIDATOR_BY_CONTEXT[Amendment] = CommentAmendment
