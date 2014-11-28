# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import SharedMultipleProperty
from pontus.core import VisualisableElement, VisualisableElementSchema

from .interface import IKeyword


def context_is_a_keyword(context, request):
    return request.registry.content.istype(context, 'keyword')


class KeywordSchema(VisualisableElementSchema):
    """Schema for keyword"""

    name = NameSchemaNode(
        editing=context_is_a_keyword,
        )


@content(
    'keyword',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IKeyword)
class Keyword(VisualisableElement, Entity):
    """Keyword class"""
    
    name = renamer()
    referenced_elements = SharedMultipleProperty('referenced_elements',
                                                 'keywords')

    def __init__(self, **kwargs):
        super(Keyword, self).__init__(**kwargs)
        self.set_data(kwargs)
