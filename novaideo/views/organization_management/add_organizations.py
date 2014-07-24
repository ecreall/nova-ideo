import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import Schema, select, omit
from pontus.widget import FileWidget
from pontus.file import ObjectData, File

from sdkuneagi.content.processes.organization_management.behaviors import AddOrganizations
from sdkuneagi.content.novaideo_application import NovaIdeoApplication



class AddOrganizationsSchema(Schema):

    file = colander.SchemaNode(
            ObjectData(File),
            widget=FileWidget()
            )


@view_config(
    name='add_organizations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class AddOrganizationsView(FormView):

    title = 'Add organizations'
    schema = AddOrganizationsSchema(editable=True)
    behaviors = [AddOrganizations]
    formid = 'formaddorganization'
    name='add_organizations'


DEFAULTMAPPING_ACTIONS_VIEWS.update({AddOrganizations:AddOrganizationsView})
