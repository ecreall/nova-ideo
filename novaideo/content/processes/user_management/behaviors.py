from pyramid.httpexceptions import HTTPFound
from substanced.util import find_service

from dace.util import getSite
from dace.processinstance.activity import (
    ElementaryAction,
    LimitedCardinality,
    InfiniteCardinality,
    ActionType,
    StartStep,
    EndStep)
from sdkuneagi.ips.xlreader import creat_object_from_xl
from sdkuneagi.content.interface import INovaIdeoApplication
from sdkuneagi.content.person import Person


def adduser_relation_validation(process, context):
    return True


def adduser_roles_validation(process, context):
    return True#has_any_roles(roles=('Moderator',))


def adduser_processsecurity_validation(process, context):
    return True


def adduser_state_validation(process, context):
    return True


class AddUsers(InfiniteCardinality):
    isSequential = True
    context = INovaIdeoApplication
    relation_validation = adduser_relation_validation
    roles_validation = adduser_roles_validation
    processsecurity_validation = adduser_processsecurity_validation
    state_validation = adduser_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        xlfile = appstruct['file']['_object_data']
        new_users = creat_object_from_xl(file=xlfile, factory=Person, properties={'title':('String', False),
                                                                                  'description':('String', False),
                                                                                  'email':('String', False)})
        principals = find_service(root, 'principals')
        users = principals['users']
        for user in new_users:
            users[user.title] = user
    
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
        for invitation_dict in invitations:
            invitation = invitation_dict['_object_data']
            root.addtoproperty('invitations', invitation)
            #send mail
    
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#TODO bihaviors
