import colander
import deform
import deform.widget
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer, find_service

from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.schema import Schema, omit, select
from pontus.widget import RichTextWidget, LineWidget, TableWidget, Select2Widget, FileWidget
from pontus.file import Image, ObjectData
from dace.objectofcollaboration.entity import Entity
from dace.objectofcollaboration.object import (
                COMPOSITE_UNIQUE,
                SHARED_UNIQUE,
                COMPOSITE_MULTIPLE,
                SHARED_MULTIPLE,
                Object)
from dace.util import getSite


from .interface import IOrganization
from .person import Person, PersonSchema


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
    properties_def = {'members':(SHARED_MULTIPLE, 'organization', False),
                      'logo':(COMPOSITE_UNIQUE, None, False)}

    def __init__(self, **kwargs):
        super(Organization, self).__init__(**kwargs)

    @property
    def members(self):
        return self.getproperty('members')

    def setmembers(self, members):
        self.setproperty('members', members)

    @property
    def logo(self):
        return self.getproperty('logo')

    def setlogo(self, logo):
        self.setproperty('logo', logo)

