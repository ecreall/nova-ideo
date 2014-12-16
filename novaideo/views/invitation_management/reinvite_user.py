# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.invitation_management.behaviors import (
    ReinviteUser)
from novaideo.content.invitation import Invitation
from novaideo import _


@view_config(
    name='reinvite_user',
    context=Invitation,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ReinviteUserView(BasicView):

    title = _('Reinvite user')
    behaviors = [ReinviteUser]
    name = 'reinvite_user'

    def update(self):
        self.execute(None)
        return {}


DEFAULTMAPPING_ACTIONS_VIEWS.update({ReinviteUser:ReinviteUserView})