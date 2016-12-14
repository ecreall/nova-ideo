# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import pytz
import datetime
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    has_any_roles,
    get_current,
    grant_roles,
    has_role)
from dace.processinstance.activity import (
    InfiniteCardinality,
    ActionType)

from novaideo.content.interface import (
    INovaIdeoApplication,
    ISmartFolder)
from novaideo import _, nothing
from novaideo.core import access_action, serialize_roles


def siteadmin_roles_validation(process, context):
    return has_any_roles(roles=('SiteAdmin', ))


def get_access_key(obj):
    if 'published' in obj.state:
        return ['always']
    else:
        return serialize_roles((('Owner', obj), 'SiteAdmin', 'Admin'))


def see_processsecurity_validation(process, context):
    return 'published' in context.state or \
           has_any_roles(roles=('SiteAdmin', 'Admin'))\
           or has_role(role=('Owner', context))


@access_action(access_key=get_access_key)
class SeeSmartFolder(InfiniteCardinality):
    """SeeFile is the behavior allowing access to context"""
    title = _('Details')
    context = ISmartFolder
    actionType = ActionType.automatic
    processsecurity_validation = see_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def create_roles_validation(process, context):
    return has_role(role=('Member',))


class AddSmartFolder(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-folder-open'
    style_order = 0
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = create_roles_validation

    def start(self, context, request, appstruct, **kw):
        new_smart_folder = appstruct['_object_data']
        context.addtoproperty('smart_folders', new_smart_folder)
        grant_roles(roles=(('Owner', new_smart_folder), ))
        new_smart_folder.setproperty('author', get_current())
        new_smart_folder.state = PersistentList(['private'])
        new_smart_folder.reindex()
        return {'newcontext': new_smart_folder}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def createsub_roles_validation(process, context):
    return has_any_roles(roles=('SiteAdmin', 'Admin'))\
           or has_role(role=('Owner', context))


class AddSubSmartFolder(InfiniteCardinality):
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-folder-open'
    style_interaction = 'ajax-action'
    style_order = 0
    submission_title = _('Save')
    context = ISmartFolder
    roles_validation = createsub_roles_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        new_smart_folder = appstruct['_object_data']
        root.addtoproperty('smart_folders', new_smart_folder)
        context.addtoproperty('children', new_smart_folder)
        grant_roles(roles=(('Owner', new_smart_folder), ))
        new_smart_folder.setproperty('author', get_current())
        new_smart_folder.state = PersistentList(['private'])
        new_smart_folder.filters = PersistentList(
            getattr(new_smart_folder, 'filters', []))
        new_smart_folder.reindex()
        return {'newcontext': new_smart_folder}

    def redirect(self, context, request, **kw):
        return nothing


def edit_roles_validation(process, context):
    return has_any_roles(roles=('SiteAdmin', 'Admin')) or \
        has_role(role=('Owner', context))


def edit_state_validation(process, context):
    return 'private' in context.state or \
        has_any_roles(roles=('SiteAdmin', 'Admin'))


class EditSmartFolder(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    submission_title = _('Save')
    context = ISmartFolder
    roles_validation = edit_roles_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        context.filters = PersistentList(getattr(context, 'filters', []))
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


class RemoveSmartFolder(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_order = 5
    submission_title = _('Continue')
    context = ISmartFolder
    roles_validation = edit_roles_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        sub_folders = context.all_sub_folders()
        for sub_folder in sub_folders:
            root.delfromproperty('smart_folders', sub_folder)

        root.delfromproperty('smart_folders', context)
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def siteadmin_roles_validation(process, context):
    return has_any_roles(roles=('SiteAdmin', 'Admin'))


def pub_state_validation(process, context):
    return 'private' in context.state


class PublishSmartFolder(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 2
    submission_title = _('Continue')
    context = ISmartFolder
    roles_validation = siteadmin_roles_validation
    state_validation = pub_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state = PersistentList(['published'])
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def withdraw_processsecurity_validation(process, context):
    return 'published' in context.state


class WithdrawSmartFolder(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-fast-backward'
    style_order = 2
    submission_title = _('Continue')
    context = ISmartFolder
    roles_validation = siteadmin_roles_validation
    processsecurity_validation = withdraw_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        context.state = PersistentList(['private'])
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def seesmartfolders_roles_validation(process, context):
    return has_role(role=('Member',))


class SeeSmartFolders(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-folder-open'
    style_order = 0
    context = INovaIdeoApplication
    roles_validation = seesmartfolders_roles_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def order_processsecurity_validation(process, context):
    return len(context.smart_folders) > 1 and has_any_roles(roles=('SiteAdmin', 'Admin'))


class OrderSmartFolders(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'body-action'
    style_picto = 'glyphicon glyphicon-th-list'
    style_order = 8
    template = 'novaideo:views/templates/order_smart_folders.pt'
    submission_title = _('Save')
    context = INovaIdeoApplication
    processsecurity_validation = order_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        folders = appstruct['folders']
        for index, folder in enumerate(folders):
            folder.set_order(index)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@seesmartfolders"))


def ordersub_processsecurity_validation(process, context):
    return len(context.children) > 1 and has_any_roles(roles=('SiteAdmin', 'Admin'))


class OrderSubSmartFolders(OrderSmartFolders):
    context = ISmartFolder
    processsecurity_validation = ordersub_processsecurity_validation

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors
