
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.objectofcollaboration.entity import Entity
from pontus.core import VisualisableElement, VisualisableElementSchema

from .interface import IKeyword


def context_is_a_keyword(context, request):
    return request.registry.content.istype(context, 'keyword')


class KeywordSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_keyword,
        )


@content(
    'keyword',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IKeyword)
class Keyword(VisualisableElement, Entity):
    name = renamer()

    def __init__(self, **kwargs):
        super(Keyword, self).__init__(**kwargs)

