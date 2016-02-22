# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    has_role,
    grant_roles,
    get_current,
    has_any_roles)
from dace.processinstance.activity import (
    InfiniteCardinality,
    ActionType)
from dace.processinstance.core import ActivityExecuted

from ..user_management.behaviors import (
    global_user_processsecurity,
    access_user_processsecurity)
from novaideo.content.interface import INovaIdeoApplication, IFile
from novaideo.core import access_action, serialize_roles
from novaideo import _, DEFAULT_FILES


def get_access_key(obj):
    if 'published' in obj.state:
        return ['always']
    else:
        result = serialize_roles(
            (('Owner', obj), 'Moderator'))
        return result


def seefile_processsecurity_validation(process, context):
    application_files = [f.get('name') for f in DEFAULT_FILES]
    is_application_file = context.__name__ in application_files
    return (is_application_file or \
            access_user_processsecurity(process, context)) and \
          ('published' in context.state or \
           has_any_roles(roles=(('Owner', context), 'Moderator')))


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
    style_order = 99
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = createfile_roles_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        newfile = appstruct['_object_data']
        root.addtoproperty('files', newfile)
        newfile.state = PersistentList(['draft'])
        grant_roles(user=user, roles=(('Owner', newfile), ))
        newfile.setproperty('author', user)
        newfile.reindex()
        request.registry.notify(ActivityExecuted(self, [newfile], user))
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
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        request.registry.notify(
            ActivityExecuted(self, [context], get_current()))
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
    style_order = 99
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seefiles_roles_validation
    processsecurity_validation = seefiles_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def states_roles_validation(process, context):
    return has_any_roles(roles=('Moderator', ('Owner', context)))


def publish_state_validation(process, context):
    return 'draft' in context.state


class Publish(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 5
    submission_title = _('Continue')
    context = IFile
    roles_validation = states_roles_validation
    state_validation = publish_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state = PersistentList(['published'])
        context.reindex()
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def private_state_validation(process, context):
    return 'published' in context.state


class Private(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-step-backward'
    style_order = 5
    submission_title = _('Continue')
    context = IFile
    roles_validation = states_roles_validation
    state_validation = private_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state = PersistentList(['draft'])
        context.reindex()
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors
