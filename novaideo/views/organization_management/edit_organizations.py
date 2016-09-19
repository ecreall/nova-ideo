# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import get_oid

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select
from pontus.default_behavior import Cancel
from pontus.file import OBJECT_OID

from novaideo.content.processes.organization_management.behaviors import (
    EditOrganizations)
from novaideo.content.novaideo_application import (
    NovaIdeoApplicationSchema,
    NovaIdeoApplication)
from novaideo import _


@view_config(
    name='editorganizations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditOrganizationsView(FormView):

    title = _('Edit organizations')
    schema = select(NovaIdeoApplicationSchema(),
                    [(u'organizations', ['title',
                                         'description',
                                         'logo',
                                         'managers',
                                         'contacts'])])
    behaviors = [EditOrganizations, Cancel]
    formid = 'formeditorganizations'
    name = 'editorganizations'

    def default_data(self):
        result = {}
        organizations = []
        for organization in self.context.organizations:
            organization_data = organization.get_data(
                self.schema.get('organizations').children[0])
            organization_data[OBJECT_OID] = str(get_oid(organization))
            if organization_data['logo']:
                logo = organization_data['logo']
                organization_data['logo'] = logo.get_data(None)

            organizations.append(organization_data)

        result['organizations'] = organizations
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {EditOrganizations: EditOrganizationsView})
