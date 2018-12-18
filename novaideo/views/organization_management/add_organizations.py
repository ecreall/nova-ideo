# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view import BasicView
from pontus.view_operation import MultipleView
from pontus.default_behavior import Cancel
from pontus.schema import Schema
from pontus.widget import FileWidget
from pontus.file import ObjectData, File

from novaideo.content.processes.organization_management.behaviors import (
    AddOrganizations)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


class AddOrganizationsStudyReport(BasicView):
    title = _('Alert for organization import')
    name = 'alertfororganizationimport'
    template = 'novaideo:views/organization_management/templates/alert_import.pt'

    def update(self):
        result = {}
        values = {}
        body = self.content(args={}, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class AddOrganizationsSchema(Schema):

    file = colander.SchemaNode(
        ObjectData(File),
        widget=FileWidget(),
        title=_('The xls file'),
        description=_("The xls file containing organizations data.")
    )


class AddOrganizationsForm(FormView):

    title = _('Upload organizations')
    schema = AddOrganizationsSchema(editable=True)
    behaviors = [AddOrganizations, Cancel]
    formid = 'formaddorganizationform'
    name = 'add_organizationsform'
    css_class = 'panel-transparent'


@view_config(
    name='add_organizations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    layout='old'
    )
class AddOrganizationsView(MultipleView):
    title = _('Upload organizations')
    name = 'add_organizations'
    behaviors = [AddOrganizations]
    viewid = 'add_organizations'
    template = 'daceui:templates/mergedmultipleview.pt'
    css_class = 'panel-transparent'
    views = (AddOrganizationsStudyReport, AddOrganizationsForm)
    validators = [AddOrganizations.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {AddOrganizations: AddOrganizationsView})