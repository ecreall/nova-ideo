# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from pyramid.view import view_config

from dace.objectofcollaboration.principal.util import has_role
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.organization_management.behaviors import (
    UserEditOrganization)
from novaideo.content.person import PersonSchema, Person
from novaideo import _


class UserEditOrganizationSchema(PersonSchema):

    ismanager = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Is the manager'),
        title='',
        missing=False
    )


@view_config(
    name='usereditorganization',
    context=Person,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class UserEditOrganizationView(FormView):

    title = _('Edit the organization')
    schema = select(UserEditOrganizationSchema(),
                    ['organization',
                     'ismanager'])
    behaviors = [UserEditOrganization, Cancel]
    formid = 'formusereditorganization'
    name = 'usereditorganization'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': UserEditOrganization.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')

    def default_data(self):
        organization = self.context.organization
        if organization:
            return {
                'organization': organization,
                'ismanager': has_role(
                    ('OrganizationResponsible', organization), self.context,
                    ignore_superiors=True)
            }

        return {}


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {UserEditOrganization: UserEditOrganizationView})
