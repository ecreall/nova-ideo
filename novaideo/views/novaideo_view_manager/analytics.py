
import datetime
import colander
import deform

from collections import OrderedDict
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from dace.objectofcollaboration.entity import Entity
from dace.processinstance.core import Behavior
from pontus.schema import Schema, omit, select
from pontus.widget import (
    SimpleMappingWidget,
    Select2Widget,
    AjaxSelect2Widget)
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.file import Object as ObjectType

from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeAnalytics)
from novaideo.utilities.analytics_utility import hover_color
from novaideo.utilities.util import to_localized_time
from novaideo.content.processes import get_content_types_states
from novaideo import core, _, log
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.views.filter import (
    get_contents_by_keywords, get_contents_by_states,
    get_contents_by_dates)


DEFAULT_CONTENT_TYPES = ['idea', 'proposal']


DATESOF = [
    ('publication', _('Publication')),
    ('examination', _('Examination'))
]


DATE_FORMAT = {
    'day': '%d/%m/%Y',
    'month': '%m/%Y',
    'year': '%Y'
}


FREQUENCY = [
    ('day', _('Day')),
    ('month', _('Month')),
    ('year', _('Year'))
]


class Compute(Behavior):

    behavior_id = "compute"
    title = _("Compute")
    description = ""

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, ""))


class AnalyticsForm(FormView):

    behaviors = [Compute]

    def calculate_posted_filter(self):
        try:
            form_data = self._build_form()
            values = self.request.POST or self.request.GET
            controls = values.items()
            validated = form_data[0].validate(controls)
            setattr(self, 'validated', validated)
        except Exception as e:
            log.warning(e)


#****************************** Content by keywords ***********************************

class ContentsByKeywords(BasicView):
    title = _('Contents by keywords')
    name = 'content_by_keywords'
    # validators = [Search.get_validator()]
    template = 'novaideo:views/novaideo_view_manager/templates/charts.pt'
    viewid = 'content_by_keywords'

    def update(self):
        result = {}
        values = {
            'id': 'keywords',
            'row_len': 2,
            'charts': [
                {
                    'id': 'bar',
                    'title': _('Total des contenus classé par types par mots clés')
                },
                {
                    'id': 'doughnut',
                    'title': _('Pourcentage du cumul par mots clés')
                }
            ]
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


@colander.deferred
def authors_choices(node, kw):
    """"""
    context = node.bindings['context']
    request = node.bindings['request']
    values = []

    def title_getter(oid):
        author = None
        try:
            author = get_obj(int(oid))
        except Exception:
            return oid

        title = getattr(author, 'title', author.__name__)
        return title

    ajax_url = request.resource_url(context,
                                    '@@novaideoapi',
                                    query={'op': 'find_user'})
    return AjaxSelect2Widget(
        values=values,
        ajax_url=ajax_url,
        multiple=False,
        title_getter=title_getter)


@colander.deferred
def states_choices(node, kw):
    request = node.bindings['request']
    localizer = request.localizer
    states_mapping = get_content_types_states(
        request.analytics_default_content_types, True)
    values = [(k, ', '.join([localizer.translate(st)
                             for st in states_mapping[k]]))
              for k in sorted(states_mapping.keys())]

    return Select2Widget(values=values, multiple=True)


@colander.deferred
def content_types_choices(node, kw):
    request = node.bindings['request']
    values = [(key, getattr(c, 'type_title', c.__class__.__name__))
              for key, c in list(core.SEARCHABLE_CONTENTS.items())
              if key in request.analytics_default_content_types]
    return Select2Widget(values=values, multiple=True)


@colander.deferred
def default_content_types(node, kw):
    request = node.bindings['request']
    if request.is_idea_box:
        return ['idea']

    return ['proposal']


@colander.deferred
def keywords_choice(node, kw):
    context = node.bindings['context']
    values = [(i, i) for i in sorted(context.keywords)]
    return Select2Widget(values=values,
                         create=False,
                         multiple=True)


class PublicationDates(Schema):

    date_from = colander.SchemaNode(
        colander.Date(),
        title=_('From'),
        missing=None
        )

    date_to = colander.SchemaNode(
        colander.Date(),
        title=_('To'),
        description_bottom=True,
        description=_('You can select the dates of contents to be displayed.'),
        missing=None,
        )


class ContentsByKeywordsSchema(Schema):

    content_types = colander.SchemaNode(
        colander.Set(),
        widget=content_types_choices,
        title=_('Types'),
        description=_('You can select the content types to be displayed.'),
        default=default_content_types,
        missing=default_content_types
    )

    states = colander.SchemaNode(
        colander.Set(),
        widget=states_choices,
        title=_('States'),
        description=_('You can select the states of the contents to be displayed.'),
        default=['published'],
        missing=['published']
    )

    keywords = colander.SchemaNode(
        colander.Set(),
        widget=keywords_choice,
        title=_('Keywords'),
        description=_("You can select the keywords of the contents to be displayed."),
        missing=[]
        )

    author = colander.SchemaNode(
        ObjectType(),
        widget=authors_choices,
        title=_('Author'),
        description=_('You can enter the author name of the contents to be displayed.'),
        default=None,
        missing=None
        )


    dates = omit(PublicationDates(
        widget=SimpleMappingWidget(css_class="filter-block"
                                             " object-well"
                                             " default-well")
        ),
            ["_csrf_token_"])


class ContentsByKeywordsForm(AnalyticsForm):
    title = _('Contents by keywords')
    schema = ContentsByKeywordsSchema()
    formid = 'content_by_keywords_form'
    name = 'content_by_keywords_form'

    def before_update(self):
        if len(self.request.analytics_default_content_types) == 1:
            self.schema = omit(self.schema, ['content_types'])

        formwidget = deform.widget.FormWidget(
            css_class='analytics-form filter-form well')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        formwidget.ajax_url = self.request.resource_url(
            self.context, '@@analyticsapi', query={'op': 'contents_by_keywords'})
        self.schema.widget = formwidget


class ContentsByKeywordsView(MultipleView):
    title = _('Contents by keywords')
    name = 'content_by_keywords_view'
    template = 'novaideo:views/templates/row_merged_multiple_view.pt'
    views = (ContentsByKeywordsForm, ContentsByKeywords)


#****************************** Content by states ***********************************

class ContentsByStates(BasicView):
    title = _('Contents by states')
    name = 'content_by_keywords'
    template = 'novaideo:views/novaideo_view_manager/templates/charts.pt'
    viewid = 'content_by_states'

    def update(self):
        result = {}
        values = {
            'id': 'states',
            'row_len': 2,
            'charts': [
                {
                    'id': 'bar',
                    'title': _('Total des contenus classé par types par états')
                },
                {
                    'id': 'doughnut',
                    'title': _('Pourcentage du cumul par états')
                }
            ]
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


@colander.deferred
def content_type_choices(node, kw):
    request = node.bindings['request']
    values = [(key, getattr(c, 'type_title', c.__class__.__name__))
              for key, c in list(core.SEARCHABLE_CONTENTS.items())
              if key in request.analytics_default_content_types]
    return Select2Widget(values=values)


@colander.deferred
def default_content_type(node, kw):
    request = node.bindings['request']
    if request.is_idea_box:
        return 'idea'

    return 'proposal'


@colander.deferred
def default_states(node, kw):
    request = node.bindings['request']
    to_exclude = ['draft', 'published', 'archived',
                  'favorable', 'to_study', 'unfavorable',
                  'to work']
    default = get_content_types_states(['proposal'])['proposal']
    if request.is_idea_box:
        default = get_content_types_states(['idea'])['idea']

    [default.pop(s) for s in to_exclude if s in default]
    return default


class ContentsByStatesSchema(ContentsByKeywordsSchema):

    content_types = colander.SchemaNode(
        colander.String(),
        widget=content_type_choices,
        title=_('Type'),
        description=_('You can select the content type to be displayed.'),
        default=default_content_type,
        missing=default_content_type
    )

    states = colander.SchemaNode(
        colander.Set(),
        widget=states_choices,
        title=_('States'),
        description=_('You can select the states of the contents to be displayed.'),
        default=default_states,
        missing=default_states
    )


class ContentsByStatesForm(AnalyticsForm):
    title = _('Contents by states')
    schema = ContentsByStatesSchema()
    formid = 'content_by_states_form'
    name = 'content_by_states_form'

    def before_update(self):
        if len(self.request.analytics_default_content_types) == 1:
            self.schema = omit(self.schema, ['content_types'])

        formwidget = deform.widget.FormWidget(
            css_class='analytics-form filter-form well')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        formwidget.ajax_url = self.request.resource_url(
            self.context, '@@analyticsapi', query={'op': 'contents_by_states'})
        self.schema.widget = formwidget


class ContentsByStatesView(MultipleView):
    title = _('Contents by states')
    name = 'content_by_states_view'
    template = 'novaideo:views/templates/row_merged_multiple_view.pt'
    views = (ContentsByStatesForm, ContentsByStates)


#****************************** Content by Dates ***********************************

class ContentsByDates(BasicView):
    title = _('Contents by dates')
    name = 'content_by_dates'
    # validators = [Search.get_validator()]
    template = 'novaideo:views/novaideo_view_manager/templates/charts.pt'
    viewid = 'content_by_dates'

    def update(self):
        result = {}
        values = {
            'id': 'dates',
            'row_len': 2,
            'charts': [
                {
                    'id': 'line',
                    'title': _('Total des contenus classé par types par date')
                }
            ]
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


@colander.deferred
def date_of_choices(node, kw):
    return Select2Widget(values=DATESOF, multiple=False)


@colander.deferred
def frequency_of_choices(node, kw):
    return Select2Widget(values=FREQUENCY, multiple=False)


class IntervalDates(Schema):

    date_of = colander.SchemaNode(
        colander.String(),
        widget=date_of_choices,
        title=_('Date type'),
        description=_('You can select the date type.'),
        default='publication',
        missing='publication'
    )

    frequency = colander.SchemaNode(
        colander.String(),
        widget=frequency_of_choices,
        title=_('Frequency'),
        description=_('You can select the frequency.'),
        default='month',
        missing='month'
    )

    date_from = colander.SchemaNode(
        colander.Date(),
        title=_('From'),
        missing=None
        )

    date_to = colander.SchemaNode(
        colander.Date(),
        title=_('To'),
        description_bottom=True,
        description=_('You can select the dates of contents to be displayed.'),
        missing=None,
        )


class ContentsByDatesSchema(ContentsByKeywordsSchema):

    dates = omit(IntervalDates(
        widget=SimpleMappingWidget(css_class="filter-block"
                                             " object-well"
                                             " default-well")
        ),
            ["_csrf_token_"])


class ContentsByDatesForm(AnalyticsForm):
    title = _('Contents by dates')
    schema = select(ContentsByDatesSchema(),
                    ['content_types', 'keywords', 'author', 'dates'])
    formid = 'content_by_dates_form'
    name = 'content_by_dates_form'

    def before_update(self):
        if len(self.request.analytics_default_content_types) == 1:
            self.schema = omit(self.schema, ['content_types'])

        if len(self.request.content_to_examine) == 0:
            self.schema = omit(self.schema, [('dates', ['date_of'])])

        formwidget = deform.widget.FormWidget(
            css_class='analytics-form filter-form well')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        formwidget.ajax_url = self.request.resource_url(
            self.context, '@@analyticsapi', query={'op': 'contents_by_dates'})
        self.schema.widget = formwidget


class ContentsByDatesView(MultipleView):
    title = _('Contents by dates')
    name = 'content_by_dates_view'
    template = 'novaideo:views/templates/row_merged_multiple_view.pt'
    views = (ContentsByDatesForm, ContentsByDates)



#****************************** Content by states ***********************************


@view_config(
    name='analytics',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AnalyticsView(MultipleView):
    title = _('Analytics')
    name = 'analytics'
    validators = [SeeAnalytics.get_validator()]
    template = 'novaideo:views/templates/resizable_multipleview.pt'
    views = (ContentsByStatesView, ContentsByKeywordsView, ContentsByDatesView)
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/chartjs/Chart.js',
                                 'novaideo:static/js/analytics.js']}


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeAnalytics: AnalyticsView})


@view_config(name='analyticsapi',
             context=Entity,
             xhr=True,
             renderer='json')
class AnalyticsAPIJsonView(BasicView):
    analytics_template = 'novaideo:views/novaideo_view_manager/templates/analytics.pt'
    analytics_study = 'novaideo:views/novaideo_view_manager/templates/charts_study.pt'
    color_mapping = {
        'idea': {
            'background': '#adcce7',
            'hover': hover_color('#adcce7')
        },
        'proposal': {
            'background': '#959595',
            'hover': hover_color('#959595')
        }
    }

    def get_color(self, key):
        root = self.request.root
        return root.get_color(key)

    def contents_by_keywords(self):
        results = {}
        user = get_current()
        root = self.request.root
        formview = ContentsByKeywordsForm(self.context, self.request)
        formview.calculate_posted_filter()
        validated = getattr(formview, 'validated', {})
        default_contents = self.request.analytics_default_content_types
        states = validated.get('states', [])
        keywords = validated.get('keywords', [])
        types = validated.get('content_types', default_contents)
        author = validated.get('author', None)
        date_date = validated.get('dates', {})
        date_from = date_date.get('date_from', None)
        date_to = date_date.get('date_to', None)
        contribution_filter = {'authors': []}
        if author is not None:
            contribution_filter = {'authors': [author]}

        localizer = self.request.localizer
        has_value = False
        for type_ in types:
            title = getattr(
                core.SEARCHABLE_CONTENTS.get(type_), 'type_title', type_)
            filter_ = {
                'metadata_filter': {
                    'content_types': [type_],
                    'states': states,
                    'keywords': keywords
                },
                'contribution_filter': contribution_filter
            }
            data = get_contents_by_keywords(
                filter_, user, root, date_from, date_to)
            has_value = has_value or data[1] > 0
            results[localizer.translate(title)] = {
                'data': data[0],
                'len': data[1],
                'color': self.color_mapping.get(type_)
                }

        labels = [list(v['data'].keys()) for v in results.values()]
        labels = sorted(list(set([(item, item) for sublist in labels
                                  for item in sublist
                                  if not keywords or item in keywords])))
        study = self.content(
            args={'results': results}, template=self.analytics_study)['body']
        values = {
            'has_value': has_value,
            'analytics': results,
            'labels': OrderedDict(labels),
            'view': self,
            'charts': ['bar', 'doughnut'],
            'study': study,
            'id': 'keywords'}
        body = self.content(
            args=values, template=self.analytics_template)['body']
        return {'body': body}

    def contents_by_states(self):
        results = {}
        user = get_current()
        root = self.request.root
        formview = ContentsByStatesForm(self.context, self.request)
        formview.calculate_posted_filter()
        validated = getattr(formview, 'validated', {})
        default_content = 'proposal'
        if self.request.is_idea_box:
            default_content = 'idea'

        states = validated.get('states', [])
        keywords = validated.get('keywords', [])
        type_ = validated.get('content_types', default_content)
        author = validated.get('author', None)
        date_date = validated.get('dates', {})
        date_from = date_date.get('date_from', None)
        date_to = date_date.get('date_to', None)
        contribution_filter = {'authors': []}
        if author is not None:
            contribution_filter = {'authors': [author]}

        flattened_states = get_content_types_states([type_], True)
        if not states:
            states = list(flattened_states.keys())

        localizer = self.request.localizer
        has_value = False
        if type_ is not None:
            title = getattr(
                core.SEARCHABLE_CONTENTS.get(type_), 'type_title', type_)
            filter_ = {
                'metadata_filter': {
                    'content_types': [type_],
                    'states': states,
                    'keywords': keywords
                },
                'contribution_filter': contribution_filter}
            data = get_contents_by_states(
                filter_, user, root, date_from, date_to)
            has_value = has_value or data[1] > 0
            results[localizer.translate(title)] = {
                'data': data[0],
                'len': data[1],
                'color': self.color_mapping.get(type_)
                }

        states = dict([(s, ', '.join([localizer.translate(k) for k
                                      in flattened_states[s]]))
                       for s in states if s in flattened_states])
        labels = [list(v['data'].keys()) for v in results.values()]
        labels = sorted(list(set([(item, states[item]) for sublist in labels
                                  for item in sublist
                                  if not states or item in states])))
        study = self.content(
            args={'results': results}, template=self.analytics_study)['body']
        values = {
            'has_value': has_value,
            'analytics': results,
            'labels': OrderedDict(labels),
            'view': self,
            'charts': ['bar', 'doughnut'],
            'study': study,
            'id': 'states'}
        body = self.content(
            args=values, template=self.analytics_template)['body']
        return {'body': body}

    def contents_by_dates(self):
        results = {}
        user = get_current()
        root = self.request.root
        formview = ContentsByDatesForm(self.context, self.request)
        formview.calculate_posted_filter()
        validated = getattr(formview, 'validated', {})
        default_contents = self.request.analytics_default_content_types
        content_types = validated.get('content_types', default_contents)
        date_date = validated.get('dates', {})
        date_of = date_date.get('date_of', 'publication')
        frequency = date_date.get('frequency', 'month')
        date_from = date_date.get('date_from', None)
        date_to = date_date.get('date_to', None)
        if date_of == 'publication':
            states = ['published']
        else:
            states = ['examined']

        keywords = validated.get('keywords', [])
        author = validated.get('author', None)
        contribution_filter = {'authors': []}
        if author is not None:
            contribution_filter = {'authors': [author]}

        localizer = self.request.localizer
        has_value = False
        for type_ in content_types:
            title = getattr(
                core.SEARCHABLE_CONTENTS.get(type_), 'type_title', type_)
            filter_ = {
                'metadata_filter': {
                    'content_types': [type_],
                    'states': states,
                    'keywords': keywords
                },
                'contribution_filter': contribution_filter}
            data = get_contents_by_dates(
                filter_, user, root,
                date_of, frequency, date_from, date_to)
            has_value = has_value or data[1] > 0
            results[localizer.translate(title)] = {
                'data': data[0],
                'len': data[1],
                'color': self.color_mapping.get(type_)
                }

        ignore_day = frequency != 'day'
        ignore_month = frequency == 'year'
        date_format = DATE_FORMAT.get(frequency)

        def to_localized(date_str):
            """To localized date"""
            date = datetime.datetime.strptime(
                date_str, date_format)
            return to_localized_time(
                date, self.request,
                date_only=True,
                ignore_month=ignore_month, ignore_day=ignore_day,
                force_ignore=True, translate=True)

        labels = [list(v['data'].keys()) for v in results.values()]
        labels = list(set([(item, to_localized(item)) for sublist in labels
                           for item in sublist]))
        labels = sorted(labels,
                        key=lambda e: datetime.datetime.strptime(
                            e[0], date_format))
        study = self.content(
            args={'results': results}, template=self.analytics_study)['body']
        values = {
            'has_value': has_value,
            'analytics': results,
            'labels': OrderedDict(labels),
            'view': self,
            'charts': ['line'],
            'study': study,
            'id': 'dates'}
        body = self.content(
            args=values, template=self.analytics_template)['body']
        return {'body': body}

    def __call__(self):
        operation_name = self.params('op')
        if operation_name is not None:
            operation = getattr(self, operation_name, None)
            if operation is not None:
                return operation()

        return {}
