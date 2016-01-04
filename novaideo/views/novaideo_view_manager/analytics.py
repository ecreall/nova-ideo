

import colander
import deform

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from dace.objectofcollaboration.entity import Entity
from dace.processinstance.core import Behavior
from pontus.schema import Schema, omit
from pontus.widget import (
    SequenceWidget, SimpleMappingWidget,
    RadioChoiceWidget, Select2Widget, FileWidget,
    AjaxSelect2Widget)
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.file import Object as ObjectType

from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeAnalytics)
from novaideo.utilities.analytics_utility import hover_color
from novaideo.content.processes import get_content_types_states
from novaideo import core, _, log
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.views.filter import (
    get_contents_by_keywords, get_contents_by_states)


DEFAULT_CONTENT_TYPES = ['idea', 'proposal']


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


class ContentsByStatesSchema(ContentsByKeywordsSchema):

    content_types = colander.SchemaNode(
        colander.String(),
        widget=content_type_choices,
        title=_('Type'),
        description=_('You can select the content type to be displayed.'),
        default=default_content_type,
        missing=default_content_type
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
    views = (ContentsByStatesView, ContentsByKeywordsView)
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
                filter_, user, root)
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
            'labels': dict(labels),
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
                filter_, user, root)
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
            'labels': dict(labels),
            'view': self,
            'charts': ['bar', 'doughnut'],
            'study': study,
            'id': 'states'}
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
