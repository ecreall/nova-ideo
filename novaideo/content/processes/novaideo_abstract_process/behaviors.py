# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
from pyramid.httpexceptions import HTTPFound
from persistent.list import PersistentList

from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    has_role, 
    grant_roles, 
    get_current)
from dace.interfaces import IEntity
from dace.processinstance.activity import (
    InfiniteCardinality,
    ActionType)

from ..user_management.behaviors import global_user_processsecurity
from novaideo.content.interface import INovaIdeoApplication, IFile
from novaideo.core import acces_action, can_access
from novaideo import _



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
        user.delfromproperty('selections', context)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@index'))


def seefile_processsecurity_validation(process, context):
    return True


@acces_action()
class SeeFile(InfiniteCardinality):
    """SeeFile is the behavior allowing access to context"""
    title = _('Details')
    context = IFile
    actionType = ActionType.automatic
    processsecurity_validation = seefile_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def createfile_roles_validation(process, context):
    return has_role(role=('Moderator',))


class CreateFile(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-file'
    style_order = 0
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = createfile_roles_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        newfile = appstruct['_object_data']
        root.addtoproperty('files', newfile)
        newfile.state.append('published')
        grant_roles(roles=(('Owner', newfile), ))
        newfile.setproperty('author', get_current())
        newfile.reindex()
        self.newcontext = newfile
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(self.newcontext, "@@index"))


def edit_roles_validation(process, context):
    return has_role(role=('Moderator', ))


class EditFile(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    submission_title = _('Save')
    context = IFile
    roles_validation = edit_roles_validation

    def start(self, context, request, appstruct, **kw):
        context.modified_at = datetime.datetime.today()
        context.reindex()
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def seefiles_roles_validation(process, context):
    return has_role(role=('Moderator', ))


def seefiles_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class SeeFiles(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-th-list'
    style_order = -1
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seefiles_roles_validation
    processsecurity_validation = seefiles_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def adddeadline_processsecurity_validation(process, context):
    return datetime.datetime.today() >= context.deadlines[-1].replace(tzinfo=None) and \
           global_user_processsecurity(process, context)


class AddDeadLine(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-time'
    style_order = 9
    submission_title = _('Save')
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seefiles_roles_validation
    processsecurity_validation = adddeadline_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        if hasattr(context, 'deadlines'):
            context.deadlines.append(appstruct['deadline'])
        else:
            context.deadlines = PersistentList([appstruct['deadline']])

        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def editdeadline_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           getattr(context, 'deadlines', [])


class EditDeadLine(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-time'
    style_order = 9
    submission_title = _('Save')
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seefiles_roles_validation
    processsecurity_validation = editdeadline_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        current = context.deadlines[-1]
        context.deadlines.remove(current)
        context.deadlines.append(appstruct['deadline'])
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def seeproposals_roles_validation(process, context):
    return has_role(role=('Moderator', ))


def seeproposals_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class SeeOrderedProposal(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-th-list'
    style_order = -2
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seeproposals_roles_validation
    processsecurity_validation = seeproposals_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))

#TODO behaviors
