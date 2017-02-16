# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select
from pontus.default_behavior import Cancel

from novaideo.content.processes.organization_management.behaviors import (
    AddMembers)
from novaideo.content.organization import OrganizationSchema, Organization
from novaideo import _


class AddMembersSchema(OrganizationSchema):

    are_managers = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Are managers'),
        title='',
        missing=False
    )


@view_config(
    name='addmembers',
    context=Organization,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AddMembersView(FormView):

    title = _('Add Members')
    schema = select(AddMembersSchema(),
                    ['members',
                     'are_managers'])
    behaviors = [AddMembers, Cancel]
    formid = 'formaddmembers'
    name = 'addmembers'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': AddMembers.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


DEFAULTMAPPING_ACTIONS_VIEWS.update({AddMembers: AddMembersView})
