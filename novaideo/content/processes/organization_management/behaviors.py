# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    has_role, grant_roles, revoke_roles, get_current)
from dace.processinstance.activity import (
    InfiniteCardinality,
    ActionType)
from dace.processinstance.core import ActivityExecuted

from novaideo.ips.xlreader import create_object_from_xl
from novaideo.content.interface import INovaIdeoApplication, IOrganization
from novaideo.content.organization import Organization
from novaideo import _
from ..user_management.behaviors import global_user_processsecurity
from novaideo.core import access_action, serialize_roles



def add_roles_validation(process, context):
    return False#has_role(role=('Moderator',))


def add_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class AddOrganizations(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-home'
    style_order = 1
    submission_title = _('Save')
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = add_roles_validation
    processsecurity_validation = add_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        xlfile = appstruct['file']['_object_data']
        organizations = create_object_from_xl(
            file=xlfile,
            factory=Organization,
            properties={'title': ('String', False),
                        'description': ('String', False)})
        root.setproperty('organizations', organizations)
        request.registry.notify(ActivityExecuted(
            self, organizations, get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def creatorg_roles_validation(process, context):
    return has_role(role=('Moderator',))


def creatorg_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class CreatOrganizations(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-home'
    style_order = 2
    submission_title = _('Save')
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = creatorg_roles_validation
    processsecurity_validation = creatorg_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        new_organizations = appstruct['organizations']
        for organization_dict in new_organizations:
            organization = organization_dict['_object_data']
            root.addtoproperty('organizations', organization)
            #send mail
        request.registry.notify(ActivityExecuted(
            self, new_organizations, get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@seeorganizations'))


def edit_roles_validation(process, context):
    return has_role(role=('Admin',))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           context.organizations


class EditOrganizations(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-home'
    style_order = 4
    submission_title = _('Save')
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        for org_struct in appstruct['organizations']:
            organization = org_struct['_object_data']
            organization.modified_at = datetime.datetime.now(tz=pytz.UTC)

        request.registry.notify(ActivityExecuted(
            self, appstruct['organizations'], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@seeorganizations'))


def seeorgs_roles_validation(process, context):
    return has_role(role=('Collaborator',))


def seeorgs_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class SeeOrganizations(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-home'
    style_order = 3
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seeorgs_roles_validation
    processsecurity_validation = seeorgs_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def get_access_key(obj):
    return serialize_roles(
            ('Member',))


def see_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           has_role(role=('Member',))


@access_action(access_key=get_access_key)
class SeeOrganization(InfiniteCardinality):
    isSequential = False
    title = _('Details')
    actionType = ActionType.automatic
    context = IOrganization
    processsecurity_validation = see_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def editorg_roles_validation(process, context):
    return has_role(role=('Moderator',)) or \
           has_role(role=('OrganizationResponsible', context))


def editorg_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class EditOrganization(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    isSequential = False
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    title = _('Edit organization')
    submission_title = _('Save')
    context = IOrganization
    roles_validation = editorg_roles_validation
    processsecurity_validation = editorg_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        organization = appstruct['_object_data']
        organization.modified_at = datetime.datetime.now(tz=pytz.UTC)
        request.registry.notify(ActivityExecuted(
            self, [organization], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors
