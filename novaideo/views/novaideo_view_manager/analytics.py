

import colander
import deform

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from dace.objectofcollaboration.entity import Entity
from dace.processinstance.core import Behavior
from pontus.schema import Schema
from pontus.widget import (
    SequenceWidget, SimpleMappingWidget,
    RadioChoiceWidget, Select2Widget, FileWidget)
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView

from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeAnalytics)
from novaideo.utilities.analytics_utility import hover_color
from novaideo.content.processes import get_content_types_states
from novaideo import core, _
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.views.filter import (
    get_contents_by_keywords, get_contents_by_states)


DEFAULT_CONTENT_TYPES = ['idea', 'proposal']



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
def states_choices(node, kw):
    request = node.bindings['request']
    localizer = request.localizer
    states_mapping = get_content_types_states(DEFAULT_CONTENT_TYPES, True)
    values = [(k, ', '.join([localizer.translate(st)
                       for st in states_mapping[k]]))
              for k in sorted(states_mapping.keys())]

    return Select2Widget(values=values, multiple=True)


@colander.deferred
def content_types_choices(node, kw):
    content_to_examine = DEFAULT_CONTENT_TYPES
    values = [(key, getattr(c, 'type_title', c.__class__.__name__))
              for key, c in list(core.SEARCHABLE_CONTENTS.items())
              if key in content_to_examine]
    return Select2Widget(values=values, multiple=True)


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
        default=DEFAULT_CONTENT_TYPES,
        missing=DEFAULT_CONTENT_TYPES
    )

    states = colander.SchemaNode(
        colander.Set(),
        widget=states_choices,
        title=_('States'),
        description=_('You can select the states of the contents to be displayed.'),
        default=[],
        missing=[]
    )

    keywords = colander.SchemaNode(
        colander.Set(),
        widget=keywords_choice,
        title=_('Keywords'),
        description=_("You can select the keywords of the contents to be displayed."),
        missing=[]
        )


class Send(Behavior):

    behavior_id = "send"
    title = _("Send")
    description = ""

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, ""))


class ContentsByKeywordsForm(FormView):
    title = _('Contents by keywords')
    schema = ContentsByKeywordsSchema()
    behaviors = [Send]
    formid = 'content_by_keywords_form'
    name = 'content_by_keywords_form'

    def before_update(self):
        formwidget = deform.widget.FormWidget(
            css_class='analytics-form filter-form well')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        formwidget.ajax_url = self.request.resource_url(
            self.context, '@@analyticsapi', query={'op': 'contents_by_keywords'})
        self.schema.widget = formwidget


class ContentsByKeywordsView(MultipleView):
    title = _('Contents by keywords')
    name = 'content_by_keywords_view'
    template = 'novaideo:views/templates/simple_mergedmultipleview.pt'
    views = (ContentsByKeywordsForm, ContentsByKeywords)


#****************************** Content by states ***********************************

class ContentsByStates(BasicView):
    title = _('Contents by states')
    name = 'content_by_keywords'
    # validators = [Search.get_validator()]
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
    content_to_examine = DEFAULT_CONTENT_TYPES
    values = [(key, getattr(c, 'type_title', c.__class__.__name__))
              for key, c in list(core.SEARCHABLE_CONTENTS.items())
              if key in content_to_examine]
    return Select2Widget(values=values)


class ContentsByStatesSchema(ContentsByKeywordsSchema):

    content_types = colander.SchemaNode(
        colander.String(),
        widget=content_type_choices,
        title=_('Type'),
        description=_('You can select the content type to be displayed.'),
        default='proposal',
        missing='proposal'
    )


class ContentsByStatesForm(FormView):
    title = _('Contents by states')
    schema = ContentsByStatesSchema()
    behaviors = [Send]
    formid = 'content_by_states_form'
    name = 'content_by_states_form'

    def before_update(self):
        formwidget = deform.widget.FormWidget(
            css_class='analytics-form filter-form well')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        formwidget.ajax_url = self.request.resource_url(
            self.context, '@@analyticsapi', query={'op': 'contents_by_states'})
        self.schema.widget = formwidget


class ContentsByStatesView(MultipleView):
    title = _('Contents by states')
    name = 'content_by_states_view'
    template = 'novaideo:views/templates/simple_mergedmultipleview.pt'
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

    def get_color(self, key, index=1, is_hover=False):
        root = self.request.root
        return root.get_color(key)

    def contents_by_keywords(self):
        states = self.params('states')
        keywords = self.params('keywords')
        types = self.params('content_types')
        results = {}
        user = get_current()
        root = self.request.root
        if types is None:
            types = []
        elif not isinstance(types, (list, tuple)):
            types = [types]

        if states is None:
            states = []
        elif not isinstance(states, (list, tuple)):
            states = [states]

        if keywords is None:
            keywords = []
        elif not isinstance(keywords, (list, tuple)):
            keywords = [keywords]

        for type_ in types:
            title = getattr(
                core.SEARCHABLE_CONTENTS.get(type_), 'type_title', type_)
            filter_ = {'metadata_filter': {
                'content_types': [type_],
                'states': states,
                'keywords': keywords
            }}
            results[title] = {
                'data': get_contents_by_keywords(
                    filter_, user, root),
                'color': self.color_mapping.get(type_)
                }
        labels = [list(v['data'].keys()) for v in results.values()]
        labels = sorted(list(set([item for sublist in labels
                                  for item in sublist
                                  if not keywords or item in keywords])))
        values = {'analytics': results,
                  'labels': labels,
                  'view': self,
                  'charts': ['bar', 'doughnut'],
                  'id': 'keywords'}
        body = self.content(
            args=values, template=self.analytics_template)['body']
        return {'body': body}

    def contents_by_states(self):
        states = self.params('states')
        keywords = self.params('keywords')
        types = self.params('content_types')
        results = {}
        user = get_current()
        root = self.request.root
        if types is None:
            types = []
        elif not isinstance(types, (list, tuple)):
            types = [types]

        if states is None:
            states = []
        elif not isinstance(states, (list, tuple)):
            states = [states]

        if keywords is None:
            keywords = []
        elif not isinstance(keywords, (list, tuple)):
            keywords = [keywords]

        flattened_states = get_content_types_states(types, True)
        if not states:
            states = list(flattened_states.keys())

        for type_ in types:
            title = getattr(
                core.SEARCHABLE_CONTENTS.get(type_), 'type_title', type_)
            filter_ = {'metadata_filter': {
                'content_types': [type_],
                'states': states,
                'keywords': keywords
            }}
            results[title] = {
                'data': get_contents_by_states(
                    filter_, user, root, self.request),
                'color': self.color_mapping.get(type_)
                }

        localizer = self.request.localizer
        states = [flattened_states[s] for s in states if s in flattened_states]
        states = list(set([localizer.translate(item) for sublist in states
                           for item in sublist]))
        labels = [list(v['data'].keys()) for v in results.values()]
        labels = sorted(list(set([item for sublist in labels
                                  for item in sublist
                                  if not states or item in states])))
        values = {'analytics': results,
                  'labels': labels,
                  'view': self,
                  'charts': ['bar', 'doughnut'],
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
