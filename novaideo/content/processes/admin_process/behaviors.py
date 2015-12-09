# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import pytz
import datetime
from pyramid.httpexceptions import HTTPFound

from dace.objectofcollaboration.principal.util import (
    has_any_roles)
from dace.processinstance.activity import (
    InfiniteCardinality)

from novaideo.content.interface import (
    INovaIdeoApplication)
from novaideo import _


def siteadmin_roles_validation(process, context):
    return has_any_roles(roles=('Admin', ))


class ConfigureSite(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-wrench'
    style_order = 0
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = siteadmin_roles_validation

    def start(self, context, request, appstruct, **kw):
        site = appstruct['_object_data']
        # work_conf = appstruct.pop('work_conf')
        # site.set_data(work_conf)
        site.modified_at = datetime.datetime.now(tz=pytz.UTC)
        # deadline = work_conf.pop('deadline', None)
        # if deadline:
        #     deadline = deadline.replace(tzinfo=pytz.UTC)
        #     if site.deadlines:
        #         current = site.deadlines[-1]
        #         site.deadlines.remove(current)

        #     site.deadlines.append(deadline)

        site.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, ""))

#TODO behaviors
