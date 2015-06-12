# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.work_mode_processes.amendment_work_mode_process.behaviors import Alert
from novaideo.content.proposal import Proposal
from novaideo import _


@view_config(
    name='alert',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AlertView(BasicView):
    title = _('Alert')
    name = 'alert'
    behaviors = [Alert]
    viewid = 'alert'

    def update(self):
        results = self.execute(None)
        return results[0]

DEFAULTMAPPING_ACTIONS_VIEWS.update({Alert: AlertView})
