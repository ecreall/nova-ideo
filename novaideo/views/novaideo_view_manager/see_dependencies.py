# -*- coding: utf8 -*-
# Copyright (c) 2016 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import Batch

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView

from novaideo.core import can_access
from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeDependencies)
from novaideo.utilities.util import (
    render_small_listing_objs)
from novaideo.core import Node
from novaideo import _


BATCH_DEFAULT_SIZE = 20

WG_MESSAGES = {
    '0': _(u"""No association"""),
    '1': _(u"""One association"""),
    '*': _(u"""${nember} associations""")}


@view_config(
    name='seedependencies',
    context=Node,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeDependenciesView(BasicView):
    name = 'seedependencies'
    viewid = 'seedependencies'
    behaviors = [SeeDependencies]
    template = 'novaideo:views/novaideo_view_manager/templates/home.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    view_icon = 'icon ion-android-share'
    title = _('The associations')
    description = _('See the associations')

    def update(self):
        self.execute(None)
        user = get_current()
        objects = [obj for obj
                   in self.context.get_sub_nodes()
                   if can_access(user, obj)]
        objects = sorted(
            objects,
            key=lambda e: getattr(e, 'modified_at'),
            reverse=True)
        url = self.request.resource_url(self.context, self.name)
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_node_dependencies_" + str(self.context.__oid__)
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(WG_MESSAGES[index], mapping={'nember': len_result})
        result = {}
        result_body = render_small_listing_objs(
            self.request, batch, user)

        values = {
            'bodies': result_body,
            'batch': batch,
            'empty_message': _("No association"),
            'empty_icon': 'glyphicon glyphicon-link'
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeDependencies: SeeDependenciesView})
