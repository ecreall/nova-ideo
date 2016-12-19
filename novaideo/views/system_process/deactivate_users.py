# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.system_process.behaviors import (
    DeactivateUsers)
from novaideo.content.novaideo_application import (
    NovaIdeoApplication)
from novaideo import _


@view_config(
    name='deactivateusers',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DeactivateUsersView(BasicView):
    title = _('Disactivate')
    name = 'deactivateusers'
    behaviors = [DeactivateUsers]
    viewid = 'deactivateusers'

    def update(self):
        results = self.execute(None)
        return results[0]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {DeactivateUsers: DeactivateUsersView})
