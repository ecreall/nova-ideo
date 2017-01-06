# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the 
Proposal management process definition. 
"""
import pytz
import datetime
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound

import html_diff_wrapper
from dace.util import (
    getSite)
from dace.objectofcollaboration.principal.util import (
    has_role,
    get_current)
#from dace.objectofcollaboration import system
from dace.processinstance.activity import (
    InfiniteCardinality, ActionType, ElementaryAction)

from novaideo.content.alert import InternalAlertKind
from novaideo.utilities.alerts_utility import alert_comment_nia
from novaideo.utilities.util import diff_analytics
from novaideo.content.interface import IProposal
from ...user_management.behaviors import global_user_processsecurity
from novaideo import _
from ...proposal_management.behaviors import add_attached_files


def correct_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def correct_roles_validation(process, context):
    return has_role(role=('Participant', context))


def correct_processsecurity_validation(process, context):
    return global_user_processsecurity()


def correct_state_validation(process, context):
    working_group = context.working_group
    return working_group and 'active' in working_group.state and\
           'amendable' in context.state


class CorrectProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    submission_title = _('Save')
    context = IProposal
    processs_relation_id = 'proposal'
    relation_validation = correct_relation_validation
    roles_validation = correct_roles_validation
    processsecurity_validation = correct_processsecurity_validation
    state_validation = correct_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        related_ideas = appstruct.pop('related_ideas')
        add_files = appstruct.pop('add_files')
        copy_of_proposal = context.get_version(user, (context, 'version'))
        context.working_group.init_nonproductive_cycle()
        context.state = PersistentList(['amendable', 'published'])
        context.set_data(appstruct)
        context.text = html_diff_wrapper.normalize_text(
            context.text)
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.set_related_ideas(
            related_ideas, user)
        # Add Nia comment
        alert_comment_nia(
            context, request, getSite(),
            internal_kind=InternalAlertKind.working_group_alert,
            subject_type='proposal',
            alert_kind='new_version',
            diff=diff_analytics(
                copy_of_proposal, context, ['title', 'text', 'description'])
            )
        add_attached_files({'add_files': add_files}, context)
        context.reindex()
        return {'newcontext': context}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def close_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def close_roles_validation(process, context):
    return has_role(role=('System',))


def close_state_validation(process, context):
    wg = context.working_group
    return wg and 'active' in wg.state and 'amendable' in context.state


class CloseWork(ElementaryAction):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_order = 4
    context = IProposal
    actionType = ActionType.system
    processs_relation_id = 'proposal'
    roles_validation = close_roles_validation
    relation_validation = close_relation_validation
    state_validation = close_state_validation

    def start(self, context, request, appstruct, **kw):
        #TODO
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#TODO behaviors
