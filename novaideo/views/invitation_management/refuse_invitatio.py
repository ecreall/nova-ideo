# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.invitation_management.behaviors import (
    RefuseInvitation)
from novaideo.content.invitation import Invitation
from novaideo import _


@view_config(
    name='refuse_invitation',
    context=Invitation,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class RefuseInvitationView(BasicView):

    title = _('Refuse the invitation')
    behaviors = [RefuseInvitation]
    name = 'refuse_invitation'

    def update(self):
        self.execute(None)
        return {}


DEFAULTMAPPING_ACTIONS_VIEWS.update({RefuseInvitation:RefuseInvitationView})
