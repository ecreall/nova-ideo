# -*- coding: utf8 -*-
import datetime
from pyramid.httpexceptions import HTTPFound

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
from novaideo.core import acces_action, can_access, FileEntity
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
        user.delproperty('selections', context)
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
    return has_role(role=('Admin',))


class CreateFile(InfiniteCardinality):
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
    return has_role(role=('Admin', ))


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


#TODO behaviors
