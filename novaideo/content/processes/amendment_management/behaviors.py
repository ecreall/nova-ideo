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
from dace.objectofcollaboration.principal.util import has_any_roles, grant_roles, get_current
from dace.processinstance.activity import InfiniteCardinality, ElementaryAction, ActionType

from pontus.dace_ui_extension.interfaces import IDaceUIAPI

from novaideo.ips.mailer import mailer_send
from novaideo.content.interface import INovaIdeoApplication, IAmendment, ICorrelableEntity
from ..user_management.behaviors import global_user_processsecurity
from novaideo.mail import PRESENTATION_AMENDMENT_MESSAGE, PRESENTATION_AMENDMENT_SUBJECT
from novaideo import _
from novaideo.content.amendment import Amendment, IntentionSchema
from novaideo.content.correlation import Correlation
from ..comment_management.behaviors import validation_by_context
from novaideo.core import acces_action
from novaideo.content.processes.idea_management.behaviors import PresentIdea, Associate as AssociateIdea
from novaideo.utilities.text_analyzer import ITextAnalyzer
from novaideo.ips.htmldiff import htmldiff


try:
      basestring
except NameError:
      basestring = str


def del_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context.proposal),))


def duplicate_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           (('draft' in context.state and has_any_roles(roles=(('Owner', context),))) or \
             'published' in context.state)


def duplicate_state_validation(process, context):
    proposal = context.proposal
    wg = proposal.working_group
    return 'amendable' in proposal.state and 'active' in wg.state


class DuplicateAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 3
    context = IAmendment
    roles_validation =del_roles_validation
    processsecurity_validation = duplicate_processsecurity_validation
    state_validation = duplicate_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        copy_of_amendment = copy(context, (context.proposal, 'amendments'))
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
        grant_roles(roles=(('Owner', copy_of_amendment), ))
        copy_of_amendment.reindex()
        context.reindex()
        self.newcontext = copy_of_amendment
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(self.newcontext, "@@index"))


def del_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context),))


def del_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def del_state_validation(process, context):
    return ('draft' in context.state)


class DelAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
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
    return has_any_roles(roles=(('Owner', context),))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           not(context.explanations and any(e['intention'] is not None for e in context.explanations.values()))


def edit_state_validation(process, context):
    return ('draft' in context.state)


class EditAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
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
    return has_any_roles(roles=(('Owner', context),))


def exp_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def exp_state_validation(process, context):
    return ('draft' in context.state) and not('explanation' in context.state)


class ExplanationAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
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

        context.reindex()
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def pub_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context),))


def pub_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           not context.explanations or  not(context.explanations and any(e['intention'] is None for e in context.explanations.values()))


def pub_state_validation(process, context):
    return ('explanation' in context.state) and ('draft' in context.state)


class SubmitAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 1
    context = IAmendment
    roles_validation = pub_roles_validation
    processsecurity_validation = pub_processsecurity_validation
    state_validation = pub_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('draft')
        context.state.remove('explanation')
        context.state.append('published')
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def comm_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context.proposal),))


def comm_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def comm_state_validation(process, context):
    return 'published' in context.state


class CommentAmendment(InfiniteCardinality):
    isSequential = False
    context = IAmendment
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


def present_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context.proposal),))


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
    return global_user_processsecurity(process, context) and \
           (has_any_roles(roles=(('Owner', context),)) or \
           (has_any_roles(roles=('Member',)) and 'published' in context.state))


class Associate(AssociateIdea):
    context = IAmendment
    processsecurity_validation = associate_processsecurity_validation


def seeamendment_processsecurity_validation(process, context):
    return ('published' in context.state or has_any_roles(roles=(('Owner', context),)))

@acces_action()
class SeeAmendment(InfiniteCardinality):
    title = _('Details')
    context = IAmendment
    actionType = ActionType.automatic
    processsecurity_validation = seeamendment_processsecurity_validation

    def _add_modal(self, soup, tag, context, request):
        context_oid = get_oid(context)
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,'dace_ui_api')
        if not hasattr(self, 'explanationitemaction'):
            explanationitemnode = self.process['explanationitem']
            explanationitem_wis = [wi for wi in explanationitemnode.workitems if wi.node is explanationitemnode]
            if explanationitem_wis:
                self.explanationitemaction = explanationitem_wis[0].actions[0]

        if hasattr(self, 'explanationitemaction'):
            values= {'url':request.resource_url(context, '@@explanationjson', query={'op':'getform', 'itemid':tag['data-item']}),
                     'item': context.explanations[tag['data-item']],
                    }
            template = 'novaideo:views/amendment_management/templates/explanation_item.pt'
            body = renderers.render(template, values, request)
            explanation_item_soup = BeautifulSoup(body)

            actionurl_update = dace_ui_api.updateaction_viewurl(request=request, action_uid=str(get_oid(self.explanationitemaction)), context_uid=str(context_oid))
            values= {'url':actionurl_update,
                     'item': context.explanations[tag['data-item']],
                    }
            template = 'novaideo:views/amendment_management/templates/explanation_modal_item.pt'
            modal_body = renderers.render(template, values, request)
            explanation_item_modal_soup = BeautifulSoup(modal_body)
            soup.body.append(explanation_item_modal_soup.body)
            tag.append(explanation_item_soup.body)
            tag.body.unwrap()

    def _identify_explanations(self, context, request, diff, descriminator):
        context_oid = str(get_oid(context))
        user = get_current()
        user_oid = get_oid(user)
        soup = BeautifulSoup(diff)
        ins_tags = soup.find_all('ins')
        del_tags = soup.find_all('del')
        del_included = []
        for ins_tag in ins_tags:
            new_explanation_tag = soup.new_tag("span", id="explanation")
            new_explanation_tag['data-context'] = context_oid
            new_explanation_tag['data-item'] = str(descriminator)
            init_vote = {'oid':descriminator, 'intention':None}
            previous_del_tag = ins_tag.find_previous_sibling('del')
            correct_exist = False
            inst_string = ins_tag.string
            if previous_del_tag is not None:
                previous_del_tag_string = previous_del_tag.string
                del_included.append(previous_del_tag)
                if previous_del_tag_string != inst_string:
                    tofind = str(previous_del_tag) +' '+str(ins_tag)
                    explanation_exist = (diff.find(tofind) >=0)
                    if explanation_exist:
                        if not(str(descriminator) in context.explanations): 
                            context.explanations[str(descriminator)] = PersistentDict(init_vote)

                        descriminator += 1 
                        previous_del_tag.wrap(new_explanation_tag)
                        new_explanation_tag.append(ins_tag)
                        self._add_modal(soup, new_explanation_tag, context, request)
                        continue
                else:
                    ins_tag.unwrap()
                    previous_del_tag.extract()

            if ins_tag.parent is not None:
                if not(str(descriminator) in context.explanations): 
                    context.explanations[str(descriminator)] = PersistentDict(init_vote)

                descriminator += 1
                ins_tag.wrap(new_explanation_tag)
                self._add_modal(soup, new_explanation_tag, context, request)

        for del_tag in del_tags:
            if not(del_tag in del_included):
                if del_tag.string is not None:
                    new_explanation_tag = soup.new_tag("span", id="explanation")
                    new_explanation_tag['data-context'] = context_oid
                    new_explanation_tag['data-item'] = str(descriminator)
                    init_vote = {'oid':descriminator, 'intention':None}
                    if not(str(descriminator) in context.explanations): 
                        context.explanations[str(descriminator)] = PersistentDict(init_vote)

                    descriminator += 1
                    del_tag.wrap(new_explanation_tag)
                    self._add_modal(soup, new_explanation_tag, context, request)
                else:
                    del_tag.extract()        

        return soup

    def start(self, context, request, appstruct, **kw):
        if 'explanation' in context.state:
            proposal = context.proposal
            textdiff = htmldiff.render_html_diff(getattr(proposal, 'text', ''), getattr(context, 'text', ''))
            descriminator = 1
            souptextdiff = self._identify_explanations(context, request, textdiff, descriminator)
            context.explanationtext = souptextdiff

        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#TODO behaviors

validation_by_context[Amendment] = CommentAmendment
