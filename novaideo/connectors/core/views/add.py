# -*- coding: utf8 -*-
# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.connectors.core.content.behaviors import (
    AddConnectors)
from novaideo.connectors.core import CONNECTOR_PROCESSES
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.utilities.util import generate_navbars, ObjectRemovedException


@view_config(
    name='addconnectors',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AddConnectorsView(BasicView):
    title = _('Add new connectors')
    name = 'addconnectors'
    behaviors = [AddConnectors]
    template = 'novaideo:connectors/core/views/templates/add_connectors.pt'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    viewid = 'addconnectors'
    css_class = 'panel-transparent'

    def update(self):
        self.execute(None)
        try:
            navbars = generate_navbars(
                self.request, self.context,
                process_id=CONNECTOR_PROCESSES,
                node_id='create',
                descriminators=['body-action'])
        except ObjectRemovedException:
            return HTTPFound(
                self.request.resource_url(
                    self.context, '@@seeconnectors'))

        result = {}
        values = {
            'bodies': navbars['body_actions']
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = navbars['messages']
        item['isactive'] = navbars['isactive']
        result.update(navbars['resources'])
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {AddConnectors: AddConnectorsView})
