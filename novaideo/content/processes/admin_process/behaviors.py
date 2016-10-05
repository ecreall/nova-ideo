# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from io import StringIO, BytesIO
import csv
import pytz
import datetime
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound
from pyramid.response import FileIter

from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    has_any_roles,
    get_current)
from dace.processinstance.activity import (
    InfiniteCardinality)

from novaideo.adapters import (
    IExtractionAdapter, EXTRACTION_ATTR)
from novaideo.utilities.util import to_localized_time
from novaideo.content.interface import (
    INovaIdeoApplication,
    ISearchableEntity)
from novaideo import _
from novaideo.views.filter import find_entities


def siteadmin_roles_validation(process, context):
    return has_any_roles(roles=('SiteAdmin', ))


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


class Extract(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-export'
    style_order = 8
    submission_title = _('Continue')
    context = INovaIdeoApplication
    processsecurity_validation = siteadmin_roles_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        localizer = request.localizer
        appstruct.pop('_csrf_token_')
        attributes_to_extract = appstruct.pop('attributes_to_extract')
        if not attributes_to_extract:
            attributes_to_extract = list(EXTRACTION_ATTR.keys())

        attributes_to_extract = sorted(
            attributes_to_extract, key=lambda a: EXTRACTION_ATTR[a]['order'])
        objects = find_entities(
            user=user,
            sort_on='release_date',
            **appstruct
        )
        csv_file = StringIO()
        fieldnames = []
        for attr in attributes_to_extract:
            fieldnames.append(
                localizer.translate(EXTRACTION_ATTR[attr]['title']))

        writer = csv.DictWriter(
            csv_file, fieldnames=fieldnames, dialect='excel', delimiter=';')
        writer.writeheader()
        registry = request.registry
        for obj in objects:
            adapter = registry.queryAdapter(
                obj, IExtractionAdapter)
            if adapter:
                writer.writerow(
                    dict([(localizer.translate(EXTRACTION_ATTR[attr]['title']),
                           localizer.translate(getattr(adapter, attr)(
                               user, request))) for
                          attr in attributes_to_extract]))

        csv_file.seek(0)
        return {'file': BytesIO(csv_file.read().encode('windows-1252', 'replace')),
                'filter': appstruct, 'user': user}

    def redirect(self, context, request, **kw):
        filter_ = kw.get('filter', None)
        keywords = []
        if filter_:
            keywords = list(filter_.get(
                'metadata_filter', {}).get(
                'keywords', []))

        keywords = '-'.join(keywords)
        user = kw.get('user', None)
        user_title = getattr(user, 'title', user.name)
        now = datetime.datetime.now()
        date = to_localized_time(now, request=request, translate=True)
        file_name = 'Extraction_{keywords}_{date}_{user}'.format(
            keywords=keywords, date=date, user=user_title)
        file_name = file_name.replace(' ', '-')
        csv_file = kw.get('file', '')
        response = request.response
        response.content_type = 'application/vnd.ms-excel;charset=windows-1252'
        response.content_disposition = 'inline; filename="{file_name}.csv"'.format(
            file_name=file_name)
        response.app_iter = FileIter(csv_file)
        return response

#TODO behaviors
