# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
import json
from pyramid.view import view_config

from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import (
    DEFAULTMAPPING_ACTIONS_VIEWS)
from dace.util import get_obj

from pontus.view import BasicView

from novaideo.core import Node
from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeGraph)
from novaideo import _
from novaideo.core import can_access


@view_config(
    name='seegraph',
    context=Node,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeGraphView(BasicView):
    title = _('Graph of dependences')
    name = 'seegraph'
    behaviors = [SeeGraph]
    template = 'novaideo:views/novaideo_view_manager/templates/graph_entities.pt'
    viewid = 'seegraph'
    # requirements = {'css_links': [],
    #                 'js_links': ['novaideo:static/jsnetworkx/d3.min.js',
    #                              'novaideo:static/jsnetworkx/jsnetworkx.js']}

    def update(self):
        result = {}
        user = get_current()
        values = {'nodes': self.context.graph,
                  'node_id': self.context.get_node_id(),
                  'get_obj': get_obj,
                  'can_access': can_access,
                  'user': user,
                  'json': json}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        self.execute(None)
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeGraph: SeeGraphView})
