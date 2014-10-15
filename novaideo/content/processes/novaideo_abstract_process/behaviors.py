# -*- coding: utf8 -*-
from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.interfaces import IEntity
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

from novaideo.content.interface import INovaIdeoApplication
from novaideo import _
from ..user_management.behaviors import global_user_processsecurity
from novaideo.core import acces_action, can_access



def select_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def select_processsecurity_validation(process, context):
    user =  get_current()
    return global_user_processsecurity(process, context) and can_access(user, context) and not (context in getattr(user, 'selections', [])) 


class SelectEntity(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-star-empty'
    style_order = 100
    isSequential = False
    context = IEntity
    roles_validation = select_roles_validation
    processsecurity_validation = select_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        user =  get_current()
        user.addtoproperty('selections', context)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@index'))



def deselect_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def deselect_processsecurity_validation(process, context):
    user =  get_current()
    return global_user_processsecurity(process, context) and can_access(user, context) and (context in getattr(user, 'selections', [])) 


def deselect_state_validation(process, context):
    return True

class DeselectEntity(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-star'
    style_order = 101
    isSequential = False
    context = IEntity
    roles_validation = deselect_roles_validation
    processsecurity_validation = deselect_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        user =  get_current()
        user.delproperty('selections', context)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@index'))

#TODO behaviors
