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
from .commentabl import Commentabl
from novaideo import _


@colander.deferred
def ideas_choice(node, kw):
    root = getSite()
    ideas = [i for i in root.ideas if 'published' in i.state]
    values = [(i, i) for i in ideas]
    return Select2Widget(values=values, multiple=True)


def context_is_a_proposal(context, request):
    return request.registry.content.istype(context, 'proposal')


class ProposalSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_proposal,
        )

    body = colander.SchemaNode(
        colander.String(),
        widget= RichTextWidget()
        )

    keywords = colander.SchemaNode(
                   colander.Sequence(),
                   omit(KeywordSchema(factory=Keyword,
                                      editable=True,
                                      name=_('Keyword')),['_csrf_token_']),
                   title=_('Keywords')
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
class Proposal(Commentabl):
    name = renamer()
    author = SharedUniqueProperty('author')
    tokens = CompositeMultipleProperty('tokens')
    keywords = CompositeMultipleProperty('keywords')
    ideas = SharedMultipleProperty('ideas')

    def __init__(self, **kwargs):
        super(ActionProposal, self).__init__(**kwargs)
        if 'body' in kwargs:
            self.body = kwargs.get('body')

        if 'keywords' in kwargs:
            self.keywords = kwargs.get('keywords')

    def setauthor(self, author):
        self.setproperty('author', author)

    def settokens(self, tokens):
        self.setproperty('tokens', tokens)

    def setkeywords(self, keywords):
        self.setproperty('keywords', keywords)

    def setideas(self, ideas):
        self.setproperty('ideas', ideas)

