# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
import deform
import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.user_management.behaviors import (
    ConfirmRegistration)
from novaideo.content.person import Preregistration
from novaideo import _



@view_config(
    route_name='registrations',
    name='',
    context=Preregistration,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ConfirmRegistrationView(BasicView):
    title = _('Registration confirmation')
    name = 'confirmation'
    behaviors = [ConfirmRegistration]
    viewid = 'confirmationview'

    def update(self):
        results = self.execute(None)
        return results[0]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {ConfirmRegistration: ConfirmRegistrationView})
