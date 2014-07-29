import colander
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer
from substanced.principal import UserSchema

from dace.util import getSite
from dace.objectofcollaboration.principal import User
from dace.descriptors import (
    SharedUniqueProperty,
    CompositeMultipleProperty,
    CompositeUniqueProperty)
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import FileWidget, Select2Widget
from pontus.file import Image, ObjectData, Object as ObjectType

from .interface import IPerson
from novaideo import _

@colander.deferred
def organization_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = []
    root = getSite()
    if root is None:
        root = context.__parent__.__parent__

    prop = sorted(root.organizations, key=lambda p: p.title)
    values = [(i, i.title) for i in prop]
    return Select2Widget(values=values)


@colander.deferred
def titles_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite()
    values = [(i, i) for i in root.titles]
    return Select2Widget(values=values)


def context_is_a_person(context, request):
    return request.registry.content.istype(context, 'person')


class PersonSchema(VisualisableElementSchema, UserSchema):

    name = NameSchemaNode(
        editing=context_is_a_person,
        )

    picture = colander.SchemaNode(
            ObjectData(Image),
            widget= FileWidget(),
            required = False
            )

    first_name =  colander.SchemaNode(
                    colander.String(),
                    title=_('First name') 
                    )

    last_name = colander.SchemaNode(
                    colander.String(),
                    title=_('Last name')
                    )
  
    user_title = colander.SchemaNode(
                    colander.String(),
                    widget=titles_choice,
                    title=_('Title')
                )

    organization = colander.SchemaNode(
                ObjectType(),
                widget=organization_choice,
                missing=None,
                title=_('Organization')
                )


@content(
    'person',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IPerson)
class Person(VisualisableElement, User):
    name = renamer()
    tokens = CompositeMultipleProperty('tokens', 'owner')
    organization = SharedUniqueProperty('organization', 'members')
    picture = CompositeUniqueProperty('picture')

    def __init__(self, **kwargs):
        super(Person, self).__init__(**kwargs)

    def settokens(self, tokens):
        self.setproperty('tokens', tokens)

    def setorganization(self, organization):
        self.setproperty('organization', organization)

