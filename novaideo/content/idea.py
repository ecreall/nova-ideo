import colander
import deform.widget
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import getSite
from dace.objectofcollaboration.entity import Entity
from dace.descriptors import SharedUniqueProperty, CompositeMultipleProperty, SharedMultipleProperty
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import RichTextWidget, LineWidget, TableWidget, Select2Widget
from pontus.schema import omit

from .interface import Iidea
from novaideo.core import Commentabl
from novaideo import _
from novaideo.core import (
    VersionableEntity,
    DuplicableEntity,
    SerchableEntity,
    SerchableEntitySchema,
    CorrelableEntity)


@colander.deferred
def intention_choice(node, kw):
    root = getSite()
    intentions = sorted(root.idea_intentions)
    values = [(i, i) for i in intentions ]
    return Select2Widget(values=values)


def context_is_a_idea(context, request):
    return request.registry.content.istype(context, 'idea')


class IdeaSchema(VisualisableElementSchema, SerchableEntitySchema):

    name = NameSchemaNode(
        editing=context_is_a_idea,
        )

    description = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        widget=deform.widget.TextAreaWidget(rows=10, cols=30),
        )

    text = colander.SchemaNode(
        colander.String(),
        widget= RichTextWidget(),
        title=_('Content'),
        missing='',
        )

    intention = colander.SchemaNode(
        colander.String(),
        widget=intention_choice,
        title=_('Intention'),
        default=_('Creation'),
        )


@content(
    'idea',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(Iidea)
class Idea(Commentabl, VersionableEntity, DuplicableEntity,
           SerchableEntity, CorrelableEntity):
    result_template = 'novaideo:views/templates/idea_result.pt'
    name = renamer()
    author = SharedUniqueProperty('author', 'ideas')

    def __init__(self, **kwargs):
        super(Idea, self).__init__(**kwargs)
        self.set_data(kwargs)
