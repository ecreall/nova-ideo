import colander
import deform.widget
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import SharedUniqueProperty, CompositeMultipleProperty
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import RichTextWidget, LineWidget, TableWidget
from pontus.schema import omit

from .interface import Iidea
from .keyword import KeywordSchema, Keyword
from .commentabl import Commentabl
from novaideo import _



def context_is_a_idea(context, request):
    return request.registry.content.istype(context, 'idea')


class IdeaSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_idea,
        )

    description = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        widget=deform.widget.TextAreaWidget(rows=10, cols=30)
        )

    text = colander.SchemaNode(
        colander.String(),
        widget= RichTextWidget(),
        title=_('Content'),
        missing=''
        )

    keywords = colander.SchemaNode(
        colander.Sequence(),
        omit(KeywordSchema(widget=LineWidget(),
                           factory=Keyword,
                           editable=True,
                           name='Keyword'),['_csrf_token_']),
        widget=TableWidget(min_len=1),
        title='Keywords'
        )


@content(
    'idea',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(Iidea)
class Idea(Commentabl):
    name = renamer()
    author = SharedUniqueProperty('author', 'ideas')
    keywords = CompositeMultipleProperty('keywords')

    def __init__(self, **kwargs):
        super(Idea, self).__init__(**kwargs)

