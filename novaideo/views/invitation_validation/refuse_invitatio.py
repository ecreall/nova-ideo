import colander
import deform.widget
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView
from pontus.schema import Schema, select, omit
from pontus.widget import FileWidget
from pontus.file import ObjectData, File

from novaideo.content.processes.invitation_validation.behaviors import RefuseInvitation
from novaideo.content.invitation import Invitation


@view_config(
    name='refuse_invitation',
    context=Invitation,
    renderer='pontus:templates/view.pt',
    )
class RefuseInvitationView(BasicView):

    title = 'Refuse invitation'
    behaviors = [RefuseInvitation]
    name='refuse_invitation'

    def update(self):
        self.execute(None)
        return {}


DEFAULTMAPPING_ACTIONS_VIEWS.update({RefuseInvitation:RefuseInvitationView})
