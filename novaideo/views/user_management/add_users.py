import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import Schema, select, omit
from pontus.widget import FileWidget
from pontus.file import ObjectData, File

from novaideo.content.processes.user_management.behaviors import AddUsers
from novaideo.content.novaideo_application import NovaIdeoApplication



class AddUsersSchema(Schema):

    file = colander.SchemaNode(
            ObjectData(File),
            widget=FileWidget()
            )


@view_config(
    name='add_users',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class AddUsersView(FormView):

    title = 'Add users'
    schema = AddUsersSchema(editable=True)
    behaviors = [AddUsers]
    formid = 'formaddusers'
    name='add_users'




DEFAULTMAPPING_ACTIONS_VIEWS.update({AddUsers:AddUsersView})
