import colander
import deform
import deform.widget
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from pontus.schema import Schema, omit, select
from pontus.widget import RichTextWidget, LineWidget, TableWidget
from dace.objectofcollaboration.entity import Entity
from dace.objectofcollaboration.object import (
                COMPOSITE_UNIQUE,
                SHARED_UNIQUE,
                COMPOSITE_MULTIPLE,
                SHARED_MULTIPLE,
                Object)

from pontus.core import VisualisableElement, VisualisableElementSchema

from .keyword import KeywordSchema, Keyword
from .interface import IActionProposal


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
                   omit(KeywordSchema(widget=LineWidget(),
                                      factory=Keyword,
                                      editable=True,
                                      name='Keyword'),['_csrf_token_']),
                   widget=TableWidget(),
                   title='Keywords'
                )

@content(
    'actionproposal',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IActionProposal)
class ActionProposal(VisualisableElement, Entity):
    name = renamer()
    properties_def = {'author':(SHARED_UNIQUE, None, False),
                      'tokens':(COMPOSITE_MULTIPLE, None, False),
                      'keywords':(COMPOSITE_MULTIPLE, None, False)}

    def __init__(self, **kwargs):
        super(ActionProposal, self).__init__(**kwargs)
        if 'body' in kwargs:
            self.body = kwargs.get('body')

        if 'keywords' in kwargs:
            self.keywords = kwargs.get('keywords')

    @property
    def author(self):
        return self.getproperty('author')

    def setauthor(self, author):
        self.setproperty('author', author)

    @property
    def tokens(self):
        return self.getproperty('tokens')

    def settokens(self, tokens):
        self.setproperty('tokens', tokens)

    @property
    def keywords(self):
        return self.getproperty('keywords')

    def setkeywords(self, keywords):
        self.setproperty('keywords', keywords)

