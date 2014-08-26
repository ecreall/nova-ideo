# -*- coding: utf8 -*-
from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import grant_roles, has_any_roles, get_current
from dace.processinstance.activity import (
    ElementaryAction,
    LimitedCardinality,
    InfiniteCardinality,
    ActionType,
    StartStep,
    EndStep)
from pontus.view import BasicView
from pontus.schema import select, omit

from novaideo.content.interface import INovaIdeoApplication, IProposal
from novaideo import _
from ..user_management.behaviors import global_user_processsecurity
from novaideo.core import acces_action

def seeideas_relation_validation(process, context):
    return True


def seeideas_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def seeideas_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and len(context.ideas)>=1


def seeideas_state_validation(process, context):
    return True


class SeeIdeas(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    relation_validation = seeideas_relation_validation
    roles_validation = seeideas_roles_validation
    processsecurity_validation = seeideas_processsecurity_validation
    state_validation = seeideas_state_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def search_processsecurity_validation(process, context):
    return True

@acces_action()
class Search(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    actionType = ActionType.automatic
    processsecurity_validation = search_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        self.content_types = appstruct['content_types']
        self.text = appstruct['text']
        return True

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root, query={'text': self.text, 'content_types': ",".join(self.content_types)}))

#see
def seemy_relation_validation(process, context):
    return True


def seemy_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def seemy_processsecurity_validation(process, context):
    user = get_current()
    return global_user_processsecurity(process, context) and getattr(user, 'ideas', [])


def seemy_state_validation(process, context):
    return True


def seemyc_processsecurity_validation(process, context):
    user = get_current()
    return global_user_processsecurity(process, context) and \
           (getattr(user, 'proposals', []) or getattr(user, 'ideas', []))

class SeeMyContents(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    relation_validation = seemy_relation_validation
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemyc_processsecurity_validation
    state_validation = seemy_state_validation

    def start(self, context, request, appstruct, **kw):
        return True

def seemys_processsecurity_validation(process, context):
    user = get_current()
    return global_user_processsecurity(process, context) and \
           (getattr(user, 'selections', []) or getattr(user, 'contacts', []))


class SeeMySelections(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    relation_validation = seemy_relation_validation
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemys_processsecurity_validation
    state_validation = seemy_state_validation

    def start(self, context, request, appstruct, **kw):
        return True


def seemypa_processsecurity_validation(process, context):
    user = get_current()
    return global_user_processsecurity(process, context) and getattr(user, 'participations', [])


class SeeMyParticipations(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    relation_validation = seemy_relation_validation
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemypa_processsecurity_validation
    state_validation = seemy_state_validation

    def start(self, context, request, appstruct, **kw):
        return True


def seemysu_processsecurity_validation(process, context):
    user = get_current()
    return global_user_processsecurity(process, context) and getattr(user, 'supports', [])


class SeeMySupports(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    relation_validation = seemy_relation_validation
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemysu_processsecurity_validation
    state_validation = seemy_state_validation

    def start(self, context, request, appstruct, **kw):
        return True

def seeproposal_processsecurity_validation(process, context):
    return has_any_roles(roles=(('Owner', context),)) or \
           not ('draft' in context.state)


@acces_action()
class SeeProposal(InfiniteCardinality):
    title = _('Details')
    context = IProposal
    actionType = ActionType.automatic
    processsecurity_validation = seeproposal_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors
