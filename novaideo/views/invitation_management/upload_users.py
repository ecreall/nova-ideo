
import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import Schema
from pontus.widget import FileWidget
from pontus.file import ObjectData, File

from novaideo.content.processes.invitation_management.behaviors import (
    UploadUsers)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


class UploadUsersSchema(Schema):

    file = colander.SchemaNode(
            ObjectData(File),
            widget=FileWidget()
            )


@view_config(
    name='upload_users',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class UploadUsersView(FormView):

    title = _('Upload users')
    schema = UploadUsersSchema(editable=True)
    behaviors = [UploadUsers]
    formid = 'formuploadusers'
    name = 'upload_users'


DEFAULTMAPPING_ACTIONS_VIEWS.update({UploadUsers:UploadUsersView})
