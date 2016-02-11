# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from zope.interface import implementer

from substanced.content import content
from substanced.util import renamer

from dace.objectofcollaboration.principal.util import has_role
from dace.objectofcollaboration.entity import Entity
from dace.objectofcollaboration.principal.role import DACE_ROLES
from dace.descriptors import SharedUniqueProperty
from pontus.widget import Select2Widget
from pontus.core import VisualisableElement

from .interface import IInvitation
from .person import PersonSchema
from novaideo import _
from novaideo.role import DEFAULT_ROLES, APPLICATION_ROLES


@colander.deferred
def roles_choice(node, kw):
    roles = APPLICATION_ROLES.copy()
    if not has_role(role=('Admin', )) and 'Admin' in roles:
        roles.pop('Admin')

    values = [(key, name) for (key, name) in roles.items()
              if not DACE_ROLES[key].islocal]
    values = sorted(values, key=lambda e: e[0])
    return Select2Widget(values=values, multiple=True)


def context_is_a_invitation(context, request):
    return request.registry.content.istype(context, 'invitation')


class InvitationSchema(PersonSchema):
    """Schema for invitation"""

    roles = colander.SchemaNode(
        colander.Set(),
        widget=roles_choice,
        title=_('Roles'),
        missing=DEFAULT_ROLES,
        default=DEFAULT_ROLES,
        )

    ismanager = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Is the manager'),
        title='',
        missing=False
    )


@content(
    'invitation',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IInvitation)
class Invitation(VisualisableElement, Entity):
    """Invitation class"""
    templates = {'default': 'novaideo:views/templates/invitation_result.pt',
                 'bloc': 'novaideo:views/templates/invitation_result.pt'}
    name = renamer()
    organization = SharedUniqueProperty('organization')
    manager = SharedUniqueProperty('manager')

    def __init__(self, **kwargs):
        super(Invitation, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.title = 'Invitation' + \
                     self.first_name + ' ' + \
                     self.last_name
