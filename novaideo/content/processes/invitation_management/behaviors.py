# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
from pyramid.httpexceptions import HTTPFound

from substanced.util import get_oid
from dace.util import find_service, getSite
from dace.objectofcollaboration.principal.util import has_role
from dace.processinstance.activity import (
    InfiniteCardinality,
    ActionType)
from novaideo.ips.xlreader import create_object_from_xl
from novaideo.content.interface import INovaIdeoApplication, IInvitation
from novaideo.content.invitation import Invitation
from novaideo.ips.mailer import mailer_send
from novaideo.mail import INVITATION_MESSAGE
from novaideo import _
from ..user_management.behaviors import global_user_processsecurity
from novaideo.core import acces_action

def uploaduser_relation_validation(process, context):
    return True


def uploaduser_roles_validation(process, context):
    return has_role(role=('Moderator',))


def uploaduser_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def uploaduser_state_validation(process, context):
    return True


class UploadUsers(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    relation_validation = uploaduser_relation_validation
    roles_validation = uploaduser_roles_validation
    processsecurity_validation = uploaduser_processsecurity_validation
    state_validation = uploaduser_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        xlfile = appstruct['file']['_object_data']
        new_invitations = create_object_from_xl(file=xlfile, factory=Invitation, properties={'first_name':('String', False),
                                                                                  'last_name':('String', False),
                                                                                  'user_title':('String', False),
                                                                                  'email':('String', False)})
        def_container = find_service('process_definition_container')
        pd = def_container.get_definition('invitationvalidation')
        runtime = find_service('runtime')
        for invitation in new_invitations:
            invitation.title = u"""{title} {user_title} {first_name} {last_name}""".format(title=invitation.title,
                                                                                           user_title=getattr(self.context, 'user_title',''),
                                                                                           first_name=getattr(self.context, 'first_name',''),
                                                                                           last_name=getattr(self.context, 'last_name',''))
            invitation.state.append('pending')
            root.addtoproperty('invitations', invitation)
            proc = pd()
            proc.__name__ = proc.id
            runtime.addtoproperty('processes', proc)
            proc.defineGraph(pd)
            proc.execute()
            proc.execution_context.add_involved_entity('invitation', invitation)
            url = request.resource_url(root, "@@seeinvitation",query={'invitation_id':str(get_oid(invitation))})
            message = INVITATION_MESSAGE.format(
                invitation=invitation,
                user_title=getattr(invitation, 'user_title', ''),
                invitation_url=url,
                roles=", ".join(getattr(invitation, 'roles', [])))
            mailer_send(subject='Invitation', recipients=[invitation.email], body=message )

        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))



def inviteuser_relation_validation(process, context):
    return True


def inviteuser_roles_validation(process, context):
    return has_role(role=('Moderator',))


def inviteuser_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def inviteuser_state_validation(process, context):
    return True


class InviteUsers(InfiniteCardinality):
    isSequential = False
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
            url = request.resource_url(root, "@@seeinvitation",query={'invitation_id':str(get_oid(invitation))})
            message = INVITATION_MESSAGE.format(
                invitation=invitation,
                user_title=getattr(invitation, 'user_title', ''),
                invitation_url=url,
                roles=", ".join(getattr(invitation, 'roles', [])))
            mailer_send(subject='Invitation', recipients=[invitation.email], body=message )

        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))




def seeinv_processsecurity_validation(process, context):
    return has_role(role=('Anonymous',)) and not has_role(role=('Administrator',))

@acces_action()
class SeeInvitation(InfiniteCardinality):
    isSequential = False
    title = _('Details')
    actionType = ActionType.automatic
    context = INovaIdeoApplication
    processsecurity_validation = seeinv_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def seeinvs_relation_validation(process, context):
    return True


def seeinvs_roles_validation(process, context):
    return has_role(role=('Moderator',))


def seeinvs_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and context.invitations


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
        return HTTPFound(request.resource_url(context))


def edit_relation_validation(process, context):
    return True


def edit_roles_validation(process, context):
    return has_role(role=('Moderator',))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and context.invitations


def edit_state_validation(process, context):
    return True


class EditInvitations(InfiniteCardinality):
    isSequential = True
    context = INovaIdeoApplication
    relation_validation = edit_relation_validation
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def editinv_relation_validation(process, context):
    return True


def editinv_roles_validation(process, context):
    return has_role(role=('Moderator',))


def editinv_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def editinv_state_validation(process, context):
    return True


class EditInvitation(InfiniteCardinality):
    isSequential = False
    title = _('Edit invitation')
    context = IInvitation
    relation_validation = editinv_relation_validation
    roles_validation = editinv_roles_validation
    processsecurity_validation = editinv_processsecurity_validation
    state_validation = editinv_state_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors
