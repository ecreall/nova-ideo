# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.util import get_obj
from dace.objectofcollaboration.principal.util import get_current
from dace.objectofcollaboration.entity import Entity
from dace.processinstance.core import (
    DEFAULTMAPPING_ACTIONS_VIEWS, PROCESS_HISTORY_KEY)

from pontus.view import BasicView

from novaideo.content.processes import get_states_mapping
from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeEntityHistory)
from novaideo import _


@view_config(
    name='seeentityhistory',
    context=Entity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeEntityHistoryView(BasicView):
    title = _('Processes history')
    name = 'seeentityhistory'
    behaviors = [SeeEntityHistory]
    template = 'novaideo:views/novaideo_view_manager/templates/entity_history.pt'
    viewid = 'seeentityhistory'

    def update(self):
        self.execute(None)
        result = {}
        history = getattr(self.context, 'annotations', {}).get(
            PROCESS_HISTORY_KEY, [])
        values = {'context': self.context,
                  'history': history,
                  'current_user': get_current(),
                  'get_states_mapping': get_states_mapping,
                  'get_obj': get_obj}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeEntityHistory: SeeEntityHistoryView})
