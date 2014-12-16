# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.invitation_management.behaviors import (
    RemindInvitation)
from novaideo.content.invitation import Invitation
from novaideo import _


@view_config(
    name='remind_invitation',
    context=Invitation,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class RemindInvitationView(BasicView):

    title = _('Remind invitation')
    behaviors = [RemindInvitation]
    name = 'remind_invitation'

    def update(self):
        self.execute(None)
        return {}


DEFAULTMAPPING_ACTIONS_VIEWS.update({RemindInvitation:RemindInvitationView})