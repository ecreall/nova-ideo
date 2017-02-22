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
from novaideo.content.interface import (
    INovaIdeoApplication, IOrganization, IPerson)
from novaideo.content.organization import Organization
from novaideo import _, nothing
from ..user_management.behaviors import global_user_processsecurity
from novaideo.core import access_action, serialize_roles


def add_roles_validation(process, context):
    return False#has_role(role=('Moderator',))


def add_processsecurity_validation(process, context):
    return global_user_processsecurity()


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
    return global_user_processsecurity()


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
            organization.state.append('published')
            root.addtoproperty('organizations', organization)
            organization.reindex()
            #send mail
        request.registry.notify(ActivityExecuted(
            self, new_organizations, get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@seeorganizations'))


def edit_roles_validation(process, context):
    return has_role(role=('SiteAdmin',))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity() and \
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
            members = organization.members
            for manager in organization.managers:
                if manager not in members:
                    organization.addtoproperty('members', manager)

            organization.modified_at = datetime.datetime.now(tz=pytz.UTC)
            organization.reindex()

        request.registry.notify(ActivityExecuted(
            self, appstruct['organizations'], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@seeorganizations'))


def seeorgs_roles_validation(process, context):
    return has_role(role=('Collaborator',))


def seeorgs_processsecurity_validation(process, context):
    return global_user_processsecurity()


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
    return global_user_processsecurity() and \
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
    return global_user_processsecurity()


class EditOrganization(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_interaction = 'ajax-action'
    isSequential = False
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    title = _('Edit')
    submission_title = _('Save')
    context = IOrganization
    roles_validation = editorg_roles_validation
    processsecurity_validation = editorg_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        organization = appstruct['_object_data']
        members = organization.members
        for manager in organization.managers:
            if manager not in members:
                organization.addtoproperty('members', manager)

        organization.modified_at = datetime.datetime.now(tz=pytz.UTC)
        organization.reindex()
        request.registry.notify(ActivityExecuted(
            self, [organization], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def rmorg_processsecurity_validation(process, context):
    return global_user_processsecurity()


class RemoveOrganization(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_interaction = 'ajax-action'
    style_order = 4
    submission_title = _('Continue')
    context = IOrganization
    roles_validation = editorg_roles_validation
    processsecurity_validation = rmorg_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        root.delfromproperty('organizations', context)
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(request.root, "@@seeorganizations"))


class AddMembers(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'typcn typcn-user-add'
    style_interaction = 'ajax-action'
    style_order = 2
    submission_title = _('Continue')
    context = IOrganization
    roles_validation = editorg_roles_validation
    processsecurity_validation = editorg_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        members = appstruct['members']
        are_managers = appstruct['are_managers']
        for member in members:
            new_member = False
            if member not in context.members:
                context.addtoproperty('members', member)
                new_member = True

            if are_managers and (new_member or not has_role(
                    user=member,
                    role=('OrganizationResponsible', context),
                    ignore_superiors=True)):
                grant_roles(
                    user=member,
                    roles=(('OrganizationResponsible',
                            context),))
            member.reindex()

        context.reindex()
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def rmmembers_processsecurity_validation(process, context):
    return context.members and global_user_processsecurity()


class RemoveMembers(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'typcn typcn-user-delete'
    style_interaction = 'ajax-action'
    style_order = 3
    submission_title = _('Continue')
    context = IOrganization
    roles_validation = editorg_roles_validation
    processsecurity_validation = rmmembers_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        members = appstruct['members']
        for member in members:
            if member in context.members:
                context.delfromproperty('members', member)
                if has_role(user=member,
                    role=('OrganizationResponsible', context),
                    ignore_superiors=True):
                    revoke_roles(
                        user=member,
                        roles=(('OrganizationResponsible', context), ))
            member.reindex()

        context.reindex()
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def usereditorg_roles_validation(process, context):
    return has_role(role=('Moderator',))


def usereditorg_processsecurity_validation(process, context):
    return 'active' in context.state and global_user_processsecurity()


class UserEditOrganization(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-home'
    style_interaction = 'ajax-action'
    style_order = 3
    submission_title = _('Save')
    context = IPerson
    roles_validation = usereditorg_roles_validation
    processsecurity_validation = usereditorg_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        organization = appstruct['organization']
        if organization:
            is_manager = appstruct['ismanager']
            context.set_organization(organization)
            if is_manager:
                grant_roles(
                    user=context,
                    roles=(('OrganizationResponsible',
                            organization),))
            else:
                revoke_roles(
                    user=context,
                    roles=(('OrganizationResponsible',
                            organization),))

            context.reindex()
            context.modified_at = datetime.datetime.now(tz=pytz.UTC)
            request.registry.notify(ActivityExecuted(
                self, [context], get_current()))

        return {}

    def redirect(self, context, request, **kw):
        return nothing


def withdraw_roles_validation(process, context):
    organization = context.organization
    if organization:
        return has_role(role=('Moderator',)) or \
               has_role(role=('OrganizationResponsible', organization))

    return False


def withdraw_processsecurity_validation(process, context):
    return context.organization and global_user_processsecurity()


class WithdrawUser(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'typcn typcn-user-add'
    style_interaction = 'ajax-action'
    style_order = 4
    submission_title = _('Continue')
    context = IPerson
    roles_validation = withdraw_roles_validation
    processsecurity_validation = withdraw_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        context.set_organization(None)
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return nothing



#TODO behaviors
