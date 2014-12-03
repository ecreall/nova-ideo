# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.httpexceptions import HTTPFound
from substanced.util import find_service, get_oid

from dace.util import getSite
from dace.objectofcollaboration.principal.util import grant_roles, has_role
from dace.processinstance.activity import (
    ElementaryAction,
    InfiniteCardinality)
from pontus.schema import select, omit

from novaideo.ips.mailer import mailer_send
from novaideo.content.interface import IInvitation
from novaideo.content.person import Person
from novaideo.content.invitation import InvitationSchema
from ..user_management.behaviors import global_user_processsecurity
from novaideo.mail import INVITATION_MESSAGE



def accept_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'invitation')


def accept_roles_validation(process, context):
    return has_role(role=('Anonymous',)) and not has_role(role=('Admin',))


def accept_state_validation(process, context):
    return 'pending' in context.state


class AcceptInvitation(ElementaryAction):
    context = IInvitation
    relation_validation = accept_relation_validation
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
        person = Person(password=password)
        person.set_data(datas)
        root = getSite(context)
        principals = find_service(root, 'principals')
        name = person.first_name + ' ' + person.last_name
        principals['users'][name] = person
        grant_roles(person, roles)
        grant_roles(person, (('Owner', person),))
        context.state.remove('pending')
        context.state.append('accepted')
        root.delfromproperty('invitations', context)
        return True

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def refuse_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'invitation')


def refuse_roles_validation(process, context):
    return has_role(role=('Anonymous',)) and not has_role(role=('Admin',))


def refuse_state_validation(process, context):
    return 'pending' in context.state


class RefuseInvitation(ElementaryAction):
    context = IInvitation
    relation_validation = refuse_relation_validation
    roles_validation = refuse_roles_validation
    state_validation = refuse_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('pending')
        context.state.append('refused')
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def remove_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'invitation')


def remove_roles_validation(process, context):
    return has_role(role=('Moderator',))


def remove_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class RemoveInvitation(ElementaryAction):
    context = IInvitation
    relation_validation = remove_relation_validation
    roles_validation = remove_roles_validation
    processsecurity_validation = remove_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        root.delfromproperty('invitations', context)
        return True

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def reinvite_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'invitation')


def reinvite_roles_validation(process, context):
    return has_role(role=('Moderator',))


def reinvite_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def reinvite_state_validation(process, context):
    return 'refused' in context.state


class ReinviteUser(ElementaryAction):
    context = IInvitation
    relation_validation = reinvite_relation_validation
    roles_validation = reinvite_roles_validation
    processsecurity_validation = reinvite_processsecurity_validation
    state_validation = reinvite_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        url = request.resource_url(root, "@@seeinvitation", 
                          query={'invitation_id':str(get_oid(context))})
        message = INVITATION_MESSAGE.format(
            invitation=context,
            user_title=getattr(context, 'user_title', ''),
            invitation_url=url,
            roles=", ".join(getattr(context, 'roles', [])))
        mailer_send(subject='Invitation', 
                    recipients=[context.email], 
                    body=message )
        context.state.remove('refused')
        context.state.append('pending')
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def remind_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'invitation')


def remind_roles_validation(process, context):
    return has_role(role=('Moderator',))


def remind_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def remind_state_validation(process, context):
    return 'pending' in context.state


class RemindInvitation(InfiniteCardinality):
    isSequential = True
    context = IInvitation
    relation_validation = remind_relation_validation
    roles_validation = remind_roles_validation
    processsecurity_validation = remind_processsecurity_validation
    state_validation = remind_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        url = request.resource_url(root, "@@seeinvitation", 
                                query={'invitation_id':str(get_oid(context))})
        message = INVITATION_MESSAGE.format(
            invitation=context,
            user_title=getattr(context, 'user_title', ''),
            invitation_url=url,
            roles=", ".join(getattr(context, 'roles', [])))
        mailer_send(subject='Invitation', 
            recipients=[context.email], 
            body=message )
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#TODO behaviors
