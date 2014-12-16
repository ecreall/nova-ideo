# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select

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
    schema = select(NovaIdeoApplicationSchema(editable=True), 
                    [(u'organizations', ['title',
                                         'description',
                                        'email',
                                        'phone',
                                        'fax',
                                        'logo',
                                        'members'])])
    behaviors = [EditOrganizations]
    formid = 'formeditorganizations'
    name = 'editorganizations'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update({EditOrganizations:EditOrganizationsView})