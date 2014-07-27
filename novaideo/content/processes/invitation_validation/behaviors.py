from pyramid.httpexceptions import HTTPFound
from substanced.util import find_service

from dace.util import getSite
from dace.objectofcollaboration.principal.util import grant_roles
from dace.processinstance.activity import (
    ElementaryAction,
    LimitedCardinality,
    InfiniteCardinality,
    ActionType,
    StartStep,
    EndStep)
from pontus.schema import select, omit

from novaideo.ips.xlreader import creat_object_from_xl
from novaideo.content.interface import IInvitation
from novaideo.content.person import Person
from novaideo.content.invitation import InvitationSchema


def accept_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'invitation')


def accept_roles_validation(process, context):
    return True#has_any_roles(roles=('Moderator',))


def accept_processsecurity_validation(process, context):
    return True


def accept_state_validation(process, context):
    return 'pending' in context.state


class AcceptInvitation(ElementaryAction):
    context = IInvitation
    relation_validation = accept_relation_validation
    roles_validation = accept_roles_validation
    processsecurity_validation = accept_processsecurity_validation
    state_validation = accept_state_validation

    def start(self, context, request, appstruct, **kw):
        datas = context.get_data(select(omit(InvitationSchema(), ['_csrf_token_']),['user_title',
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
        name = person.first_name + ' ' +person.last_name
        principals['users'][name] = person
        grant_roles(person, roles)
        context.state.remove('pending')
        context.state.append('accepted')
        root.delproperty('invitations', context) 
        return True

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root, "@@index"))


def refuse_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'invitation')


def refuse_roles_validation(process, context):
    return True#has_any_roles(roles=('Moderator',))


def refuse_processsecurity_validation(process, context):
    return True


def refuse_state_validation(process, context):
    return 'pending' in context.state


class RefuseInvitation(ElementaryAction):
    context = IInvitation
    relation_validation = refuse_relation_validation
    roles_validation = refuse_roles_validation
    processsecurity_validation = refuse_processsecurity_validation
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
    return True#has_any_roles(roles=('Moderator',))


def remove_processsecurity_validation(process, context):
    return True


def remove_state_validation(process, context):
    return True


class RemoveInvitation(ElementaryAction):
    context = IInvitation
    relation_validation = remove_relation_validation
    roles_validation = remove_roles_validation
    processsecurity_validation = remove_processsecurity_validation
    state_validation = remove_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        root.delproperty('invitations', context) 
        return True

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root, "@@index"))


def reinvite_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'invitation')


def reinvite_roles_validation(process, context):
    return True#has_any_roles(roles=('Moderator',))


def reinvite_processsecurity_validation(process, context):
    return True


def reinvite_state_validation(process, context):
    return 'refused' in context.state


class ReinviteUser(ElementaryAction):
    context = IInvitation
    relation_validation = reinvite_relation_validation
    roles_validation = reinvite_roles_validation
    processsecurity_validation = reinvite_processsecurity_validation
    state_validation = reinvite_state_validation

    def start(self, context, request, appstruct, **kw):
        #send mail
        context.state.remove('refused')
        context.state.append('pending')
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def remind_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'invitation')


def remind_roles_validation(process, context):
    return True#has_any_roles(roles=('Moderator',))


def remind_processsecurity_validation(process, context):
    return True


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
        #send mail to person    
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))



#TODO bihaviors
