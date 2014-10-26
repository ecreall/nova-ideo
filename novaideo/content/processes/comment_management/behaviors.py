# -*- coding: utf8 -*-
from zope.interface import Interface

from pyramid.httpexceptions import HTTPFound
from substanced.util import find_service, get_oid

from dace.util import getSite
from dace.objectofcollaboration.principal.util import grant_roles, has_role, get_current
from dace.processinstance.activity import (
    ElementaryAction,
    LimitedCardinality,
    InfiniteCardinality,
    ActionType,
    StartStep,
    EndStep)
from pontus.schema import select, omit

from novaideo.content.interface import IInvitation
from novaideo.content.person import Person
from novaideo.content.interface import IComment
from novaideo import _


validation_by_context = {} #TODO Proposals


def respond_relation_validation(process, context):
    subject = context.subject
    try:
        if subject.__class__ in validation_by_context:
            comment_action = validation_by_context[subject.__class__]
            return comment_action.relation_validation.__func__(process, subject)
    except Exception:
        return True


def respond_roles_validation(process, context):
    subject = context.subject
    try:
        if subject.__class__ in validation_by_context:
            comment_action = validation_by_context[subject.__class__]
            return comment_action.roles_validation.__func__(process, subject)
    except Exception:
        return True


def respond_processsecurity_validation(process, context):
    subject = context.subject
    try:
        if subject.__class__ in validation_by_context:
            comment_action = validation_by_context[subject.__class__]
            return comment_action.processsecurity_validation.__func__(process, subject)
    except Exception:
        return True


def respond_state_validation(process, context):
    subject = context.subject
    try:
        if subject.__class__ in validation_by_context:
            comment_action = validation_by_context[subject.__class__]
            return comment_action.state_validation.__func__(process, subject)
    except Exception:
        return True


class Respond(InfiniteCardinality):
    title = _('Replay')
    access_controled = True
    context = IComment
    relation_validation = respond_relation_validation
    roles_validation = respond_roles_validation
    processsecurity_validation = respond_processsecurity_validation
    state_validation = respond_state_validation

    def start(self, context, request, appstruct, **kw):
        comment = appstruct['_object_data']
        context.addtoproperty('comments', comment)
        user = get_current()
        comment.setproperty('author', user)
        self.newcontext = comment.subject
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(self.newcontext, '@@index'))


#TODO behaviors
