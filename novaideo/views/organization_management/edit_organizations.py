from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.organization_management.behaviors import  EditOrganizations
from novaideo.content.novaideo_application import NovaIdeoApplicationSchema, NovaIdeoApplication



@view_config(
    name='editorganizations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class EditOrganizationsView(FormView):

    title = 'Edit organizations'
    schema = select(NovaIdeoApplicationSchema(editable=True),[(u'organizations',['title',
                                                                                 'description',
                                                                                 'logo'])])
    behaviors = [EditOrganizations]
    formid = 'formeditorganizations'
    name='editorganizations'

    def default_data(self):
        return self.context

DEFAULTMAPPING_ACTIONS_VIEWS.update({EditOrganizations:EditOrganizationsView})
