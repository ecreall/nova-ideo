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
from pontus.view import BasicView
from pontus.schema import select, omit

from novaideo.content.interface import INovaIdeoApplication
from novaideo import _


def login_relation_validation(process, context):
    return True


def login_roles_validation(process, context):
    return has_any_roles(roles=('Anonymous', ), ignore_superiors=True)


def login_processsecurity_validation(process, context):
    return True


def login_state_validation(process, context):
    return True


class AnonymousLogIn(InfiniteCardinality):
    title = _('Log in access')
    context = Interface
    actionType = ActionType.automatic
    relation_validation = login_relation_validation
    roles_validation = login_roles_validation
    processsecurity_validation = login_processsecurity_validation
    state_validation = login_state_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root, "@@index"))


#TODO bihaviors
