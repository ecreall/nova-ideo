# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    has_role)
from dace.processinstance.activity import (
    InfiniteCardinality)

from novaideo.content.interface import INovaIdeoApplication
from novaideo import _


def update_roles_validation(process, context):
    return has_role(role=('Admin',))


class Update(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-repeat'
    style_order = 10
    submission_title = _('Update')
    context = INovaIdeoApplication
    roles_validation = update_roles_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        runtime = root['runtime']
        processes = list(runtime.processes)
        if self.process in processes:
            processes.remove(self.process)

        [runtime.delfromproperty('processes', p) for p in processes
         if getattr(p.definition, 'isUnique', False)]
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, ""))


#TODO behaviors
