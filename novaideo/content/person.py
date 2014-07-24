import colander
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer
from substanced.principal import UserSchema

from dace.util import getSite
from dace.objectofcollaboration.entity import Entity
from dace.objectofcollaboration.object import (
                SHARED_UNIQUE,
                COMPOSITE_MULTIPLE,
                COMPOSITE_UNIQUE)
from dace.objectofcollaboration.principal import User
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import RadioChoiceWidget, FileWidget
from pontus.file import Image, ObjectData, Object as ObjectType
from .interface import IPerson


@colander.deferred
def organization_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = []
    root = getSite(context)
    if root is None:
        root = context.__parent__.__parent__

    prop = root.organizations
    values = [(i, i.get_view(request)) for i in prop]
    return RadioChoiceWidget(values=values)


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

    organization = colander.SchemaNode(
                ObjectType(),
                widget=organization_choice,
                requierd=False
                )


@content(
    'person',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IPerson)
class Person(VisualisableElement, User):
    name = renamer()
    properties_def = {'tokens':(COMPOSITE_MULTIPLE, 'owner', True),
                      'organization':(SHARED_UNIQUE, 'members', False),
                      'picture':(COMPOSITE_UNIQUE, None, False)}

    def __init__(self, **kwargs):
        super(Person, self).__init__(**kwargs)

    @property
    def tokens(self):
        return self.getproperty('tokens')

    def settokens(self, tokens):
        self.setproperty('tokens', tokens)

    @property
    def organization(self):
        return self.getproperty('organization')

    def setorganization(self, organization):
        self.setproperty('organization', organization)

