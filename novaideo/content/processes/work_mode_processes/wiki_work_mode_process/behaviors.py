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
    getSite,
    copy)
from dace.objectofcollaboration.principal.util import (
    has_role,
    get_current)
#from dace.objectofcollaboration import system
from dace.processinstance.activity import (
    InfiniteCardinality, ActionType, ElementaryAction)

from novaideo.content.interface import IProposal
from ...user_management.behaviors import global_user_processsecurity
from novaideo import _
from novaideo.content.correlation import CorrelationType
from novaideo.utilities.util import connect
from ...proposal_management.behaviors import add_attached_files


try:
    basestring
except NameError:
    basestring = str


def correct_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def correct_roles_validation(process, context):
    return has_role(role=('Participant', context))


def correct_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def correct_state_validation(process, context):
    return 'active' in context.working_group.state and\
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

    def _get_newversion(self, context, root, wg):
        contextname = context.__name__
        copy_of_proposal = copy(context,
                                (root, 'proposals'),
                                new_name=context.__name__,
                                omit=('created_at', 'modified_at'),
                                roles=True)
        copy_of_proposal.setproperty('version', context)
        copy_of_proposal.setproperty('originalentity', context.originalentity)
        root.rename(copy_of_proposal.__name__, contextname)
        copy_of_proposal.state = PersistentList(['amendable', 'published'])
        copy_of_proposal.setproperty('author', context.author)
        copy_of_proposal.setproperty('comments', context.comments)
        self.process.attachedTo.process.execution_context.add_created_entity(
            'proposal', copy_of_proposal)
        wg.setproperty('proposal', copy_of_proposal)
        self.process.reindex()
        return copy_of_proposal

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        wg = context.working_group
        related_ideas = appstruct.pop('related_ideas')
        add_files = appstruct.pop('add_files')
        copy_of_proposal = self._get_newversion(context, root, wg)
        context.state = PersistentList(['version', 'archived'])
        copy_of_proposal.set_data(appstruct)
        copy_of_proposal.text = html_diff_wrapper.normalize_text(
            copy_of_proposal.text)
        copy_of_proposal.modified_at = datetime.datetime.now(tz=pytz.UTC)
        #correlation idea of replacement ideas... del replaced_idea
        connect(copy_of_proposal,
                related_ideas,
                {'comment': _('Add related ideas'),
                 'type': _('New version')},
                user,
                ['related_proposals', 'related_ideas'],
                CorrelationType.solid)
        add_attached_files({'add_files': add_files}, copy_of_proposal)
        copy_of_proposal.reindex()
        context.reindex()
        return {'newcontext': copy_of_proposal}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def close_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def close_roles_validation(process, context):
    return has_role(role=('System',))


def close_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'amendable' in context.state


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
