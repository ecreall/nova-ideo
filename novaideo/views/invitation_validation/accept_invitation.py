import colander
import deform.widget
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import Schema, select, omit
from pontus.widget import FileWidget
from pontus.file import ObjectData, File

from novaideo.content.processes.invitation_validation.behaviors import AcceptInvitation
from novaideo.content.invitation import Invitation



class AcceptInvitationSchema(Schema):

    password = colander.SchemaNode(
        colander.String(),
        widget = deform.widget.CheckedPasswordWidget(),
        validator=colander.Length(min=3, max=100),
        )


@view_config(
    name='accept_invitation',
    context=Invitation,
    renderer='pontus:templates/view.pt',
    )
class AcceptInvitationView(FormView):

    title = 'Accept invitation users'
    schema = AcceptInvitationSchema()
    behaviors = [AcceptInvitation]
    formid = 'formacceptinvitation'
    name='accept_invitation'


DEFAULTMAPPING_ACTIONS_VIEWS.update({AcceptInvitation:AcceptInvitationView})
