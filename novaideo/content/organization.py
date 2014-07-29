import colander
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer, find_service

from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import Select2Widget, FileWidget
from pontus.file import Image, ObjectData
from dace.objectofcollaboration.entity import Entity
from dace.descriptors import SharedMultipleProperty, CompositeUniqueProperty
from dace.util import getSite

from .interface import IOrganization


@colander.deferred
def default_members(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = []
    if hasattr(context, 'members'):
        values = context.members

    return values


@colander.deferred
def members_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = []
    root = getSite(context)
    if root is None:
        root = context.__parent__.__parent__

    principals = find_service(root, 'principals')
    prop = principals['users'].values()
    values = [(i, i.name) for i in prop if getattr(i, 'organization', None) in (None, context)]
    return Select2Widget(values=values, multiple=True)


def context_is_a_organization(context, request):
    return request.registry.content.istype(context, 'organization')


class OrganizationSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_organization,
        )
    
    logo = colander.SchemaNode(
            ObjectData(Image),
            widget= FileWidget(),
            required = False
            )

    email = colander.SchemaNode(
                colander.String(),
                validator=colander.All(
                    colander.Email(),
                    colander.Length(max=100)
                    ),
                )

    phone = colander.SchemaNode(
                     colander.String(),
                     title="Phone number")

    fax = colander.SchemaNode(
                     colander.String())

    members = colander.SchemaNode(
        colander.Set(),
        widget=members_choice,
        default=default_members,
        title='Members'
        )


@content(
    'organization',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IOrganization)
class Organization(VisualisableElement, Entity):
    name = renamer()
    members = SharedMultipleProperty('members', 'organization')
    logo = CompositeUniqueProperty('logo')

    def __init__(self, **kwargs):
        super(Organization, self).__init__(**kwargs)
        if 'phone' in kwargs:
            self.phone = kwargs.get('phone')

        if 'fax' in kwargs:
            self.fax = kwargs.get('fax')

        if 'email' in kwargs:
            self.email = kwargs.get('email')

    def setmembers(self, members):
        self.setproperty('members', members)

    def setlogo(self, logo):
        self.setproperty('logo', logo)

