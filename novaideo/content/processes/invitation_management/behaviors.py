from pyramid.httpexceptions import HTTPFound

from dace.util import find_service, getSite
from dace.processinstance.activity import (
    ElementaryAction,
    LimitedCardinality,
    InfiniteCardinality,
    ActionType,
    StartStep,
    EndStep)
from novaideo.ips.xlreader import creat_object_from_xl
from novaideo.content.interface import INovaIdeoApplication, IInvitation
from novaideo.content.person import Person
from novaideo.content.invitation import Invitation


def uploaduser_relation_validation(process, context):
    return True


def uploaduser_roles_validation(process, context):
    return True#has_any_roles(roles=('Moderator',))


def uploaduser_processsecurity_validation(process, context):
    return True


def uploaduser_state_validation(process, context):
    return True


class UploadUsers(InfiniteCardinality):
    isSequential = True
    context = INovaIdeoApplication
    relation_validation = uploaduser_relation_validation
    roles_validation = uploaduser_roles_validation
    processsecurity_validation = uploaduser_processsecurity_validation
    state_validation = uploaduser_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        xlfile = appstruct['file']['_object_data']
        new_invitations = creat_object_from_xl(file=xlfile, factory=Invitation, properties={'first_name':('String', False),
                                                                                  'last_name':('String', False),
                                                                                  'user_title':('String', False),
                                                                                  'email':('String', False)})
        def_container = find_service('process_definition_container')
        pd = def_container.get_definition('invitationvalidation')
        runtime = find_service('runtime')
        for invitation in new_invitations:
            invitation.state.append('pending')
            root.addtoproperty('invitations', invitation)
            proc = pd()
            proc.__name__ = proc.id
            runtime.addtoproperty('processes', proc)
            proc.defineGraph(pd)
            proc.execute()
            proc.execution_context.add_involved_entity('invitation', invitation)

    
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))



def inviteuser_relation_validation(process, context):
    return True


def inviteuser_roles_validation(process, context):
    return True#has_any_roles(roles=('Moderator',))


def inviteuser_processsecurity_validation(process, context):
    return True


def inviteuser_state_validation(process, context):
    return True


class InviteUsers(InfiniteCardinality):
    isSequential = True
    context = INovaIdeoApplication
    relation_validation = inviteuser_relation_validation
    roles_validation = inviteuser_roles_validation
    processsecurity_validation = inviteuser_processsecurity_validation
    state_validation = inviteuser_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        invitations = appstruct['invitations']
        def_container = find_service('process_definition_container')
        pd = def_container.get_definition('invitationvalidation')
        runtime = find_service('runtime')
        for invitation_dict in invitations:
            invitation = invitation_dict['_object_data']
            invitation.state.append('pending')
            root.addtoproperty('invitations', invitation)
            proc = pd()
            proc.__name__ = proc.id
            runtime.addtoproperty('processes', proc)
            proc.defineGraph(pd)
            proc.execute()
            proc.execution_context.add_involved_entity('invitation', invitation)
            #send mail
    
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))



def seeinv_relation_validation(process, context):
    return True


def seeinv_roles_validation(process, context):
    return True#has_any_roles(roles=('Moderator',))


def seeinv_processsecurity_validation(process, context):
    return len(context.__parent__.invitations)>=1


def seeinv_state_validation(process, context):
    return True


class SeeInvitation(InfiniteCardinality):
    isSequential = False
    title = 'Details'
    actionType = ActionType.automatic
    context = IInvitation
    relation_validation = seeinv_relation_validation
    roles_validation = seeinv_roles_validation
    processsecurity_validation = seeinv_processsecurity_validation
    state_validation = seeinv_state_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def seeinvs_relation_validation(process, context):
    return True


def seeinvs_roles_validation(process, context):
    return True#has_any_roles(roles=('Moderator',))


def seeinvs_processsecurity_validation(process, context):
    return len(context.invitations)>=1


def seeinvs_state_validation(process, context):
    return True


class SeeInvitations(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    relation_validation = seeinvs_relation_validation
    roles_validation = seeinvs_roles_validation
    processsecurity_validation = seeinvs_processsecurity_validation
    state_validation = seeinvs_state_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO bihaviors
