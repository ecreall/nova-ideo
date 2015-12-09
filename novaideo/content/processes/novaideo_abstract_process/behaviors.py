# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import pytz
import datetime
from pyramid.httpexceptions import HTTPFound
from persistent.list import PersistentList

from dace.objectofcollaboration.principal.util import (
    has_role,
    get_current)
from dace.interfaces import IEntity
from dace.processinstance.activity import InfiniteCardinality

from ..user_management.behaviors import global_user_processsecurity
from novaideo.content.interface import INovaIdeoApplication
from novaideo import _


def select_roles_validation(process, context):
    return has_role(role=('Member',))


def select_processsecurity_validation(process, context):
    user = get_current()
    return not (context in getattr(user, 'selections', [])) and \
           global_user_processsecurity(process, context)


class SelectEntity(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-star-empty'
    style_order = 100
    isSequential = False
    context = IEntity
    roles_validation = select_roles_validation
    processsecurity_validation = select_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        user.addtoproperty('selections', context)
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@index'))


def deselect_roles_validation(process, context):
    return has_role(role=('Member',))


def deselect_processsecurity_validation(process, context):
    user = get_current()
    return (context in getattr(user, 'selections', [])) and \
           global_user_processsecurity(process, context)


def deselect_state_validation(process, context):
    return True


class DeselectEntity(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-star'
    style_order = 101
    isSequential = False
    context = IEntity
    roles_validation = deselect_roles_validation
    processsecurity_validation = deselect_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        user.delfromproperty('selections', context)
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@index'))


def deadline_roles_validation(process, context):
    return has_role(role=('Examiner', ))


def adddeadline_processsecurity_validation(process, context):
    return getattr(context, 'content_to_examine', []) and\
           datetime.datetime.now(tz=pytz.UTC) >= \
           context.deadlines[-1].replace(tzinfo=pytz.UTC) and \
           global_user_processsecurity(process, context)


class AddDeadLine(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-time'
    style_order = 9
    submission_title = _('Save')
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = deadline_roles_validation
    processsecurity_validation = adddeadline_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        if hasattr(context, 'deadlines'):
            context.deadlines.append(appstruct['deadline'])
        else:
            context.deadlines = PersistentList([appstruct['deadline']])

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def editdeadline_processsecurity_validation(process, context):
    return getattr(context, 'content_to_examine', []) and\
           global_user_processsecurity(process, context) and \
           getattr(context, 'deadlines', [])


class EditDeadLine(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-time'
    style_order = 9
    submission_title = _('Save')
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = deadline_roles_validation
    processsecurity_validation = editdeadline_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        current = context.deadlines[-1]
        context.deadlines.remove(current)
        context.deadlines.append(appstruct['deadline'])
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))

#TODO behaviors
