# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
from pyramid.view import view_config

from substanced.util import Batch

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView
from pontus.widget import CheckboxChoiceWidget
from pontus.schema import Schema
from pontus.form import FormView

from novaideo.content.processes.novaideo_view_manager.behaviors import Search
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from .widget import SearchTextInputWidget, SearchFormWidget
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.content.processes import get_states_mapping
from novaideo.views.filter import (
    get_filter, FilterView, FILTER_SOURCES, merge_with_filter_view, find_entities)


CONTENTS_MESSAGES = {
    '0': _(u"""No element found"""),
    '1': _(u"""One element found"""),
    '*': _(u"""${nember} elements found""")
}

DEFAULT_SEARCHABLE_CONTENT = [('idea', _('Ideas')),
                              ('proposal', _('Proposals')),
                              ('person', _('Persons'))
                            ]


@view_config(
    name='advanced_search',
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AdvancedSearchView(FilterView):
    title = _('Advanced search')
    name = 'advanced_search'
    behaviors = [Search]
    formid = 'formadvanced_search'
    wrapper_template = 'pontus:templates/views_templates/view_wrapper.pt'

    def update(self):
        self.calculate_posted_filter()
        if self.validated:
            result_view = SearchResultView(self.context, self.request)
            result_view.validated = self.validated
            result = result_view.update()
            return result
        else:
            return super(AdvancedSearchView, self).update()


@colander.deferred
def content_types_choices(node, kw):
    return CheckboxChoiceWidget(values=DEFAULT_SEARCHABLE_CONTENT,
                                inline=True,
                                css_class='search-choice',
                                item_css_class="search-choices")


@colander.deferred
def default_content_types_choices(node, kw):
    return [k[0] for k in DEFAULT_SEARCHABLE_CONTENT]


@colander.deferred
def text_to_search_widget(node, kw):
    request = node.bindings['request']
    choices = [{'id': 'search-choice-'+k[0],
               'title': k[1],
               'order': index} for index, k
               in enumerate(DEFAULT_SEARCHABLE_CONTENT)]
    choices = sorted(
        choices, key=lambda v: v['order'])
    advanced_search_url = request.resource_url(
        request.root, '@@advanced_search')
    return SearchTextInputWidget(
        button_type='submit',
        description=_("The keyword search is done using"
                      " commas between keywords."),
        advanced_search_url=advanced_search_url,
        placeholder=_("Search"),
        choices=choices)


class SearchSchema(Schema):
    widget = SearchFormWidget()

    content_types = colander.SchemaNode(
        colander.Set(),
        widget=content_types_choices,
        title='',
        default=default_content_types_choices,
        missing=default_content_types_choices,
        )

    text_to_search = colander.SchemaNode(
        colander.String(),
        widget=text_to_search_widget,
        title='',
        missing='',
        )


@view_config(
    name='search',
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SearchView(FormView):
    title = _('Search')
    name = 'search'
    coordinates = 'header'
    schema = SearchSchema()
    behaviors = [Search]
    formid = 'formsearch'
    wrapper_template = 'daceui:templates/simple_view_wrapper.pt'

    def calculate_posted_filter(self):
        post = getattr(self, 'postedform', self.request.POST or self.request.GET or {})
        form, reqts = self._build_form()
        form.formid = self.viewid + '_' + form.formid
        posted_formid = None
        default_content = [key[0] for key in DEFAULT_SEARCHABLE_CONTENT]
        default_content.remove("person")
        if '__formid__' in post:
            posted_formid = post['__formid__']

        if posted_formid is not None and posted_formid == form.formid:
            try:
                post = post.copy()
                controls = post.items()
                validated = form.validate(controls)
                self.executed = True
                if 'content_types' in validated:
                    return {'metadata_filter':
                                {'content_types': validated['content_types']},
                            'text_filter':
                                {'text_to_search': validated['text_to_search']}}
                else:
                    return {'metadata_filter':
                                {'content_types': default_content},
                            'text_filter':
                                {'text_to_search': validated['text_to_search']}}
            except Exception:
                pass

        content_types = self.params('content_types')
        text = self.params('text_to_search')
        if text is None:
            text = ''

        if content_types is None:
            content_types = default_content
        elif not isinstance(content_types, (list, tuple)):
            content_types = [content_types]

        return {'metadata_filter': {'content_types': content_types},
                'text_filter': {'text_to_search': text}}

    def before_update(self):
        root = getSite()
        self.action = self.request.resource_url(root, '')

    def default_data(self):
        appstruct = self.calculate_posted_filter()
        return {'content_types': appstruct.get(
                    'metadata_filter', {}).get('content_types', []),
                'text_to_search': appstruct.get(
                    'text_filter', {}).get('text_to_search', '')}


@view_config(
    name='',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SearchResultView(BasicView):
    title = _('Nova-Ideo contents')
    name = ''
    validators = [Search.get_validator()]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'search_result'

    def _add_filter(self, user):
        def source(**args):
            default_content = [key[0] for key in DEFAULT_SEARCHABLE_CONTENT]
            default_content.remove("person")
            filter_ = {
                'metadata_filter': {'content_types': default_content}
            }
            objects = find_entities(user=user, filters=[filter_], **args)
            return objects

        url = self.request.resource_url(self.context, '@@novaideoapi')
        return get_filter(
            self,
            url=url,
            source=source,
            select=['metadata_filter', 'geographic_filter',
                    'contribution_filter', 'temporal_filter',
                    'text_filter', 'other_filter'],
            filter_source="search_source")

    def update(self):
        user = get_current()
        validated = getattr(self, 'validated', {})
        posted = self.request.POST or self.request.GET or {}
        posted = posted.copy()
        executed = True if validated else False
        if not validated:
            formviewinstance = SearchView(self.context, self.request)
            formviewinstance.postedform = posted
            validated = formviewinstance.calculate_posted_filter()
            executed = getattr(formviewinstance, 'executed', False)

        filter_form = None
        if not executed:
            filter_form, filter_data = self._add_filter(user)
            default_content = [key[0] for key in DEFAULT_SEARCHABLE_CONTENT]
            default_content.remove("person")
            filter_ = {
                'metadata_filter': {'content_types': default_content}
            }
            validated = merge_with_filter_view(self, {})
            validated['request'] = self.request
            validated['filters'] = [filter_]

        objects = find_entities(
            user=user,
            sort_on='release_date', reverse=True,
            **validated)
        url = self.request.resource_url(self.context, self.request.view_name,
                                        query=posted)
        batch = Batch(objects,
                      self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(CONTENTS_MESSAGES[index],
                       mapping={'nember': len_result})

        filter_instance = getattr(self, 'filter_instance', None)
        filter_body = None
        if filter_instance:
            filter_data['filter_message'] = self.title
            filter_body = filter_instance.get_body(filter_data)

        result_body = []
        for obj in batch:
            render_dict = {'object': obj,
                           'current_user': user,
                           'state': get_states_mapping(user, obj,
                                   getattr(obj, 'state_or_none', [None])[0])}
            body = self.content(args=render_dict,
                                template=obj.templates['default'])['body']
            result_body.append(body)

        result = {}
        values = {'bodies': result_body,
                  'batch': batch,
                  'filter_body': filter_body}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        if filter_form:
            result['css_links'] = filter_form['css_links']
            result['js_links'] = filter_form['js_links']

        return result



        # result_body = []
        # for obj in batch:
        #     object_values = {'object': obj,
        #                      'current_user': user,
        #                      'state': get_states_mapping(user, obj,
        #                            getattr(obj, 'state', [None])[0])}
        #     body = self.content(args=object_values,
        #                         template=obj.templates.get('default'))['body']
        #     result_body.append(body)

        # result = {}
        # values = {
        #     'bodies': result_body,
        #     'length': len_result,
        #     'batch': batch
        # }
        # body = self.content(args=values, template=self.template)['body']
        # item = self.adapt_item(body, self.viewid)
        # result['coordinates'] = {self.coordinates: [item]}
        # result = merge_dicts(self.requirements_copy, result)
        # return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({Search: SearchView})


FILTER_SOURCES.update(
    {"search_source": SearchResultView})

#"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

# import colander
# import datetime
# from pyramid.view import view_config

# from substanced.util import Batch

# from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
# from dace.objectofcollaboration.principal.util import get_current
# from dace.util import getSite
# from pontus.view import BasicView
# from pontus.widget import Select2Widget
# from pontus.schema import Schema, select

# from creationculturelle.content.processes.creationculturelle_view_manager.behaviors import (
#     Search)
# from creationculturelle import _
# from .widget import SearchTextInputWidget, SearchFormWidget
# from creationculturelle.content.processes import get_states_mapping
# from creationculturelle.content.keyword import ROOT_TREE
# from creationculturelle import core
# from creationculturelle.views.filter import (
#     FilterView, find_entities, FilterSchema,
#     artists_choices, cities_choices,
#     DEFAULT_TREE)
# from creationculturelle.utilities.cinema_utility import next_weekday
# from creationculturelle.utilities.utils import get_month_range, deepcopy


# CONTENTS_MESSAGES = {
#     '0': _(u"""No element found"""),
#     '1': _(u"""One element found"""),
#     '*': _(u"""${nember} elements found""")
#     }


# def _whatever_dates():
#     return {
#         'start_date': None,
#         'end_date': None
#     }


# def _today_dates():
#     today = datetime.datetime.today()
#     return {
#         'start_date': today,
#         'end_date': today
#     }


# def _tomorrow_dates():
#     tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
#     return {
#         'start_date': tomorrow,
#         'end_date': tomorrow
#     }


# def _week_end_dates():
#     today = datetime.datetime.today()
#     start_weekend = next_weekday(today, 5)
#     end_weekend = next_weekday(today, 6)
#     return {
#         'start_date': start_weekend,
#         'end_date': end_weekend
#     }


# def _week_dates():
#     today = datetime.datetime.today()
#     end_weekend = next_weekday(today, 6)
#     return {
#         'start_date': today,
#         'end_date': end_weekend
#     }


# def _next_week_dates():
#     today = datetime.datetime.today()
#     start_weekend = next_weekday(today, 0, 1)
#     end_weekend = next_weekday(today, 6, 1)
#     return {
#         'start_date': start_weekend,
#         'end_date': end_weekend
#     }


# def _Within_15_dates():
#     start_weekend = datetime.datetime.today()
#     end_weekend = start_weekend + datetime.timedelta(days=15)
#     return {
#         'start_date': start_weekend,
#         'end_date': end_weekend
#     }


# def _one_month_dates():
#     today = datetime.datetime.today()
#     _, end_date = get_month_range(today)
#     return {
#         'start_date': today,
#         'end_date': end_date
#     }


# def _next_month_dates():
#     st_date, end_date = get_month_range(
#         datetime.datetime.today(),
#         next_month=True)
#     return {
#         'start_date': st_date,
#         'end_date': end_date
#     }


# DEFAULT_DATES = {
#     0: (_('Whatever'), _whatever_dates),
#     1: (_('Today'), _today_dates),
#     2: (_('Tomorrow'), _tomorrow_dates),
#     3: (_('This week-end'), _week_end_dates),
#     4: (_('This week'), _week_dates),
#     5: (_('Next week'), _next_week_dates),
#     6: (_('Within 15 days'), _Within_15_dates),
#     7: (_('Within one month'), _one_month_dates),
#     8: (_('Next month'), _next_month_dates)
# }


# @colander.deferred
# def thematic_widget(node, kw):
#     request = node.bindings['request']
#     values = request.get_site_folder.get_keywords_by_level()
#     if len(values) >= 1:
#         values = [(k, k) for k in sorted(values[1])]

#     return Select2Widget(values=values, multiple=True)


# @colander.deferred
# def dates_widget(node, kw):
#     values = [(k, v[0]) for k, v in
#               sorted(DEFAULT_DATES.items(), key=lambda e: e[0])]
#     return Select2Widget(values=values)


# class CalendarSearchSchema(FilterSchema):

#     thematics = colander.SchemaNode(
#         colander.Set(),
#         widget=thematic_widget,
#         title=_('Thematics'),
#         description=_('You can select the thematics of the cultural events to be displayed.'),
#         default=[],
#         missing=[]
#     )

#     city = colander.SchemaNode(
#         colander.Set(),
#         widget=cities_choices,
#         title=_('Where ?'),
#         default=[],
#         missing=[],
#         description=_("You can enter the names of the cities where cultural events to be displayed take place.")
#         )

#     dates = colander.SchemaNode(
#         colander.Int(),
#         widget=dates_widget,
#         title=_('When ?'),
#         missing=0,
#         description=_('You can select the dates of the cultural events to be displayed.')
#         )

#     artists_ids = colander.SchemaNode(
#         colander.Set(),
#         widget=artists_choices,
#         title=_('Artists'),
#         description=_('You can enter the artists names to display the associated contents.'),
#         default=[],
#         missing=[]
#         )

#     text_to_search = colander.SchemaNode(
#         colander.String(),
#         description=_("You can enter the words that appear in the cultural events to be displayed."),
#         title=_('keywords'),
#         default='',
#         missing=''
#     )

#     def deserialize(self, cstruct=colander.null):
#         appstruct = super(CalendarSearchSchema, self).deserialize(cstruct)
#         thematics = appstruct.get('thematics', [])
#         dates = appstruct.get('dates', 0)
#         appstruct = {
#             'metadata_filter': {
#                 'content_types': {'cultural_event'},
#                 'tree': deepcopy(DEFAULT_TREE)
#                 },
#             'text_filter': {
#                 'text_to_search': appstruct.pop('text_to_search', '')
#                 },
#             'contribution_filter': {
#                 'artists_ids': appstruct.pop('artists_ids', [])
#                 },
#             'geographic_filter': {
#                 'city': appstruct.pop('city', [])
#                 },
#             'temporal_filter': {
#                 'start_end_dates': DEFAULT_DATES[dates][1]()
#                 }
#         }
#         for thematic in thematics:
#             appstruct['metadata_filter']['tree'][ROOT_TREE][thematic] = {}

#         return appstruct


# @view_config(
#     name='advanced_search',
#     renderer='pontus:templates/views_templates/grid.pt',
#     )
# class AdvancedSearchView(FilterView):
#     title = _('Advanced search')
#     name = 'advanced_search'
#     behaviors = [Search]
#     formid = 'formadvanced_search'
#     wrapper_template = 'pontus:templates/views_templates/view_wrapper.pt'

#     def before_update(self):
#         if not self.request.user:
#             self.schema = select(CalendarSearchSchema(),
#                                  ['thematics', 'city',
#                                   'dates',
#                                   'artists_ids',
#                                   'text_to_search'])

#         return super(AdvancedSearchView, self).before_update()

#     def update(self):
#         self.calculate_posted_filter()
#         if self.validated:
#             result_view = SearchResultView(self.context, self.request)
#             result_view.validated = self.validated
#             result = result_view.update()
#             return result
#         else:
#             return super(AdvancedSearchView, self).update()


# @view_config(
#     name='search_result',
#     renderer='pontus:templates/views_templates/grid.pt',
#     )
# class SearchResultView(BasicView):
#     title = ''
#     name = 'search_result'
#     validators = [Search.get_validator()]
#     template = 'creationculturelle:views/creationculturelle_view_manager/templates/search_result.pt'
#     viewid = 'search_result'

#     def update(self):
#         self.execute(None)
#         user = get_current()
#         validated = getattr(self, 'validated', {})
#         posted = self.request.POST or self.request.GET or {}
#         posted = posted.copy()
#         clear_posted = False
#         if not validated:
#             if posted:
#                 clear_posted = True
#                 searcinstance = SearchView(self.context, self.request,
#                                            filter_result=True)
#                 if searcinstance.validated:
#                     validated = searcinstance.validated

#         objects = find_entities(
#             user=user,
#             sort_on='release_date', reverse=True,
#             include_site=True,
#             **validated)
#         url = self.request.resource_url(
#             self.context, self.request.view_name, query=posted)
#         batch = Batch(objects, self.request,
#                       default_size=core.BATCH_DEFAULT_SIZE,
#                       url=url)
#         #clear posted values: See usermenu panel
#         if clear_posted:
#             if self.request.POST:
#                 self.request.POST.clear()
#             elif self.request.GET:
#                 self.request.GET.clear()

#         batch.target = "#results_contents"
#         len_result = batch.seqlen
#         index = str(len_result)
#         if len_result > 1:
#             index = '*'

#         self.title = _(CONTENTS_MESSAGES[index],
#                        mapping={'nember': len_result})
#         result_body = []
#         for obj in batch:
#             render_dict = {'object': obj,
#                            'current_user': user,
#                            'state': get_states_mapping(user, obj,
#                                    getattr(obj, 'state_or_none', [None])[0])}
#             body = self.content(args=render_dict,
#                                 template=obj.templates['default'])['body']
#             result_body.append(body)

#         result = {}
#         values = {'bodies': result_body,
#                   'batch': batch}
#         body = self.content(args=values, template=self.template)['body']
#         item = self.adapt_item(body, self.viewid)
#         result['coordinates'] = {self.coordinates: [item]}
#         return result

#     def before_update(self):
#         super(SearchResultView, self).before_update()
#         self.title = _('${creationculturelle_title} contents',
#               mapping={'creationculturelle_title': self.request.root.title})


# @colander.deferred
# def text_to_search_widget(node, kw):
#     context = node.bindings['context']
#     request = node.bindings['request']
#     root = getSite()
#     ajax_url = request.resource_url(context,
#                                     '@@creationculturelapi',
#                                     query={'op': 'find_entities'})
#     advanced_search_url = request.resource_url(
#         root, '@@advanced_search')
#     return SearchTextInputWidget(
#         url=ajax_url,
#         advanced_search_url=advanced_search_url,
#         placeholder=_('Ex. théâtre le 13 juillet'))


# class SearchSchema(Schema):
#     widget = SearchFormWidget()

#     text_to_search = colander.SchemaNode(
#         colander.String(),
#         widget=text_to_search_widget,
#         title='',
#         default='',
#         missing='',
#         )

#     def deserialize(self, cstruct=colander.null):
#         appstruct = super(SearchSchema, self).deserialize(cstruct)
#         appstruct = {
#             'text_filter':
#             {'text_to_search': appstruct.pop('text_to_search', '')},
#         }
#         return appstruct


# @view_config(
#     name='simple_search',
#     renderer='pontus:templates/views_templates/grid.pt',
#     )
# class SearchView(FilterView):
#     title = _('Search')
#     name = 'search'
#     schema = select(SearchSchema(), ['text_to_search'])
#     behaviors = [Search]
#     formid = 'formsearch'
#     wrapper_template = 'daceui:templates/simple_view_wrapper.pt'

#     def before_update(self):
#         self.schema = select(SearchSchema(), ['text_to_search'])
#         root = getSite()
#         self.action = self.request.resource_url(
#             root, '@@search_result')


# DEFAULTMAPPING_ACTIONS_VIEWS.update({Search: AdvancedSearchView})
