import colander
import deform
import deform.widget
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from pontus.schema import Schema
from pontus.widget import RichTextWidget
from dace.objectofcollaboration.entity import Entity
from dace.objectofcollaboration.object import (
                COMPOSITE_UNIQUE,
                SHARED_UNIQUE,
                COMPOSITE_MULTIPLE,
                SHARED_MULTIPLE,
                Object)

from pontus.core import VisualisableElement, VisualisableElementSchema

from .interface import IToken


def context_is_a_token(context, request):
    return request.registry.content.istype(context, 'token')


class TokenSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_token,
        )


@content(
    'token',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IToken)
class Token(VisualisableElement, Entity):
    name = renamer()
    properties_def = {'owner':(SHARED_UNIQUE, 'tokens', False)}

    def __init__(self, **kwargs):
        super(Token, self).__init__(**kwargs)

    @property
    def owner(self):
        return self.getproperty('owner')

    def setowner(self, owner):
        self.setproperty('owner', owner)

