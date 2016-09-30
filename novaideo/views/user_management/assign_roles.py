# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
import colander
from pyramid.view import view_config

from dace.objectofcollaboration.principal.role import DACE_ROLES
from dace.objectofcollaboration.principal.util import get_roles, has_role
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.widget import Select2Widget
from pontus.schema import Schema

from novaideo.content.processes.user_management.behaviors import (
    AssignRoles)
from novaideo.content.person import Person
from novaideo import _
from novaideo.role import get_authorized_roles
from novaideo.content.invitation import roles_validator


@colander.deferred
def roles_choice(node, kw):
    roles = get_authorized_roles()
    values = [(key, name) for (key, name) in roles.items()
              if not DACE_ROLES[key].islocal]
    values = sorted(values, key=lambda e: e[0])
    return Select2Widget(values=values, multiple=True)


class RolesSchema(Schema):

    roles = colander.SchemaNode(
        colander.Set(),
        validator=colander.All(
            roles_validator
            ),
        widget=roles_choice,
        title=_('Roles'),
        missing='Member'
    )


@view_config(
    name='assignroles',
    context=Person,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AssignRolesView(FormView):

    title = _('Assign roles')
    schema = RolesSchema()
    behaviors = [AssignRoles, Cancel]
    formid = 'formassignroles'
    name = 'assignroles'

    def default_data(self):
        roles = [r for r in get_roles(self.context)
                 if not getattr(DACE_ROLES.get(r, None), 'islocal', False)]
        return {'roles': roles}

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': AssignRoles.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {AssignRoles: AssignRolesView})
