import colander
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import getSite
from dace.descriptors import (
    CompositeMultipleProperty,
    SharedUniqueProperty,
    SharedMultipleProperty
)
from pontus.widget import RichTextWidget,Select2Widget
from pontus.core import VisualisableElementSchema

from .interface import IProposal
from novaideo.core import Commentabl
from novaideo import _
from novaideo.core import (
    SerchableEntity,
    SerchableEntitySchema,
    CorrelableEntity)


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
        widget= RichTextWidget(),
        )

    ideas  = colander.SchemaNode(
        colander.Set(),
        widget=ideas_choice,
        title=_('Related ideas'),
        missing=[],
        default=[],
        )


@content(
    'proposal',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IProposal)
class Proposal(Commentabl, SerchableEntity, CorrelableEntity):
    result_template = 'novaideo:views/templates/proposal_result.pt'
    name = renamer()
    author = SharedUniqueProperty('author')
    tokens = CompositeMultipleProperty('tokens')
    ideas = SharedMultipleProperty('ideas')

    def __init__(self, **kwargs):
        super(Proposal, self).__init__(**kwargs)
        self.set_data(kwargs)
