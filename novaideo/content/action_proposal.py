import colander
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from pontus.schema import omit
from pontus.widget import RichTextWidget
from dace.objectofcollaboration.entity import Entity
from dace.descriptors import CompositeMultipleProperty, SharedUniqueProperty

from pontus.core import VisualisableElement, VisualisableElementSchema

from .keyword import KeywordSchema, Keyword
from .interface import IActionProposal
from novaideo import _

def context_is_a_actionproposal(context, request):
    return request.registry.content.istype(context, 'actionproposal')


class ActionProposalSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_actionproposal,
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

@content(
    'actionproposal',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IActionProposal)
class ActionProposal(VisualisableElement, Entity):
    name = renamer()
    author = SharedUniqueProperty('author')
    tokens = CompositeMultipleProperty('tokens')
    keywords = CompositeMultipleProperty('keywords')

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

