# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import Batch, get_oid

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from dace.util import find_catalog
from pontus.view import BasicView
from pontus.util import merge_dicts
from pontus.view_operation import MultipleView

from novaideo.utilities.util import render_listing_objs
from novaideo.content.processes.proposal_management.behaviors import (
    SeeAmendments)
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.views.filter import (
    get_filter, FILTER_SOURCES,
    find_entities)
from novaideo.views.filter.util import merge_with_filter_view
from novaideo.views.filter.sort import (
    sort_view_objects)
from novaideo.content.interface import IAmendment
from novaideo.views.core import asyn_component_config


AMENDMENTS_MESSAGES = {
    '0': _(u"""No amended version"""),
    '1': _(u"""One amended version"""),
    '*': _(u"""${number} amended versions""")}


class Header(BasicView):
    title = ''
    name = 'amendmentsheader'
    template = 'novaideo:views/proposal_management/templates/amendments_header.pt'
    
    def update(self):
        result = {}
        len_result = self.get_binding('len_result')
        len_my = self.get_binding('len_my')
        len_others = self.get_binding('len_others')
        values = {
            'current_user': self.get_binding('user'),
            'proposal': self.context,
            'len_result': len_result,
            'len_my': len_my,
            'len_others': len_others
            }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class ContentView(BasicView):
    template = 'novaideo:views/novaideo_view_manager/templates/home.pt'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    isactive = False
    hasparent = True
    filter_class = ''
    view_filter = [('metadata_filter', ['states', 'keywords']), 'geographic_filter',
                  'contribution_filter',
                  ('temporal_filter', ['negation', 'created_date']),
                  'text_filter', 'other_filter']

    def _add_filter(self, user, query):
        def source(**args):
            objects = find_entities(
                interfaces=[IAmendment],
                add_query=query,
                user=user, **args)
            return objects

        url = self.request.resource_url(
            self.context, '@@novaideoapi',
            query={'view_content_id': self.content_id})
        return get_filter(
            self,
            url=url,
            source=source,
            select=self.view_filter,
            filter_source="seeproposalamendments",
            filterid=self.viewid)

    def update(self):
        body = ''
        result = {}
        if self.isactive or self.params('on_demand') == 'load':
            user = get_current()
            query = self._get_query(user)
            filter_form, filter_data = self._add_filter(user, query)
            args = {}
            args = merge_with_filter_view(self, args)
            args['request'] = self.request
            objects = find_entities(
                interfaces=[IAmendment],
                user=user,
                add_query=query,
                **args)
            objects, sort_body = sort_view_objects(
                self, objects, ['amendment'], user)
            url = self.request.resource_url(
                self.context, 'seeproposalamendments',
                query={'view_content_id': self.content_id})
            batch = Batch(objects,
                          self.request,
                          url=url,
                          default_size=BATCH_DEFAULT_SIZE)
            self.len_objects = len(objects)
            self.title = _(self.title, mapping={'nb': batch.seqlen})
            batch.target = "#results-" + self.content_id
            filter_instance = getattr(self, 'filter_instance', None)
            filter_body = None
            if filter_instance:
                filter_data['filter_message'] = self.title
                filter_body = filter_instance.get_body(filter_data)
            result_body, result = render_listing_objs(
                self.request, batch, user,
                display_state=getattr(self, 'display_state', True))
            values = {'bodies': result_body,
                      'batch': batch,
                      'empty_message': self.empty_message,
                      'empty_icon': self.empty_icon,
                      'filter_body': filter_body,
                      'filter_class': self.filter_class,
                      'sort_body': sort_body,
                      'view': self}
            if filter_form:
                result = merge_dicts(
                    {'css_links': filter_form['css_links'],
                     'js_links': filter_form['js_links']
                    }, result)

            body = self.content(args=values, template=self.template)['body']

        item = self.adapt_item(body, self.viewid)
        item['isactive'] = self.isactive
        result['coordinates'] = {self.coordinates: [item]}
        return result


class MyAmendmentView(ContentView):
    title = _('My amendments')
    content_id = 'proposal-myamendments'
    viewid = 'proposal-myamendments'
    view_icon = 'icon novaideo-icon icon-amendment'
    counter_id = 'proposal-myamendment-counter'
    empty_message = _("No amended version")
    empty_icon = 'icon novaideo-icon icon-amendment'
    isactive = True
    view_filter = [('metadata_filter', ['states', 'keywords']), 'geographic_filter',
                  ('temporal_filter', ['negation', 'created_date']),
                  'text_filter', 'other_filter']

    def _get_query(self, user):
        dace_catalog = find_catalog('dace')
        novaideo_catalog = find_catalog('novaideo')
        object_authors_index = novaideo_catalog['object_authors']
        container_index = dace_catalog['container_oid']
        return container_index.eq(get_oid(self.context)) & \
            object_authors_index.any([get_oid(user)])


@asyn_component_config(
    id='proposal-amendments',
    on_demand=True,
    delegate='proposal_amendments')
class AmendmentsView(ContentView):
    title = _('Other amendments')
    content_id = 'proposal-amendments'
    viewid = 'proposal-amendments'
    view_icon = 'icon novaideo-icon icon-amendment'
    counter_id = 'proposal-amendment-counter'
    empty_message = _("No amended version")
    empty_icon = 'icon novaideo-icon icon-amendment'

    def _get_query(self, user):
        dace_catalog = find_catalog('dace')
        novaideo_catalog = find_catalog('novaideo')
        object_authors_index = novaideo_catalog['object_authors']
        container_index = dace_catalog['container_oid']
        return container_index.eq(get_oid(self.context)) & \
            object_authors_index.notany([get_oid(user)])


@asyn_component_config(id='proposal_amendments')
class SeeAmendmentsView(MultipleView):
    title = _('Amended versions')
    name = 'seepamendments'
    viewid = 'seepamendments'
    template = 'novaideo:views/templates/multipleview.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    css_class = 'contents-bloc'
    behaviors = [SeeAmendments]
    center_tabs = True
    views = (MyAmendmentView, AmendmentsView)

    def _init_views(self, views, **kwargs):
        if self.params('load_view'):
            delegated_by = kwargs.get('delegated_by', None)
            views = tuple(self.views)
            view_id = self.params('view_content_id')
            if view_id == 'proposal-myamendments':
                views = (MyAmendmentView, )

            if 'proposal-amendments' in (delegated_by, view_id):
                views = (AmendmentsView, )

        super(SeeAmendmentsView, self)._init_views(views, **kwargs)


@view_config(
    name='seeproposalamendments',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AllAmendmentsView(MultipleView):
    title = _('Amended versions')
    name = 'seeproposalamendments'
    viewid = 'seeproposalamendments'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    view_icon = 'novaideo-icon icon-amendment'
    contextual_help = 'amendments-help'
    description = _("See amended versions")
    css_class = 'panel-transparent contents-bloc'
    views = (Header, SeeAmendmentsView)
    validators = [SeeAmendments.get_validator()]

    def update(self):
        len_result = self.get_binding('len_result')
        if len_result:
            index = str(len_result)
            if len_result > 1:
                index = '*'

            self.title = _(AMENDMENTS_MESSAGES[index],
                           mapping={'number': len_result})

        return super(AllAmendmentsView, self).update()

    def bind(self):
        bindings = {}
        user = get_current(self.request)
        dace_catalog = find_catalog('dace')
        novaideo_catalog = find_catalog('novaideo')
        object_authors_index = novaideo_catalog['object_authors']
        container_index = dace_catalog['container_oid']
        query = container_index.eq(get_oid(self.context))
        objects = find_entities(
            interfaces=[IAmendment],
            user=user,
            add_query=query)
        query = query & object_authors_index.any([get_oid(user)])
        my_objs = find_entities(
            interfaces=[IAmendment],
            user=user,
            add_query=query)
        len_result = len(objects)
        len_my = len(my_objs)
        len_others = len_result - len_my
        bindings['user'] = user
        bindings['len_result'] = len_result
        bindings['len_my'] = len_my
        bindings['len_others'] = len_others
        setattr(self, '_bindings', bindings)


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeAmendments: AllAmendmentsView})


FILTER_SOURCES.update(
    {"seeproposalamendments": SeeAmendmentsView})
