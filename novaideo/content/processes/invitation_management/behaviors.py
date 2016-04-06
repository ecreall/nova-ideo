# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
from pyramid.httpexceptions import HTTPFound
from substanced.util import find_service

from dace.util import getSite, name_chooser
from dace.objectofcollaboration.principal.util import (
    grant_roles, has_role, get_current, has_any_roles)
from dace.processinstance.activity import (
    InfiniteCardinality,
    ActionType)
from pontus.schema import select, omit

from novaideo.ips.xlreader import create_object_from_xl
from novaideo.content.interface import INovaIdeoApplication, IInvitation
from novaideo.content.invitation import Invitation
from novaideo import _
from novaideo.content.processes.user_management.behaviors import (
    global_user_processsecurity,
    initialize_tokens)
from novaideo.core import access_action, serialize_roles
from novaideo.utilities.util import gen_random_token
from novaideo.content.person import Person
from novaideo.content.invitation import InvitationSchema
from novaideo.role import DEFAULT_ROLES, APPLICATION_ROLES
from novaideo.utilities.alerts_utility import alert


def uploaduser_roles_validation(process, context):
    return False#has_role(role=('Moderator',))


def uploaduser_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class UploadUsers(InfiniteCardinality):
    style_descriminator = 'admin-action'
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = uploaduser_roles_validation
    processsecurity_validation = uploaduser_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current()
        xlfile = appstruct['file']['_object_data']
        new_invitations = create_object_from_xl(
            file=xlfile,
            factory=Invitation,
            properties={'first_name': ('String', False),
                        'last_name': ('String', False),
                        'user_title': ('String', False),
                        'email': ('String', False)})
        title_template = u"""{title} {user_title} {first_name} {last_name}"""
        mail_template = root.get_mail_template('invitation')
        localizer = request.localizer
        novaideo_title = root.title
        for invitation in new_invitations:
            invitation.title = title_template.format(
                title=invitation.title,
                user_title=getattr(self.context,
                                   'user_title', ''),
                first_name=getattr(self.context,
                                   'first_name', ''),
                last_name=getattr(self.context,
                                  'last_name', ''))
            invitation.state.append('pending')
            invitation.setproperty('manager', user)
            invitation.__name__ = gen_random_token()
            root.addtoproperty('invitations', invitation)
            url = request.resource_url(invitation, "")
            roles_translate = [localizer.translate(APPLICATION_ROLES.get(r, r))
                               for r in getattr(invitation, 'roles', [])]

            subject = mail_template['subject'].format(
                novaideo_title=novaideo_title
            )
            message = mail_template['template'].format(
                invitation=invitation,
                user_title=localizer.translate(_(getattr(
                            invitation, 'user_title', ''))),
                invitation_url=url,
                roles=", ".join(roles_translate),
                novaideo_title=novaideo_title)
            alert('email', [root.get_site_sender()], [invitation.email],
                  subject=subject, body=message)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def inviteuser_roles_validation(process, context):
    return has_role(role=('Moderator',)) or \
           has_role(role=('OrganizationResponsible',))


def inviteuser_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class InviteUsers(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-bullhorn'
    style_order = 5
    submission_title = _('Send')
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = inviteuser_roles_validation
    processsecurity_validation = inviteuser_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        invitations = appstruct['invitations']
        user = get_current()
        organization = getattr(user, 'organization', None)
        mail_template = root.get_mail_template('invitation')
        localizer = request.localizer
        novaideo_title = root.title
        for invitation_dict in invitations:
            invitation = invitation_dict['_object_data']
            invitation.state.append('pending')
            invitation.setproperty('manager', user)
            invitation.__name__ = gen_random_token()
            root.addtoproperty('invitations', invitation)
            if not getattr(invitation, 'roles', []):
                invitation.roles = DEFAULT_ROLES

            roles_translate = [localizer.translate(APPLICATION_ROLES.get(r, r))
                               for r in invitation.roles]
            if not invitation.organization:
                invitation.setproperty('organization', organization)

            url = request.resource_url(invitation, "")
            subject = mail_template['subject'].format(
                novaideo_title=novaideo_title
            )
            message = mail_template['template'].format(
                invitation=invitation,
                user_title=localizer.translate(_(getattr(
                    invitation, 'user_title', ''))),
                invitation_url=url,
                roles=", ".join(roles_translate),
                novaideo_title=novaideo_title)
            alert('email', [root.get_site_sender()], [invitation.email],
                  subject=subject, body=message)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@seeinvitations'))


def get_access_key(obj):
    organization = obj.organization
    result = []
    if organization:
        result = serialize_roles(
            (('OrganizationResponsible', organization),))

    result.extend(serialize_roles(
        ('Moderator', 'Anonymous')))
    return result


def seeinv_processsecurity_validation(process, context):
    organization = context.organization
    return (organization and \
            has_role(role=('OrganizationResponsible',
                           organization))) or \
            has_any_roles(roles=('Moderator',
                                'Anonymous'))


@access_action(access_key=get_access_key)
class SeeInvitation(InfiniteCardinality):
    isSequential = False
    title = _('Plus')
    actionType = ActionType.automatic
    context = IInvitation
    processsecurity_validation = seeinv_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def seeinvs_roles_validation(process, context):
    return has_any_roles(roles=('Moderator', 'OrganizationResponsible'))


def seeinvs_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class SeeInvitations(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-bullhorn'
    style_order = 6
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seeinvs_roles_validation
    processsecurity_validation = seeinvs_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def edit_roles_validation(process, context):
    return has_role(role=('Admin',))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           context.invitations


class EditInvitations(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-bullhorn'
    style_order = 7
    submission_title = _('Save')
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@seeinvitations'))


def editinv_roles_validation(process, context):
    return (context.organization and \
            has_role(role=('OrganizationResponsible',
                           context.organization))) or \
            has_role(role=('Moderator',))


def editinv_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class EditInvitation(InfiniteCardinality):
    style_picto = 'glyphicon glyphicon-pencil'
    isSequential = False
    title = _('Edit the invitation')
    submission_title = _('Save')
    context = IInvitation
    roles_validation = editinv_roles_validation
    processsecurity_validation = editinv_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def accept_roles_validation(process, context):
    return has_role(role=('Anonymous',)) and \
           not has_role(role=('Admin',))


def accept_state_validation(process, context):
    return 'pending' in context.state


class AcceptInvitation(InfiniteCardinality):
    context = IInvitation
    style_picto = 'glyphicon glyphicon-thumbs-up'
    submission_title = _('Save')
    roles_validation = accept_roles_validation
    state_validation = accept_state_validation

    def start(self, context, request, appstruct, **kw):
        datas = context.get_data(select(omit(InvitationSchema(),
                                             ['_csrf_token_']),
                                        ['user_title',
                                         'roles',
                                         'first_name',
                                         'last_name',
                                         'email',
                                         'organization']))
        roles = datas.pop('roles')
        password = appstruct['password']
        person = Person(password=password, **datas)
        root = getSite(context)
        principals = find_service(root, 'principals')
        users = principals['users']
        name = person.first_name + ' ' + person.last_name
        name = name_chooser(users, name=name)
        users[name] = person
        if getattr(context, 'ismanager', False) and \
           context.organization:
            grant_roles(person, (('OrganizationResponsible',
                                   context.organization),))

        person.state.append('active')
        grant_roles(person, roles)
        grant_roles(person, (('Owner', person),))
        initialize_tokens(person, root.tokens_mini)
        manager = context.manager
        root.delfromproperty('invitations', context)
        root.addtoproperty('news_letter_members', person)
        context.person = person
        if manager:
            mail_template = root.get_mail_template('accept_invitation')
            localizer = request.localizer
            recipient_title = localizer.translate(
                _(getattr(manager, 'user_title', '')))
            recipient_last_name = getattr(manager, 'last_name', '')
            user_title = localizer.translate(
                _(getattr(person, 'user_title', '')))
            user_first_name = getattr(person, 'first_name', '')
            user_last_name = getattr(person, 'last_name', '')
            novaideo_title = request.root.title
            url = request.resource_url(person, "@@index")
            roles_translate = [localizer.translate(APPLICATION_ROLES.get(r, r))
                               for r in roles]
            subject = mail_template['subject'].format(
                user_title=user_title,
                user_first_name=user_first_name,
                user_last_name=user_last_name,
                novaideo_title=novaideo_title
            )
            message = mail_template['template'].format(
                user_title=user_title,
                user_first_name=user_first_name,
                user_last_name=user_last_name,
                recipient_title=recipient_title,
                recipient_last_name=recipient_last_name,
                user_url=url,
                roles=", ".join(roles_translate),
                novaideo_title=novaideo_title)
            alert('email', [root.get_site_sender()], [manager.email],
                  subject=subject, body=message)

        return {}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def refuse_roles_validation(process, context):
    return has_role(role=('Anonymous',)) and \
           not has_role(role=('Admin',))


def refuse_state_validation(process, context):
    return 'pending' in context.state


class RefuseInvitation(InfiniteCardinality):
    style_picto = 'glyphicon glyphicon-thumbs-down'
    context = IInvitation
    roles_validation = refuse_roles_validation
    state_validation = refuse_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('pending')
        context.state.append('refused')
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        manager = context.manager
        if manager:
            root = getSite()
            mail_template = root.get_mail_template('refuse_invitation')
            localizer = request.localizer
            recipient_title = localizer.translate(
                _(getattr(manager, 'user_title', '')))
            recipient_last_name = getattr(manager, 'last_name', '')
            user_title = localizer.translate(
                           _(getattr(context, 'user_title', '')))
            user_first_name = getattr(context, 'first_name', '')
            user_last_name = getattr(context, 'last_name', '')
            novaideo_title = request.root.title
            url = request.resource_url(context, "@@index")
            roles_translate = [localizer.translate(APPLICATION_ROLES.get(r, r))
                               for r in context.roles]
            subject = mail_template['subject'].format(
                user_title=user_title,
                user_first_name=user_first_name,
                user_last_name=user_last_name,
                novaideo_title=novaideo_title
            )
            message = mail_template['template'].format(
                user_title=user_title,
                user_first_name=user_first_name,
                user_last_name=user_last_name,
                recipient_title=recipient_title,
                recipient_last_name=recipient_last_name,
                invitation_url=url,
                roles=", ".join(roles_translate),
                novaideo_title=novaideo_title)
            alert('email', [root.get_site_sender()], [context.manager.email],
                  subject=subject, body=message)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def remove_roles_validation(process, context):
    return (context.organization and \
            has_role(role=('OrganizationResponsible',
                           context.organization))) or \
            has_role(role=('Moderator',))


def remove_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class RemoveInvitation(InfiniteCardinality):
    style_picto = 'glyphicon glyphicon-trash'
    context = IInvitation
    roles_validation = remove_roles_validation
    processsecurity_validation = remove_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        root.delfromproperty('invitations', context)
        return {}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root, ''))


def reinvite_roles_validation(process, context):
    return (context.organization and \
            has_role(role=('OrganizationResponsible',
                           context.organization))) or \
            has_role(role=('Moderator',))


def reinvite_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def reinvite_state_validation(process, context):
    return 'refused' in context.state


class ReinviteUser(InfiniteCardinality):
    style_picto = 'glyphicon glyphicon-bullhorn'
    context = IInvitation
    roles_validation = reinvite_roles_validation
    processsecurity_validation = reinvite_processsecurity_validation
    state_validation = reinvite_state_validation

    def start(self, context, request, appstruct, **kw):
        url = request.resource_url(context, "")
        root = getSite()
        mail_template = root.get_mail_template('invitation')
        localizer = request.localizer
        roles_translate = [localizer.translate(APPLICATION_ROLES.get(r, r))
                           for r in getattr(context, 'roles', [])]
        subject = mail_template['subject'].format(
            novaideo_title=root.title
        )
        message = mail_template['template'].format(
            invitation=context,
            user_title=localizer.translate(getattr(context, 'user_title', '')),
            invitation_url=url,
            roles=", ".join(roles_translate),
            novaideo_title=root.title)
        alert('email', [root.get_site_sender()], [context.email],
              subject=subject, body=message)
        context.state.remove('refused')
        context.state.append('pending')
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def remind_roles_validation(process, context):
    return (context.organization and \
            has_role(role=('OrganizationResponsible',
                           context.organization))) or \
            has_role(role=('Moderator',))


def remind_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def remind_state_validation(process, context):
    return 'pending' in context.state


class RemindInvitation(InfiniteCardinality):
    style_picto = 'glyphicon glyphicon-bullhorn'
    isSequential = True
    context = IInvitation
    roles_validation = remind_roles_validation
    processsecurity_validation = remind_processsecurity_validation
    state_validation = remind_state_validation

    def start(self, context, request, appstruct, **kw):
        url = request.resource_url(context, "")
        root = getSite()
        mail_template = root.get_mail_template('invitation')
        localizer = request.localizer
        roles_translate = [localizer.translate(APPLICATION_ROLES.get(r, r))
                           for r in getattr(context, 'roles', [])]
        subject = mail_template['subject'].format(
            novaideo_title=root.title
        )
        message = mail_template['template'].format(
            invitation=context,
            user_title=localizer.translate(getattr(context, 'user_title', '')),
            invitation_url=url,
            roles=", ".join(roles_translate),
            novaideo_title=root.title)
        alert('email', [root.get_site_sender()], [context.email],
              subject=subject, body=message)
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors
