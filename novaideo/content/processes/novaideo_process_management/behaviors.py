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
    return has_role(role=('SiteAdmin',))


class Update(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-repeat'
    style_interaction = 'ajax-action'
    style_order = 10
    submission_title = _('Update')
    context = INovaIdeoApplication
    roles_validation = update_roles_validation

    def start(self, context, request, appstruct, **kw):
        processes_names = appstruct['processes']
        root = getSite()
        runtime = root['runtime']
        processes = [p for p in list(runtime.processes)
                     if p.__name__ in processes_names]
        if self.process in processes:
            processes.remove(self.process)

        for proc in processes:
            proc_def = proc.definition
            if getattr(proc_def, 'isUnique', False):
                runtime.delfromproperty('processes', proc)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, ""))


#TODO behaviors
