
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import SharedUniqueProperty
from pontus.core import VisualisableElement, VisualisableElementSchema

from .interface import IToken


@content(
    'token',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IToken)
class Token(VisualisableElement, Entity):
    """Token class""" 

    name = renamer()
    owner = SharedUniqueProperty('owner')
    proposal = SharedUniqueProperty('proposal')