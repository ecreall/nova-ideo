# -*- coding: utf8 -*-
# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
import colander
from pyramid.view import view_config
import yampy

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.form import FormView
from pontus.view import BasicView
from pontus.view_operation import MultipleView
from pontus.default_behavior import Cancel
from pontus.schema import Schema

from novaideo.content.interface import Iidea
from novaideo.connectors.yammer.content.behaviors import Import
from novaideo.connectors.yammer import YammerConnector
from novaideo.connectors.yammer.views import find_yammer_content
from novaideo.connectors.core import YAMMER_CONNECTOR_ID
from novaideo.widget import AjaxCheckBoxWidget
from novaideo import _, log
from novaideo.utilities.util import html_to_text


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
    yammer_connectors = list(root.get_connectors(YAMMER_CONNECTOR_ID))
    yammer_connector = yammer_connectors[0] if yammer_connectors else None
    access_token = yammer_connector.get_access_tokens(get_current()).get('access_token', None) \
        if yammer_connector else None
    values = []
    page = ''
    limit = 10
    ajax_url = None
    if yammer_connector and access_token:
        try:
            yammer = yampy.Yammer(access_token=access_token)
            messages = yammer.client.get('/messages', threaded=True, limit=limit)
            page = messages['messages'][-1]['id']
            values = [(str(e['id']), html_to_text(e['body']['plain'][:150])+'...')
                      for e in messages['messages']]
            if messages['meta']['older_available']:
                ajax_url = request.resource_url(
                    root, '@@yammerapi',
                    query={'op': 'find_yammer_messages'})
        except Exception as error:
            log.warning(error)

    return AjaxCheckBoxWidget(
        values=values,
        url=ajax_url,
        limit=limit,
        page=page,
        multiple=True,)


@colander.deferred
def default_messages(node, kw):
    return [i.source_data[YAMMER_CONNECTOR_ID]['id']
            for i in find_yammer_content([Iidea])]


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
