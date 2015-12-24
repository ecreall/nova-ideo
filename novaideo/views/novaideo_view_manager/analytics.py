

import colander
import deform

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from dace.objectofcollaboration.principal.util import get_current
from dace.objectofcollaboration.entity import Entity
from dace.processinstance.core import Behavior
from pontus.schema import Schema
from pontus.widget import (
    SequenceWidget, SimpleMappingWidget,
    CheckboxChoiceWidget, Select2Widget, FileWidget)
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView

from novaideo.utilities.analytics_utility import hover_color
from novaideo.content.processes import FLATTENED_STATES_MEMBER_MAPPING
from novaideo import core, _
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.views.filter import get_contents_by_keywords


class ContentsByKeywords(BasicView):
    title = _('Contents by keywords')
    name = 'idea_by_keywords'
    # validators = [Search.get_validator()]
    template = 'novaideo:views/novaideo_view_manager/templates/idea_by_keywords.pt'
    viewid = 'idea_by_keywords'

    def update(self):
        result = {}
        body = self.content(args={}, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


@colander.deferred
def states_choices(node, kw):
    values = [(k, FLATTENED_STATES_MEMBER_MAPPING[k])
              for k in sorted(FLATTENED_STATES_MEMBER_MAPPING.keys())]

    return Select2Widget(values=values, multiple=True)


@colander.deferred
def content_types_choices(node, kw):
    content_to_examine = ['idea', 'proposal']
    values = [(key, getattr(c, 'type_title', c.__class__.__name__))
              for key, c in list(core.SEARCHABLE_CONTENTS.items())
              if key in content_to_examine]
    return Select2Widget(values=values, multiple=True)


class ContentsByKeywordsSchema(Schema):

    content_types = colander.SchemaNode(
        colander.Set(),
        widget=content_types_choices,
        title=_('Types'),
        description=_('You can select the content types to be displayed.'),
        missing=[]
    )

    states = colander.SchemaNode(
        colander.Set(),
        widget=states_choices,
        title=_('States'),
        description=_('You can select the states of the contents to be displayed.'),
        default=[],
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
    formid = 'idea_by_keywords_form'
    name = 'idea_by_keywords_form'

    def before_update(self):
        formwidget = deform.widget.FormWidget(css_class='idea-by-keywords')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        formwidget.ajax_url = self.request.resource_url(
            self.context, '@@analyticsapi', query={'op': 'contents_by_keywords'})
        self.schema.widget = formwidget


class ContentsByKeywordsView(MultipleView):
    title = _('Contents by keywords')
    name = 'idea_by_keywords_view'
    template = 'novaideo:views/templates/simple_mergedmultipleview.pt'
    views = (ContentsByKeywordsForm, ContentsByKeywords)


@view_config(
    name='analytics',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AnalyticsView(MultipleView):
    title = _('Analytics')
    name = 'analytics'
    template = 'novaideo:views/templates/simple_mergedmultipleview.pt'
    views = (ContentsByKeywordsView, )
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/chartjs/Chart.js',
                                 'novaideo:static/js/analytics.js']}


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
        return root.keywords_mapping.get(key)

    def contents_by_keywords(self):
        states = self.params('states')
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

        for type_ in types:
            title = getattr(
                core.SEARCHABLE_CONTENTS.get(type_), 'type_title', type_)
            results[title] = {
                'data': get_contents_by_keywords(
                    [type_], states, user, root),
                'color': self.color_mapping.get(type_)
                }

        values = {'analytics': results,
                  'labels': self.request.root.keywords,
                  'view': self}
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
