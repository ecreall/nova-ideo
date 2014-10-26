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

from novaideo.content.correlation import Correlation
from novaideo.content.interface import ICorrelation
from novaideo import _
from ..user_management.behaviors import global_user_processsecurity
from ..comment_management.behaviors import validation_by_context
from novaideo.core import can_access, acces_action



def comm_roles_validation(process, context):
    return has_role(role=('Member',))


def comm_processsecurity_validation(process, context):
    if not global_user_processsecurity(process, context):
        return False

    source = context.source
    targets = context.targets
    user = get_current()
    root = getSite()
    for target in targets:
        if not can_access(user, target, None, root):
            return False

    return can_access(user, source, None, root)


class CommentCorrelation(InfiniteCardinality):
    isSequential = False
    context = ICorrelation
    roles_validation = comm_roles_validation
    processsecurity_validation = comm_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        comment = appstruct['_object_data']
        context.addtoproperty('comments', comment)
        user = get_current()
        comment.setproperty('author', user)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def see_processsecurity_validation(process, context):
    source = context.source
    targets = context.targets
    user = get_current()
    root = getSite()
    for target in targets:
        if not can_access(user, target, None, root):
            return False

    return can_access(user, source, None, root)


@acces_action()
class SeeCorrelation(InfiniteCardinality):
    title = _('Details')
    context = ICorrelation
    actionType = ActionType.automatic
    processsecurity_validation = see_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors
validation_by_context[Correlation] = CommentCorrelation
