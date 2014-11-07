
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.invitation_validation.behaviors import (
    RefuseInvitation)
from novaideo.content.invitation import Invitation
from novaideo import _


@view_config(
    name='refuse_invitation',
    context=Invitation,
    renderer='pontus:templates/view.pt',
    )
class RefuseInvitationView(BasicView):

    title = _('Refuse invitation')
    behaviors = [RefuseInvitation]
    name = 'refuse_invitation'

    def update(self):
        self.execute(None)
        return {}


DEFAULTMAPPING_ACTIONS_VIEWS.update({RefuseInvitation:RefuseInvitationView})
