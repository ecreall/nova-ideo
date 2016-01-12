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
    has_any_roles,
    grant_roles,
    get_current)
from dace.processinstance.activity import (
    InfiniteCardinality,
    ActionType)

from ..user_management.behaviors import (
    global_user_processsecurity,
    access_user_processsecurity)
from novaideo.content.interface import (
    INovaIdeoApplication,
    IWebAdvertising,
    IAdvertising)
from novaideo.core import access_action, serialize_roles
from novaideo import _


def get_access_key(obj):
    if 'published' in obj.state:
        return ['always']
    else:
        result = serialize_roles(
            (('Owner', obj), 'Moderator'))
        return result


def seewebadvertising_processsecurity_validation(process, context):
    return access_user_processsecurity(process, context) and \
          ('published' in context.state or \
           has_any_roles(
            roles=(('Owner', context), 'Moderator')))


@access_action(access_key=get_access_key)
class SeeWebAdvertising(InfiniteCardinality):
    """SeeFile is the behavior allowing access to context"""
    title = _('Details')
    context = IWebAdvertising
    actionType = ActionType.automatic
    processsecurity_validation = seewebadvertising_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def createwebadvertising_roles_validation(process, context):
    return has_role(role=('Moderator',))


class CreateWebAdvertising(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-picture'
    style_order = 100
    title = _('Create an announcement')
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = createwebadvertising_roles_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        newadvertising = appstruct['_object_data']
        root.addtoproperty('advertisings', newadvertising)
        newadvertising.state.append('editable')
        grant_roles(roles=(('Owner', newadvertising), ))
        newadvertising.setproperty('author', get_current())
        newadvertising.reindex()
        return {'newcontext': newadvertising}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def edit_roles_validation(process, context):
    return has_any_roles(
        roles=(('Owner', context), 'Moderator'))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def edit_state_validation(process, context):
    if 'editable' in context.state:
        return True

    return has_role(role=('Moderator', ))


class EditWebAdvertising(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    submission_title = _('Save')
    context = IWebAdvertising
    roles_validation = edit_roles_validation
    state_validation = edit_state_validation
    processsecurity_validation = edit_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        if context.picture:
            context.rename(context.picture.__name__, context.picture.title)

        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def publish_roles_validation(process, context):
    return has_any_roles(roles=('Moderator',))


def publish_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def publish_state_validation(process, context):
    return 'editable' in context.state


class PublishAdvertising(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-ok'
    style_order = 5
    submission_title = _('Continue')
    context = IAdvertising
    roles_validation = publish_roles_validation
    state_validation = publish_state_validation
    processsecurity_validation = publish_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        context.state = PersistentList(['published'])
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def archive_roles_validation(process, context):
    return has_any_roles(roles=('Moderator',))


def archive_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def archive_state_validation(process, context):
    return 'published' in context.state


class ArchiveAdvertising(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-folder-close'
    style_order = 6
    submission_title = _('Continue')
    context = IAdvertising
    roles_validation = archive_roles_validation
    state_validation = archive_state_validation
    processsecurity_validation = archive_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        context.state = PersistentList(['archived'])
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def remove_roles_validation(process, context):
    return has_any_roles(roles=('Moderator',))


def remove_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class RemoveAdvertising(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_order = 7
    submission_title = _('Continue')
    context = IAdvertising
    roles_validation = remove_roles_validation
    processsecurity_validation = remove_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        root.delfromproperty('advertisings', context)
        return {}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root, ""))


def seeads_roles_validation(process, context):
    return has_role(role=('Moderator',))


def seeads_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class SeeAdvertisings(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-picture'
    style_order = 100
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seeads_roles_validation
    processsecurity_validation = seeads_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))
#TODO behaviors
