# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

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
from novaideo.role import APPLICATION_ROLES


@colander.deferred
def roles_choice(node, kw):
    roles = APPLICATION_ROLES.copy()
    if not has_role(role=('Admin', )) and 'Admin' in roles:
        roles.pop('Admin')

    values = [(key, name) for (key, name) in roles.items()
              if not DACE_ROLES[key].islocal]
    values = sorted(values, key=lambda e: e[0])
    return Select2Widget(values=values, multiple=True)


class RolesSchema(Schema):

    roles = colander.SchemaNode(
        colander.Set(),
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


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {AssignRoles: AssignRolesView})
