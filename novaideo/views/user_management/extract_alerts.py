# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.user_management.behaviors import ExtractAlerts
from novaideo.content.person import Person
from novaideo import _


@view_config(
    name='extractalerts',
    context=Person,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ExtractalertsView(BasicView):
    title = _('Extract alerts')
    name = 'extractalerts'
    behaviors = [ExtractAlerts]
    viewid = 'extractalertsview'

    def update(self):
        results = self.execute(None)
        return results[0]


DEFAULTMAPPING_ACTIONS_VIEWS.update({ExtractAlerts: ExtractalertsView})
