# -*- coding: utf8 -*-
# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.httpexceptions import HTTPFound

from dace.processinstance.activity import InfiniteCardinality
from dace.objectofcollaboration.principal.util import (
    has_role)

from novaideo import _
from novaideo.content.interface import INovaIdeoApplication
from novaideo.content.processes import global_user_processsecurity


def see_roles_validation(process, context):
    return has_role(role=('SiteAdmin',))


def see_processsecurity_validation(process, context):
    return global_user_processsecurity()


class SeeConnectors(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'admin-action'
    style_picto = 'icon fa fa-plug'
    style_order = 7
    title = _('Registered connectors')
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = see_roles_validation
    processsecurity_validation = see_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(request.root, ""))


def add_roles_validation(process, context):
    return has_role(role=('SiteAdmin',))


def add_processsecurity_validation(process, context):
    return global_user_processsecurity()


class AddConnectors(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'admin-action'
    style_picto = 'icon fa fa-plug'
    style_order = 6
    title = _('Connectors')
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = add_roles_validation
    processsecurity_validation = add_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(request.root, ""))
