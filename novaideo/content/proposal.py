import colander
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import getSite
from dace.objectofcollaboration.principal.util import get_current
from dace.descriptors import (
    CompositeMultipleProperty,
    SharedUniqueProperty,
    SharedMultipleProperty
)
from pontus.widget import RichTextWidget,Select2Widget
from pontus.core import VisualisableElementSchema

from .interface import IProposal
from novaideo.core import Commentable, can_access
from novaideo import _
from novaideo.core import (
    SearchableEntity,
    SearchableEntitySchema,
    CorrelableEntity,
    DuplicableEntity)


@colander.deferred
def ideas_choice(node, kw):
    root = getSite()
    user = get_current()
    ideas = [i for i in root.ideas if can_access(user, i)]
    values = [(i, i.title) for i in ideas]
    return Select2Widget(values=values, multiple=True)


def context_is_a_proposal(context, request):
    return request.registry.content.istype(context, 'proposal')


class ProposalSchema(VisualisableElementSchema, SearchableEntitySchema):

    name = NameSchemaNode(
        editing=context_is_a_proposal,
        )

    text = colander.SchemaNode(
        colander.String(),
        widget= RichTextWidget(),
        )

    related_ideas  = colander.SchemaNode(
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
class Proposal(Commentable, SearchableEntity, DuplicableEntity, CorrelableEntity):
    result_template = 'novaideo:views/templates/proposal_result.pt'
    name = renamer()
    author = SharedUniqueProperty('author')
    working_group = SharedUniqueProperty('working_group', 'proposal')
    tokens = CompositeMultipleProperty('tokens')

    def __init__(self, **kwargs):
        super(Proposal, self).__init__(**kwargs)
        self.set_data(kwargs)

    @property
    def related_ideas(self):
        return [c.target for c in self.target_correlations if ((c.type==1) and ('related_ideas' in c.tags))]
