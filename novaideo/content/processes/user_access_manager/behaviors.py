# -*- coding: utf8 -*-
from zope.interface import Interface

from pyramid.httpexceptions import HTTPFound
from substanced.util import find_service, get_oid

from dace.util import getSite
from dace.objectofcollaboration.principal.util import grant_roles, has_any_roles
from dace.processinstance.activity import (
    ElementaryAction,
    LimitedCardinality,
    InfiniteCardinality,
    ActionType,
    StartStep,
    EndStep)
from pontus.schema import select, omit

from novaideo.ips.xlreader import creat_object_from_xl
from novaideo.ips.mailer import mailer_send
from novaideo.content.interface import IInvitation
from novaideo.content.person import Person
from novaideo.content.interface import INovaIdeoApplication
from novaideo import _


def login_relation_validation(process, context):
    return True


def login_roles_validation(process, context):
    return has_any_roles(roles=('Anonymous', 'Collaborator'))


def login_processsecurity_validation(process, context):
    return True


def login_state_validation(process, context):
    return True


class LogIn(InfiniteCardinality):
    title = _('Log in')
    access_controled = True
    context = INovaIdeoApplication
    relation_validation = login_relation_validation
    roles_validation = login_roles_validation
    processsecurity_validation = login_processsecurity_validation
    state_validation = login_state_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def logout_relation_validation(process, context):
    return True


def logout_roles_validation(process, context):
    return has_any_roles(roles=('Collaborator',))


def logout_processsecurity_validation(process, context):
    return True


def logout_state_validation(process, context):
    return True


class LogOut(InfiniteCardinality):
    title = _('Log out')
    access_controled = True
    context = INovaIdeoApplication
    relation_validation = logout_relation_validation
    roles_validation = logout_roles_validation
    processsecurity_validation = logout_processsecurity_validation
    state_validation = logout_state_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))

#TODO bihaviors
