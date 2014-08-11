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

    name = NameSchemaNode(
        editing=context_is_a_candidacy,
        )

    body = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget(),
        title=_('Candidacy'),
        )


@content(
    'candidacy',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(ICandidacy)
class Candidacy(VisualisableElement, Entity):
    name = renamer()
