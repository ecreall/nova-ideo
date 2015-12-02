# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    has_role,
    grant_roles,
    get_current)
from dace.processinstance.activity import (
    InfiniteCardinality,
    ActionType)

from ..user_management.behaviors import global_user_processsecurity
from novaideo.content.interface import INovaIdeoApplication, IFile
from novaideo.core import access_action
from novaideo import _


def get_access_key(obj):
    return ['always']


def seefile_processsecurity_validation(process, context):
    return True


@access_action(access_key=get_access_key)
class SeeFile(InfiniteCardinality):
    """SeeFile is the behavior allowing access to context"""
    title = _('Details')
    context = IFile
    actionType = ActionType.automatic
    processsecurity_validation = seefile_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

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
        return {'newcontext': newfile}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


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
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def seefiles_roles_validation(process, context):
    return has_role(role=('Moderator', ))


def seefiles_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class SeeFiles(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-file'
    style_order = -1
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seefiles_roles_validation
    processsecurity_validation = seefiles_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


#TODO behaviors
