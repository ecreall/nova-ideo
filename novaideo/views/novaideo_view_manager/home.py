# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import Batch

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView
from pontus.util import merge_dicts
from pontus.view_operation import MultipleView

from novaideo.utilities.util import render_listing_objs
from novaideo.content.processes.novaideo_view_manager.behaviors import SeeHome
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.views.filter import (
    get_filter, FILTER_SOURCES,
    merge_with_filter_view, find_entities)
from novaideo.views.filter.sort import (
    sort_view_objects)
from novaideo.views.core import asyn_component_config
# from .search import get_default_searchable_content


CONTENTS_MESSAGES = {
    '0': _(u"""No element found"""),
    '1': _(u"""One element found"""),
    '*': _(u"""${nember} elements found""")
}


class ContentView(BasicView):
    template = 'novaideo:views/novaideo_view_manager/templates/home.pt'
    anonymous_template = 'novaideo:views/novaideo_view_manager/templates/anonymous_view.pt'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    content_type = 'idea'
    isactive = False

    def _add_filter(self, user):
        def source(**args):
            # default_content = [key[0] for key in
            #                    get_default_searchable_content(self.request)]
            # default_content.remove("person")
            default_content = [self.content_type]
            filter_ = {
                'metadata_filter': {
                    'content_types': default_content,
                    'states': ['active', 'published']}
            }
            objects = find_entities(user=user, filters=[filter_], **args)
            return objects

        url = self.request.resource_url(
            self.context, '@@novaideoapi',
            query={'view_content_type': self.content_type})
        select = [('metadata_filter', ['states', 'keywords', 'challenges']), 'geographic_filter',
                  'contribution_filter',
                  ('temporal_filter', ['negation', 'created_date']),
                  'text_filter', 'other_filter']
        return get_filter(
            self,
            url=url,
            source=source,
            select=select,
            filter_source="home",
            filterid=self.content_type)

    def update(self):
        if self.request.is_idea_box:
            self.title = ''

        user = get_current()
        filter_form, filter_data = self._add_filter(user)
        # default_content = [key[0] for key in
        #                    get_default_searchable_content(self.request)]
        # default_content.remove("person")
        default_content = [self.content_type]
        validated = {
            'metadata_filter':
                {'content_types': default_content,
                'states': ['active', 'published']}
        }
        args = {}
        args = merge_with_filter_view(self, args)
        args['request'] = self.request
        objects = find_entities(
            user=user,
            filters=[validated],
            **args)
        objects, sort_body = sort_view_objects(
            self, objects, [self.content_type], user)
        url = self.request.resource_url(
            self.context, '',
            query={'view_content_type': self.content_type})
        batch = Batch(objects,
                      self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        self.title = _(self.title, mapping={'nb': batch.seqlen})
        batch.target = "#results"+"-"+ self.content_type
        filter_instance = getattr(self, 'filter_instance', None)
        filter_body = None
        if filter_instance:
            filter_data['filter_message'] = self.title
            filter_body = filter_instance.get_body(filter_data)
        result_body, result = render_listing_objs(
            self.request, batch, user)
        values = {'bodies': result_body,
                  'batch': batch,
                  'empty_message': self.empty_message,
                  'empty_icon': self.empty_icon,
                  'filter_body': filter_body,
                  'sort_body': sort_body}
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


class IdeasView(ContentView):
    title = _('Ideas (${nb})')
    content_type = 'idea'
    viewid = 'home-ideas'
    view_icon = 'icon novaideo-icon icon-idea'
    counter_id = 'home-ideas-counter'
    empty_message = _("No registered ideas")
    empty_icon = 'icon novaideo-icon icon-idea'
    isactive = True


class ProposalsView(ContentView):
    title = _('The Working Groups (${nb})')
    content_type = 'proposal'
    viewid = 'home-proposals'
    view_icon = 'icon novaideo-icon icon-wg'
    counter_id = 'home-proposals-counter'
    empty_message = _("No working group created")
    empty_icon = 'icon novaideo-icon icon-wg'


class QuestionsView(ContentView):
    title = _('Questions (${nb})')
    content_type = 'question'
    viewid = 'home-questions'
    view_icon = 'md md-live-help'
    counter_id = 'home-questions-counter'
    empty_message = _("No question asked")
    empty_icon = 'md md-live-help'


@asyn_component_config(id='novaideoapp_home')
@view_config(
    name='index',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
@view_config(
    name='',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class HomeView(MultipleView):
    title = ''
    name = ''
    behaviors = [SeeHome]
    anonymous_template = 'novaideo:views/novaideo_view_manager/templates/anonymous_view.pt'
    template = 'novaideo:views/templates/multipleview.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    viewid = 'home'
    css_class = 'simple-bloc'
    container_css_class = 'home'
    center_tabs = True
    views = (QuestionsView, IdeasView, ProposalsView)

    def _init_views(self, views, **kwargs):
        if self.params('load_view'):
            if self.request.is_idea_box:
                views = (IdeasView, )

            if self.params('view_content_type') == 'idea':
                views = (IdeasView, )

            if self.params('view_content_type') == 'proposal':
                views = (ProposalsView, )

            if self.params('view_content_type') == 'question':
                views = (QuestionsView, )

        super(HomeView, self)._init_views(views, **kwargs)

    def update_anonymous(self):
        values = {}
        result = {}
        body = self.content(
            args=values, template=self.anonymous_template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        self.title = ''
        self.wrapper_template = 'novaideo:views/novaideo_view_manager/templates/anonymous_view_wrapper.pt'
        return result

    def update(self):
        if not self.request.accessible_to_anonymous:
            return self.update_anonymous()

        return super(HomeView, self).update()


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeHome: HomeView})


FILTER_SOURCES.update(
    {"home": HomeView})
