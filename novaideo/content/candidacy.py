# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.objectofcollaboration.entity import Entity
from pontus.widget import RichTextWidget
from pontus.core import VisualisableElement, VisualisableElementSchema

from .interface import ICandidacy
from novaideo import _


def context_is_a_candidacy(context, request):
    return request.registry.content.istype(context, 'candidacy')


class CandidacySchema(VisualisableElementSchema):
    """Schema for Candidacy"""

    name = NameSchemaNode(
        editing=context_is_a_candidacy,
        )

    body = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget(),
        title=_('Application'),
        )


@content(
    'candidacy',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(ICandidacy)
class Candidacy(VisualisableElement, Entity):
    """Candidacy class"""
    name = renamer()
