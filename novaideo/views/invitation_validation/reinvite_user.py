import colander
import deform.widget
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView
from pontus.schema import Schema, select, omit
from pontus.widget import FileWidget
from pontus.file import ObjectData, File

from novaideo.content.processes.invitation_validation.behaviors import ReinviteUser
from novaideo.content.invitation import Invitation


@view_config(
    name='reinvite_user',
    context=Invitation,
    renderer='pontus:templates/view.pt',
    )
class ReinviteUserView(BasicView):

    title = 'Reinvite user'
    behaviors = [ReinviteUser]
    name='reinvite_user'

    def update(self):
        self.execute(None)
        return {}


DEFAULTMAPPING_ACTIONS_VIEWS.update({ReinviteUser:ReinviteUserView})
