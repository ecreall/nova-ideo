# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

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
    '*': _(u"""${number} elements found""")
}


class ContentView(BasicView):
    template = 'novaideo:views/novaideo_view_manager/templates/home.pt'
    anonymous_template = 'novaideo:views/novaideo_view_manager/templates/anonymous_view.pt'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    content_type = 'idea'
    isactive = False
    hasparent = True
    filter_class = ''
    view_filter = [('metadata_filter', ['states', 'keywords', 'challenges']), 'geographic_filter',
                  'contribution_filter',
                  ('temporal_filter', ['negation', 'created_date']),
                  'text_filter', 'other_filter']
    
    def _get_validated(self, validated, user):
        return validated

    def _add_filter(self, user):
        def source(**args):
            default_content = [self.content_type]
            filter_ = self._get_validated({
                'metadata_filter':
                    {'content_types': default_content,
                    'states': ['active', 'published']},
            }, user)
            objects = find_entities(user=user, filters=[filter_], **args)
            return objects

        url = self.request.resource_url(
            self.context, '@@novaideoapi',
            query={'view_content_id': self.content_id})
        return get_filter(
            self,
            url=url,
            source=source,
            select=self.view_filter,
            filter_source="home",
            filterid=self.viewid)

    def update(self):
        body = ''
        result = {}
        if self.isactive or self.params('on_demand') == 'load':
            user = get_current()
            filter_form, filter_data = self._add_filter(user)
            default_content = [self.content_type]
            validated = self._get_validated({
                'metadata_filter':
                    {'content_types': default_content,
                    'states': ['active', 'published']},
            }, user)
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
                query={'view_content_id': self.content_id})
            batch = Batch(objects,
                          self.request,
                          url=url,
                          default_size=BATCH_DEFAULT_SIZE)
            self.title = _(self.title, mapping={'nb': batch.seqlen})
            batch.target = "#results-" + self.content_id
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


class IdeasView(ContentView):
    title = _('Ideas')
    content_type = 'idea'
    content_id = 'home-ideas'
    viewid = 'home-ideas'
    view_icon = 'icon novaideo-icon icon-idea'
    counter_id = 'home-ideas-counter'
    empty_message = _("No registered ideas")
    empty_icon = 'icon novaideo-icon icon-idea'
    isactive = True


@asyn_component_config(
    id='home-proposals',
    on_demand=True,
    delegate='novaideoapp_home')
class ProposalsView(ContentView):
    title = _('The Working Groups')
    content_type = 'proposal'
    content_id = 'home-proposals'
    viewid = 'home-proposals'
    view_icon = 'icon novaideo-icon icon-wg'
    counter_id = 'home-proposals-counter'
    empty_message = _("No working group created")
    empty_icon = 'icon novaideo-icon icon-wg'


@asyn_component_config(
    id='home-questions',
    on_demand=True,
    delegate='novaideoapp_home')
class QuestionsView(ContentView):
    title = _('Questions')
    content_type = 'question'
    content_id = 'home-questions'
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
    css_class = 'transparent-panel contents-bloc async-new-contents-component'
    center_tabs = True
    views = (QuestionsView, IdeasView, ProposalsView)

    def _init_views(self, views, **kwargs):
        if self.params('load_view'):
            delegated_by = kwargs.get('delegated_by', None)
            views = [IdeasView]
            if 'question' in self.request.content_to_manage:
                views = [QuestionsView, IdeasView]

            if 'proposal' in self.request.content_to_manage:
                views.append(ProposalsView)

            views = tuple(views)
            view_id = self.params('view_content_id')
            if view_id in ('home-ideas', 'pole-home-ideas'):
                views = (IdeasView, )

            if 'home-proposals' in (delegated_by, view_id):
                views = (ProposalsView, )

            if 'home-questions' in (delegated_by, view_id):
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
