import colander
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import getSite
from dace.objectofcollaboration.entity import Entity
from dace.descriptors import (
    CompositeMultipleProperty,
    SharedUniqueProperty,
    SharedMultipleProperty
)
from pontus.schema import omit
from pontus.widget import RichTextWidget
from pontus.core import VisualisableElement, VisualisableElementSchema

from .keyword import KeywordSchema, Keyword
from .interface import IProposal
from novaideo.core import Commentabl
from novaideo import _
from novaideo.core import (
    VersionableEntity,
    DuplicableEntity,
    SerchableEntity,
    SerchableEntitySchema)


@colander.deferred
def ideas_choice(node, kw):
    root = getSite()
    ideas = [i for i in root.ideas if 'published' in i.state]
    values = [(i, i) for i in ideas]
    return Select2Widget(values=values, multiple=True)


def context_is_a_proposal(context, request):
    return request.registry.content.istype(context, 'proposal')


class ProposalSchema(VisualisableElementSchema, SerchableEntitySchema):

    name = NameSchemaNode(
        editing=context_is_a_proposal,
        )

    body = colander.SchemaNode(
        colander.String(),
        widget= RichTextWidget()
        )

    ideas  = colander.SchemaNode(
                    colander.Set(),
                    widget=ideas_choice,
                    title=_('Related ideas'),
                    missing=[],
                    default=[]
                )


@content(
    'proposal',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IProposal)
class Proposal(Commentabl, SerchableEntity):
    result_template = 'novaideo:views/templates/proposal_result.pt' 
    name = renamer()
    author = SharedUniqueProperty('author')
    tokens = CompositeMultipleProperty('tokens')
    ideas = SharedMultipleProperty('ideas')

    def __init__(self, **kwargs):
        super(ActionProposal, self).__init__(**kwargs)
        self.set_data(kwargs)


    def setauthor(self, author):
        self.setproperty('author', author)

    def settokens(self, tokens):
        self.setproperty('tokens', tokens)

    def setideas(self, ideas):
        self.setproperty('ideas', ideas)

