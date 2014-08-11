import colander
import deform
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.descriptors import SharedUniqueProperty
from dace .util import find_entities
from pontus.core import VisualisableElementSchema
from pontus.widget import Select2Widget
from pontus.file import Object as ObjectType

from .interface import ICorrelation, ICorrelableEntity
from novaideo.core import Commentabl
from novaideo import _


@colander.deferred
def targets_choice(node, kw):
    values = []
    entities = find_entities([ICorrelableEntity])
    values = [(i, i.title) for i in entities]
    values = sorted(values, key=lambda p: p[1])
    return Select2Widget(values=values, multiple=True)


def context_is_a_correlation(context, request):
    return request.registry.content.istype(context, 'correlation')


class CorrelationSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_correlation,
        )

    comment = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        )

    targets = colander.SchemaNode(
        ObjectType(),
        widget=targets_choice,
        title=_('Targets'),
        )


@content(
    'correlation',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(ICorrelation)
class Correlation(Commentabl):
    name = renamer()
    source = SharedUniqueProperty('source', 'source_correlations')
    target = SharedUniqueProperty('target', 'target_correlations')

    @property
    def ends(self):
        return (self.source, self.target)
