# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the
Correlation management process definition.
"""
from pyramid.httpexceptions import HTTPFound

from dace.objectofcollaboration.principal.util import has_role, get_current
from dace.processinstance.activity import InfiniteCardinality, ActionType

from novaideo.content.correlation import Correlation
from novaideo.content.interface import ICorrelation
from novaideo import _
from ..user_management.behaviors import global_user_processsecurity
from ..comment_management import VALIDATOR_BY_CONTEXT
from novaideo.core import can_access, access_action, get_access_keys


def comm_roles_validation(process, context):
    return has_role(role=('Member',))


def comm_processsecurity_validation(process, context):
    if not global_user_processsecurity():
        return False

    source = context.source
    targets = context.targets
    user = get_current()
    return can_access(user, source) and \
           not any(not can_access(user, target) for target in targets)


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
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def get_access_key(obj):
    objs = list(obj.targets)
    objs.append(obj.source)
    result = [get_access_keys(o) for o in objs]
    result = list(set([item for sublist in result
                       for item in sublist if item != 'always']))
    if not result:
        result = ['always']

    return result


def see_processsecurity_validation(process, context):
    source = context.source
    targets = context.targets
    user = get_current()
    return can_access(user, source) and \
           not any(not can_access(user, target) for target in targets)


@access_action(access_key=get_access_key)
class SeeCorrelation(InfiniteCardinality):
    """SeeCorrelation is the behavior allowing access to context"""
    title = _('Details')
    context = ICorrelation
    actionType = ActionType.automatic
    processsecurity_validation = see_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


VALIDATOR_BY_CONTEXT[Correlation] = {
    'action': CommentCorrelation,
    'see': SeeCorrelation,
    'access_key': get_access_key
}

#TODO behaviors
