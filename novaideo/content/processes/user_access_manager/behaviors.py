# -*- coding: utf8 -*-
from zope.interface import Interface

from pyramid.httpexceptions import HTTPFound
from substanced.util import find_service, get_oid

from dace.util import getSite
from dace.objectofcollaboration.principal.util import grant_roles, has_any_roles, has_role
from dace.processinstance.activity import (
    ElementaryAction,
    LimitedCardinality,
    InfiniteCardinality,
    ActionType,
    StartStep,
    EndStep)
from pontus.schema import select, omit

from novaideo.content.interface import IInvitation
from novaideo.content.person import Person
from novaideo.content.interface import INovaIdeoApplication
from novaideo import _


def login_roles_validation(process, context):
    return has_any_roles(roles=('Anonymous', 'Collaborator'))


class LogIn(InfiniteCardinality):
    title = _('Log in')
    access_controled = True
    context = INovaIdeoApplication
    roles_validation = login_roles_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def logout_roles_validation(process, context):
    return has_role(role=('Collaborator',))


class LogOut(InfiniteCardinality):
    title = _('Log out')
    access_controled = True
    context = INovaIdeoApplication
    roles_validation = logout_roles_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))

#TODO behaviors
