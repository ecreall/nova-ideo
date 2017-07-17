# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
import deform
import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import find_catalog
from pontus.form import FormView
from pontus.view import BasicView
from pontus.view_operation import MultipleView
from pontus.default_behavior import Cancel
from pontus.schema import Schema
from pontus.widget import AjaxSelect2Widget

from novaideo.content.interface import Iidea
from novaideo.connectors.yammer.content.behaviors import Import
from novaideo.connectors.yammer import YammerConnector
from novaideo import _


class ImportViewStudyReport(BasicView):
    title = _('Alert for deletion')
    name = 'alertfordeletion'
    template = 'novaideo:connectors/yammer/views/templates/alert_import.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


@colander.deferred
def messages_choice(node, kw):
    request = node.bindings['request']
    root = request.root
    values = []
    ajax_url = request.resource_url(root, '@@novaideoapi',
                                    query={'op': 'find_yammer_messages'})
    return AjaxSelect2Widget(
        values=values,
        ajax_url=ajax_url,
        multiple=True,
        css_class="search-idea-form")


@colander.deferred
def default_messages(node, kw):
    novaideo_catalog = find_catalog('novaideo')
    dace_catalog = find_catalog('dace')
    identifier_index = novaideo_catalog['identifier']
    object_provides_index = dace_catalog['object_provides']
    query = object_provides_index.any([Iidea.__identifier__]) &\
        identifier_index.any(['yammer'])
    ideas = list(query.execute().all())
    return [str(i.source_data['id']) for i in ideas]


class MessagesSchema(Schema):

    messages = colander.SchemaNode(
        colander.Set(),
        widget=messages_choice,
        default=default_messages,
        title=_('Messages to import'),
        description=_('Select the messages to import from your Yammer networks'),
        missing=None,
        )


class ImportForm(FormView):
    title = _('Import messages from Yammer')
    name = 'delyammerconnectorform'
    schema = MessagesSchema()
    behaviors = [Import, Cancel]
    viewid = 'importyammerconnectorform'
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Import.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='importyammerconnector',
    context=YammerConnector,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ImportYammerConnectorView(MultipleView):
    title = _('Import messages from Yammer')
    name = 'importyammerconnector'
    behaviors = [Import]
    viewid = 'importyammerconnector'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (ImportViewStudyReport, ImportForm)
    validators = [Import.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Import: ImportYammerConnectorView})
