# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import pytz
import datetime
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    has_any_roles)
from dace.processinstance.activity import (
    InfiniteCardinality)

from novaideo.content.interface import (
    INovaIdeoApplication,
    ISearchableEntity)
from novaideo import _
from novaideo.views.filter import find_entities


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


class ManageKeywords(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-tags'
    style_order = 8
    submission_title = _('Save')
    context = INovaIdeoApplication
    processsecurity_validation = siteadmin_roles_validation

    def start(self, context, request, appstruct, **kw):
        source = appstruct['source']
        targets = appstruct['targets']
        root = getSite()
        root.keywords = PersistentList(list(root.keywords))
        for target in [t for t in targets if t in root.keywords]:
            root.keywords.remove(target)

        root.keywords.append(source)
        root.reindex()

        objects = find_entities(
            interfaces=[ISearchableEntity],
            metadata_filter={'keywords': [kw.lower() for kw in targets]})

        for obj in objects:
            obj.keywords = PersistentList(list(obj.keywords))
            for target in [t for t in targets if t in obj.keywords]:
                obj.keywords.remove(target)

            obj.keywords.append(source)
            obj.reindex()

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, ""))

#TODO behaviors
