# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.novaideo_process_management.behaviors import  (
    Update)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


@view_config(
    name='updateprocesses',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class UpdateView(BasicView):
    title = _('Update processes')
    name = 'updateprocesses'
    behaviors = [Update]
    viewid = 'updateprocesses'

    def update(self):
        results = self.execute(None)
        return results[0]


DEFAULTMAPPING_ACTIONS_VIEWS.update({Update:UpdateView})
