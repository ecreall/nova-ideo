# -*- coding: utf8 -*-
import datetime
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_request, get_current_registry
from pyramid import renderers
from substanced.util import get_oid
from bs4 import BeautifulSoup

from dace.util import (
    getSite,
    getBusinessAction,
    copy,
    find_entities,
    get_obj)
from dace.objectofcollaboration.principal.util import has_role, grant_roles, get_current
from dace.processinstance.activity import InfiniteCardinality, ElementaryAction, ActionType

from pontus.dace_ui_extension.interfaces import IDaceUIAPI

from novaideo.ips.mailer import mailer_send
from novaideo.content.interface import INovaIdeoApplication, IAmendment, ICorrelableEntity
from ..user_management.behaviors import global_user_processsecurity
from novaideo.mail import PRESENTATION_AMENDMENT_MESSAGE, PRESENTATION_AMENDMENT_SUBJECT
from novaideo import _
from novaideo.content.amendment import Amendment, IntentionSchema, Intention
from novaideo.content.correlation import Correlation
from ..comment_management.behaviors import validation_by_context
from novaideo.core import acces_action
from novaideo.content.processes.idea_management.behaviors import PresentIdea, CommentIdea, Associate as AssociateIdea
from novaideo.utilities.text_analyzer import ITextAnalyzer

try:
      basestring
except NameError:
      basestring = str


def del_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal))


def duplicate_processsecurity_validation(process, context):
    return ('published' in context.state or \
            ('draft' in context.state and has_role(role=('Owner', context)))) and \
           global_user_processsecurity(process, context)


def duplicate_state_validation(process, context):
    return 'amendable' in context.proposal.state and \
           'active' in context.proposal.working_group.state


class DuplicateAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-resize-full'
    style_order = 3
    context = IAmendment
    roles_validation =del_roles_validation
    processsecurity_validation = duplicate_processsecurity_validation
    state_validation = duplicate_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        copy_of_amendment = copy(context, (context.proposal, 'amendments'), omit=('created_at', 'modified_at', 'explanations'))
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        appstruct['keywords_ref'] = result
        copy_of_amendment.set_data(appstruct)
        #context.proposal.addtoproperty('amendments', copy_of_amendment)
        copy_of_amendment.setproperty('originalentity', context)
        copy_of_amendment.state = PersistentList(['draft'])
        copy_of_amendment.setproperty('author', get_current())
        copy_of_amendment.title = context.proposal.title+'_A '+str(getattr(context.proposal, '_amendments_counter', 1)) 
        grant_roles(roles=(('Owner', copy_of_amendment), ))
        copy_of_amendment.reindex()
        context.proposal._amendments_counter = getattr(context.proposal, '_amendments_counter', 1) + 1
        context.reindex()
        self.newcontext = copy_of_amendment
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(self.newcontext, "@@index"))


def del_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal)) and has_role(role=('Owner', context))


def del_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def del_state_validation(process, context):
    return ('draft' in context.state)


class DelAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_order = 2
    context = IAmendment
    roles_validation = del_roles_validation
    processsecurity_validation = del_processsecurity_validation
    state_validation = del_state_validation

    def start(self, context, request, appstruct, **kw):
        proposal = context.proposal
        proposal.delproperty('amendments', context)
        self.newcontext = proposal
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(self.newcontext, '@@index'))


def edit_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal)) and has_role(role=('Owner', context))


def edit_processsecurity_validation(process, context):
    return not(context.explanations and \
           any(e['intention'] is not None for e in context.explanations.values())) and \
           global_user_processsecurity(process, context) 


def edit_state_validation(process, context):
    return ('draft' in context.state)


class EditAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    context = IAmendment
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation


    def start(self, context, request, appstruct, **kw):
        root = getSite()
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        appstruct['keywords_ref'] = result
        context.set_data(appstruct)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

  
def exp_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal)) and has_role(role=('Owner', context))


def exp_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def exp_state_validation(process, context):
    return ('draft' in context.state) and not('explanation' in context.state)


class ExplanationAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-question-sign'
    style_order = 1
    context = IAmendment
    roles_validation = exp_roles_validation
    processsecurity_validation = exp_processsecurity_validation
    state_validation = exp_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.append('explanation')
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index")) 


def expitem_state_validation(process, context):
    return ('draft' in context.state) and ('explanation' in context.state)


class ExplanationItem(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = True
    context = IAmendment
    roles_validation = exp_roles_validation
    processsecurity_validation = exp_processsecurity_validation
    state_validation = expitem_state_validation


    def start(self, context, request, appstruct, **kw):
        if appstruct['intention'] is not None:
            context.explanations[appstruct['item']]['intention'] = PersistentDict(appstruct['intention'])
        else:
            context.explanations[appstruct['item']]['intention'] = None

        #context.get_used_ideas.invalidate()
        context.reindex()
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def pub_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal)) and has_role(role=('Owner', context))


def pub_processsecurity_validation(process, context):
    return not context.explanations or \
           not(context.explanations and any(e['intention'] is None for e in context.explanations.values())) and \
           global_user_processsecurity(process, context)


def pub_state_validation(process, context):
    return ('explanation' in context.state) and ('draft' in context.state)


class SubmitAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 1
    context = IAmendment
    roles_validation = pub_roles_validation
    processsecurity_validation = pub_processsecurity_validation
    state_validation = pub_state_validation
   
    def _include_explanations(self, explanations, todel, toins, soup):
        explanations_data = []
        for explanation in explanations:
            explanation_data = {'tag': explanation,
                                'todel': todel,
                                'toins': toins,
                                'blocstodel': ('span', {'id':'explanation_action'})
                                }
            explanations_data.append(explanation_data)

        text_analyzer = get_current_registry().getUtility(ITextAnalyzer,'text_analyzer')
        text_analyzer.unwrap_diff(explanations_data, soup)

    def _get_amendment_text(self, context, group):
        text_analyzer = get_current_registry().getUtility(ITextAnalyzer,'text_analyzer')
        items = [str(e['oid']) for e in group]
        soup = BeautifulSoup(context.explanationtext)
        allexplanations = soup.find_all('span',{'id':'explanation'})
        explanations = [tag for tag in allexplanations if not (tag['data-item'] in items)]
        self._include_explanations(explanations, "ins", "del", soup)
        explanations = [tag for tag in allexplanations if (tag['data-item'] in items)]
        self._include_explanations(explanations, "del", "ins", soup)
        allmodal = [ m for m in soup.find_all('div',{'class':'modal'}) if m['id'].endswith("explanation_modal")]
        for modal in allmodal:
            modal.extract()

        text = text_analyzer.soup_to_text(soup)
        return text

    def _get_explanation_data(self, context, group):
        data = {
            'title': group['title'] ,
            'comment':  "\n".join(list(set([i['intention']['comment'] for i in group['explanations']]))),
            'text': self._get_amendment_text(context, group['explanations']),
            'description': context.description #TODO,
        }
        return data

    def _add_sub_amendment(self, context, group):
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
        for e in explanations:
            e['oid'] = i
            amendment.explanations[str(i)] = e
            i+=1
 
        return amendment

    def _publish_ideas(self, amendment):
        for idea in [i for i in amendment.get_used_ideas() if not('published' in i.state)]:
            idea.state = PersistentList(['published'])
            idea.reindex()

    def start(self, context, request, appstruct, **kw):
        single_amendment = appstruct['single_amendment']
        groups = []
        if single_amendment:
           group = {'title':context.title, 'explanations': list(context.explanations.values())}
           groups = [group]             
        else:
            groups = appstruct['groups']
            for group in groups:
                group['explanations'] = [context.explanations[e] for e in group['explanations']]
            
        context.state.remove('draft')
        context.state.remove('explanation')
        if len(groups) == 1:
            group = groups[0]
            data = self._get_explanation_data(context, group)
            data['title'] = group['title']
            data.pop('description')
            data.pop('text')
            context.set_data(data)
            context.state.append('published')
            self._publish_ideas(context)
        else:
            for group in groups:
                amendment = self._add_sub_amendment(context, group)
                #publish used ideas
                self._publish_ideas(amendment)

            context.state.append('archived')

        context.reindex()         
        return True

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
    return ('published' in context.state and has_role(role=('Participant', context.proposal))) or \
           ('draft' in context.state and has_role(role=('Owner', context)))

class SeeAmendmentManager(object):

    explanation_template = 'novaideo:views/amendment_management/templates/explanation_item.pt'
    modal_template = 'novaideo:views/amendment_management/templates/explanation_modal_item.pt'
    readonly_explanation_template = 'novaideo:views/amendment_management/templates/readonly/explanation_item.pt'
    readonly_modal_template = 'novaideo:views/amendment_management/templates/readonly/explanation_modal_item.pt'

    @classmethod
    def _get_explanation_diff(cls, context, request):
        proposal = context.proposal
        text_analyzer = get_current_registry().getUtility(ITextAnalyzer,'text_analyzer')
        souptextdiff, textdiff = text_analyzer.render_html_diff(getattr(proposal, 'text', ''), getattr(context, 'text', ''), "explanation")
        descriminator = 1
        cls._identify_explanations(context, request, souptextdiff, descriminator)
        return souptextdiff, textdiff

    @classmethod
    def _add_modal(cls, action, soup, tag, context, request):
        context_oid = get_oid(context)
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,'dace_ui_api')
        if not hasattr(action, 'explanationitemaction'):
            explanationitemnode = action.process['explanationitem']
            explanationitem_wis = [wi for wi in explanationitemnode.workitems if wi.node is explanationitemnode]
            if explanationitem_wis:
                action.explanationitemaction = explanationitem_wis[0].actions[0]

        if hasattr(action, 'explanationitemaction'):
            values= {'url':request.resource_url(context, '@@explanationjson', 
                                                query={'op':'getform', 'itemid':tag['data-item']}),
                     'item': context.explanations[tag['data-item']],
                    }
            body = renderers.render(cls.explanation_template, values, request)
            explanation_item_soup = BeautifulSoup(body)

            actionurl_update = dace_ui_api.updateaction_viewurl(request=request, action_uid=str(get_oid(action.explanationitemaction)), context_uid=str(context_oid))
            values= {'url':actionurl_update,
                     'item': context.explanations[tag['data-item']],
                    }
            modal_body = renderers.render(cls.modal_template, values, request)
            explanation_item_modal_soup = BeautifulSoup(modal_body)
            soup.body.append(explanation_item_modal_soup.body)
            tag.append(explanation_item_soup.body)
            tag.body.unwrap()

    @classmethod
    def _add_modal_details(cls, soup, tag, context, request):
        context_oid = get_oid(context)
        data = {}
        try:
            data = Intention.get_explanation_data(context.explanations[tag['data-item']]['intention'])
        except Exception:
            pass

        values= {'item': context.explanations[tag['data-item']], 'data': data}
        body = renderers.render(cls.readonly_explanation_template, values, request)
        explanation_item_soup = BeautifulSoup(body)
        modal_body = renderers.render(cls.readonly_modal_template, values, request)
        explanation_item_modal_soup = BeautifulSoup(modal_body)
        soup.body.append(explanation_item_modal_soup.body)
        tag.append(explanation_item_soup.body)
        tag.body.unwrap()

    @classmethod
    def _add_actions(cls, action, context, request, soup):
        explanations_tags = soup.find_all('span', {'id':'explanation'})
        for explanation_tag in explanations_tags:
            cls._add_modal(action, soup, explanation_tag, context, request)

    @classmethod
    def _add_details(cls, context, request, soup):
        explanations_tags = soup.find_all('span', {'id':'explanation'})
        for explanation_tag in explanations_tags:
            cls._add_modal_details(soup, explanation_tag, context, request)

    @classmethod
    def _identify_explanations(cls, context, request, soup, descriminator):
        correction_tags = soup.find_all('span', {'id': "explanation"})
        context_oid = str(get_oid(context))
        user = get_current()
        user_oid = get_oid(user)
        for correction_tag in correction_tags:
            correction_tag['data-context'] = context_oid
            correction_tag['data-item'] = str(descriminator)
            init_vote = {'oid':descriminator, 'intention':None}
            if not(str(descriminator) in context.explanations): 
                context.explanations[str(descriminator)] = PersistentDict(init_vote)

            descriminator += 1


@acces_action()
class SeeAmendment(InfiniteCardinality):
    title = _('Details')
    context = IAmendment
    actionType = ActionType.automatic
    processsecurity_validation = seeamendment_processsecurity_validation  

    def start(self, context, request, appstruct, **kw):
        if any(s in context.state for s in ['explanation', 'published']):
            text_analyzer = get_current_registry().getUtility(ITextAnalyzer,'text_analyzer')
            souptextdiff, textdiff = SeeAmendmentManager._get_explanation_diff(context, request)
            if 'explanation' in context.state:
                SeeAmendmentManager._add_actions(self, context, request, souptextdiff)
            else:
                SeeAmendmentManager._add_details(context, request, souptextdiff)
 
            context.explanationtext = text_analyzer.soup_to_text(souptextdiff)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#TODO behaviors

validation_by_context[Amendment] = CommentAmendment
