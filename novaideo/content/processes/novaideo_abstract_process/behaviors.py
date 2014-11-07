# -*- coding: utf8 -*-
from pyramid.httpexceptions import HTTPFound

from dace.interfaces import IEntity
from dace.objectofcollaboration.principal.util import has_role, get_current
from dace.processinstance.activity import InfiniteCardinality

from ..user_management.behaviors import global_user_processsecurity
from novaideo.core import can_access



def select_roles_validation(process, context):
    return has_role(role=('Member',))


def select_processsecurity_validation(process, context):
    user =  get_current()
    return can_access(user, context) and \
           not (context in getattr(user, 'selections', [])) and \
           global_user_processsecurity(process, context)


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
    return has_role(role=('Member',))


def deselect_processsecurity_validation(process, context):
    user =  get_current()
    return can_access(user, context) and \
           (context in getattr(user, 'selections', [])) and \
           global_user_processsecurity(process, context)


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
