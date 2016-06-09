# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the
Amendments management process definition.
"""
import datetime
import pytz
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_registry
from bs4 import BeautifulSoup

import html_diff_wrapper
from dace.util import (
    getSite,
    copy)
from dace.objectofcollaboration.principal.util import (
    has_role,
    has_any_roles,
    grant_roles,
    get_current)
from dace.processinstance.activity import InfiniteCardinality, ActionType
from dace.processinstance.core import ActivityExecuted

from novaideo.content.interface import IAmendment
from ..user_management.behaviors import global_user_processsecurity
from novaideo import _
from novaideo.content.amendment import Amendment
from ..comment_management.behaviors import VALIDATOR_BY_CONTEXT
from novaideo.core import access_action, serialize_roles
from novaideo.content.processes.idea_management.behaviors import (
    PresentIdea,
    CommentIdea,
    Associate as AssociateIdea)

from novaideo.content.processes.proposal_management.behaviors import (
    publish_ideas)
from novaideo.utilities.amendment_viewer import IAmendmentViewer
from novaideo.event import CorrelableRemoved
from novaideo.content.alert import InternalAlertKind
from novaideo.utilities.alerts_utility import alert

try:
    basestring
except NameError:
    basestring = str


def get_text_amendment_diff(proposal, amendment):
    soup, textdiff = html_diff_wrapper.render_html_diff(
        getattr(proposal, 'text', ''),
        getattr(amendment, 'text', ''))
    return textdiff


def get_text_amendment_diff_explanation(amendment, request, process):
    amendment_viewer = get_current_registry().getUtility(
        IAmendmentViewer, 'amendment_viewer')
    souptextdiff, explanations = amendment_viewer.get_explanation_diff(
        amendment, request)
    amendment_viewer.add_actions(explanations, process, amendment,
                                 request, souptextdiff)
    return explanations, html_diff_wrapper.soup_to_text(souptextdiff)


def get_text_amendment_diff_submitted(amendment, request):
    amendment_viewer = get_current_registry().getUtility(
        IAmendmentViewer, 'amendment_viewer')
    souptextdiff, explanations = amendment_viewer.get_explanation_diff(
        amendment, request)
    amendment_viewer.add_details(explanations, amendment, request, souptextdiff)
    return explanations, html_diff_wrapper.soup_to_text(souptextdiff)


def duplicate_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal))


def duplicate_processsecurity_validation(process, context):
    return ('submitted' in context.state or \
            ('draft' in context.state and \
             has_role(role=('Owner', context)))) and \
           global_user_processsecurity(process, context)


def duplicate_state_validation(process, context):
    return 'amendable' in context.proposal.state and \
           'active' in context.proposal.working_group.state


class DuplicateAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-resize-full'
    style_order = 2
    submission_title = _('Save')
    context = IAmendment
    roles_validation = duplicate_roles_validation
    processsecurity_validation = duplicate_processsecurity_validation
    state_validation = duplicate_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        copy_of_amendment = copy(context,
                                 (context.proposal, 'amendments'),
                                 omit=('created_at',
                                       'modified_at',
                                       'explanations'))
        # root.merge_keywords(appstruct['keywords'])
        copy_of_amendment.set_data(appstruct)
        copy_of_amendment.text = html_diff_wrapper.normalize_text(
            copy_of_amendment.text)
        copy_of_amendment.setproperty('originalentity', context)
        copy_of_amendment.state = PersistentList(['draft'])
        copy_of_amendment.setproperty('author', user)
        localizer = request.localizer
        copy_of_amendment.title = localizer.translate(
            _('Amended version ')) + str(getattr(context.proposal,
                                         '_amendments_counter', 1))
        grant_roles(user=user, roles=(('Owner', copy_of_amendment), ))
        copy_of_amendment.text_diff = get_text_amendment_diff(
            context.proposal, copy_of_amendment)
        copy_of_amendment.reindex()
        context.proposal._amendments_counter = getattr(
            context.proposal, '_amendments_counter', 1) + 1
        context.reindex()
        request.registry.notify(ActivityExecuted(self, [context], user))
        return {'newcontext': copy_of_amendment}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def del_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal)) and \
           has_role(role=('Owner', context))


def del_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def del_state_validation(process, context):
    return 'draft' in context.state


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
        # root.merge_keywords(context.keywords)
        context.set_data(appstruct)
        context.text = html_diff_wrapper.normalize_text(context.text)
        context.text_diff = get_text_amendment_diff(
            context.proposal, context)
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
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
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
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
        soup = BeautifulSoup(context.text_diff)
        tag_item = soup.find('button', {'data-target': '#'+str(item)})
        if tag_item and self.item_css_off in tag_item['class']:
            tag_item['class'].remove(self.item_css_off)
            tag_item['class'].append(self.item_css_on)

        context.text_diff = html_diff_wrapper.soup_to_text(soup)

    def _remove_css_item(self, context, item):
        soup = BeautifulSoup(context.text_diff)
        tag_item = soup.find('button', {'data-target': '#'+str(item)})
        if tag_item and self.item_css_on in tag_item['class']:
            tag_item['class'].remove(self.item_css_on)
            tag_item['class'].append(self.item_css_off)

        context.text_diff = html_diff_wrapper.soup_to_text(soup)

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
    root = getSite()
    not_published_ideas = False
    if getattr(root, 'moderate_ideas', False):
        not_published_ideas = any('published' not in i.state
                                  for i in context.get_used_ideas())

    not_favorable_ideas = False
    if 'idea' in getattr(root, 'content_to_examine', []):
        not_favorable_ideas = any('favorable' not in i.state
                                  for i in context.get_used_ideas())

    return not (not_published_ideas or not_favorable_ideas) and \
           (not context.explanations or \
           not(context.explanations and \
               any(e['intention'] is None 
                   for e in context.explanations.values()))) and \
           global_user_processsecurity(process, context)


def pub_state_validation(process, context):
    return ('explanation' in context.state) and ('draft' in context.state)


class SubmitAmendment(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 6
    title = _('Prepare amendments')
    submission_title = _('Submit amendments')
    context = IAmendment
    roles_validation = pub_roles_validation
    processsecurity_validation = pub_processsecurity_validation
    state_validation = pub_state_validation

    def _get_amendment_text(self, context, group):
        items = [str(e['oid']) for e in group]
        soup = BeautifulSoup(context.text_diff)
        allexplanations = soup.find_all('span', {'id': 'explanation'})
        explanations = [tag for tag in allexplanations
                        if tag['data-item'] not in items]
        blocstodel = ('span', {'id': 'explanation_action'})
        soup = html_diff_wrapper.include_diffs(
            soup, explanations,
            "ins", "del", blocstodel)
        explanations = [tag for tag in allexplanations
                        if tag['data-item'] in items]
        soup = html_diff_wrapper.include_diffs(
            soup, explanations,
            "del", "ins", blocstodel)
        allmodal = [m for m in soup.find_all('div', {'class': 'modal'})
                    if m['id'].endswith("explanation_modal")]
        for modal in allmodal:
            modal.extract()

        text = html_diff_wrapper.soup_to_text(soup)
        return text

    def _get_explanation_data(self, context, group):
        data = {
            'title': group['title'],
            'text': self._get_amendment_text(context, group['explanations']),
            # 'description': context.description,
            'justification': group.get('justification', ''),
            # 'keywords': context.keywords
        }
        return data

    def _add_sub_amendment(self, context, request, group):
        data = self._get_explanation_data(context, group)
        amendment = Amendment()
        amendment.set_data(data)
        context.proposal.addtoproperty('amendments', amendment)
        amendment.state.append('submitted')
        grant_roles(roles=(('Owner', amendment), ))
        amendment.setproperty('author', get_current())
        explanations = sorted(group['explanations'], key=lambda e: e['oid'])
        for index, explanation in enumerate(explanations):
            oid = index + 1
            explanation['oid'] = oid
            amendment.explanations[str(oid)] = explanation

        explanations, text_diff = get_text_amendment_diff_submitted(
            amendment, request)
        amendment.explanations = PersistentDict(explanations)
        amendment.text_diff = text_diff
        amendment.reindex()

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
        not_published_ideas = []
        if not request.moderate_ideas and\
           'idea' not in request.content_to_examine:
            not_published_ideas = [i for i in context.get_used_ideas()
                                   if 'published' not in i.state]
            publish_ideas(not_published_ideas, request)

        if len(groups) == 1:
            group = groups[0]
            data = self._get_explanation_data(context, group)
            # data.pop('description')
            data.pop('text')
            context.set_data(data)
            context.state.append('submitted')
            explanations, text_diff = get_text_amendment_diff_submitted(
                context, request)
            context.explanations = PersistentDict(explanations)
            context.text_diff = text_diff
        else:
            for group in groups:
                self._add_sub_amendment(context, request, group)

            context.state.append('archived')

        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        not_published_ideas.extend(context)
        request.registry.notify(ActivityExecuted(
            self, not_published_ideas, get_current()))
        alert('internal', [request.root], context.proposal.working_group.members,
              internal_kind=InternalAlertKind.working_group_alert, alert_kind='new_amendments',
              subjects=[context.proposal])
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context.proposal, "@@index"))


def comm_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal))


def comm_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def comm_state_validation(process, context):
    return 'submitted' in context.state


class CommentAmendment(CommentIdea):
    isSequential = False
    context = IAmendment
    roles_validation = comm_roles_validation
    processsecurity_validation = comm_processsecurity_validation
    state_validation = comm_state_validation

    def _get_users_to_alerts(self, context, request):
        return getattr(
            context.proposal, 'authors', [])


def present_roles_validation(process, context):
    return has_role(role=('Participant', context.proposal))


def present_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def present_state_validation(process, context):
    return 'submitted' in context.state


class PresentAmendment(PresentIdea):
    context = IAmendment
    roles_validation = present_roles_validation
    processsecurity_validation = present_processsecurity_validation
    state_validation = present_state_validation


def associate_processsecurity_validation(process, context):
    return (has_role(role=('Owner', context)) or \
            ('submitted' in context.state and has_role(role=('Member',)))) and \
           global_user_processsecurity(process, context)


class Associate(AssociateIdea):
    context = IAmendment
    processsecurity_validation = associate_processsecurity_validation


def get_access_key(obj):
    result = []
    if 'submitted' in obj.state:
        result = serialize_roles(
            (('Participant', obj.proposal), 'Admin', 'Moderator'))
    elif 'draft' in obj.state:
        result = serialize_roles(
            (('Owner', obj), 'Admin'))

    return result


def seeamendment_processsecurity_validation(process, context):
    return ('submitted' in context.state and \
            has_any_roles(roles=(('Participant', context.proposal), 'Moderator'))) or \
           ('draft' in context.state and has_role(role=('Owner', context))) or \
           has_any_roles(roles=('Admin',))


@access_action(access_key=get_access_key)
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
