import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.widget import TableWidget, LineWidget
from pontus.schema import Schema, omit, select

from sdkuneagi.content.processes.organization_management.behaviors import  CreatOrganizations
from sdkuneagi.content.novaideo_application import NovaIdeoApplication
from sdkuneagi.content.organization import OrganizationSchema, Organization


class CreatOrganizationsSchema(Schema):

    organizations = colander.SchemaNode(
                colander.Sequence(),
                select(omit(OrganizationSchema(factory=Organization, editable=True, name='Organization'),['_csrf_token_']), ['title', 'description', 'logo', 'members']),
                title='Organizations to creat'
                )


@view_config(
    name='creatorganizations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class CreatOrganizationsView(FormView):

    title = 'Creat organizations'
    schema = CreatOrganizationsSchema()
    behaviors = [CreatOrganizations]
    formid = 'formcreatorganizations'
    name='creatorganizations'

DEFAULTMAPPING_ACTIONS_VIEWS.update({CreatOrganizations:CreatOrganizationsView})
