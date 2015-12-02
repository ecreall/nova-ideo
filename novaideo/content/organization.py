# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer, find_service

from dace.objectofcollaboration.principal.util import get_users_with_role

from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import Select2Widget, FileWidget
from pontus.file import Image, ObjectData
from dace.objectofcollaboration.entity import Entity
from dace.descriptors import SharedMultipleProperty, CompositeUniqueProperty
from dace.util import getSite

from .interface import IOrganization
from novaideo import _



@colander.deferred
def members_choice(node, kw):
    context = node.bindings['context']
    values = []
    root = getSite(context)
    if root is None:
        root = context.__parent__.__parent__

    principals = find_service(root, 'principals')
    prop = list(principals['users'].values())
    values = [(i, i.name) for i in prop ]
    return Select2Widget(values=values, multiple=True)


def context_is_a_organization(context, request):
    return request.registry.content.istype(context, 'organization')


class OrganizationSchema(VisualisableElementSchema):
    """Schema for Organization"""

    name = NameSchemaNode(
        editing=context_is_a_organization,
        )

    logo = colander.SchemaNode(
        ObjectData(Image),
        widget=FileWidget(),
        required=False,
        missing=None,
        title=_('Logo'),
        )

    email = colander.SchemaNode(
        colander.String(),
        validator=colander.All(
            colander.Email(),
            colander.Length(max=100)
            ),
        missing='',
        title=_('Email'),
        )

    phone = colander.SchemaNode(
         colander.String(),
         title=_("Phone number"),
         missing=''
         )

    fax = colander.SchemaNode(
         colander.String(),
         title=_("Fax"),
         missing=''
         )

    members = colander.SchemaNode(
        colander.Set(),
        widget=members_choice,
        title=_('Members'),
        )

    managers = colander.SchemaNode(
        colander.Set(),
        widget=members_choice,
        title=_('Managers'),
        )


@content(
    'organization',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IOrganization)
class Organization(VisualisableElement, Entity):
    """Organization class"""

    templates = {
        'default': 'novaideo:views/templates/organization_result.pt'
    }
    name = renamer()
    members = SharedMultipleProperty('members', 'organization')
    logo = CompositeUniqueProperty('logo')

    def __init__(self, **kwargs):
        super(Organization, self).__init__(**kwargs)
        self.set_data(kwargs)

    @property
    def managers(self):
        return get_users_with_role(role=('OrganizationResponsible', self))