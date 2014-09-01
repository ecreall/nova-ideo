import colander
from zope.interface import implementer
from persistent.list import PersistentList
from pyramid.threadlocal import get_current_request

from substanced.interfaces import IUserLocator
from substanced.principal import DefaultUserLocator
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
    DuplicableEntity,
    VersionableEntity)


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
class Proposal(Commentable, VersionableEntity, SearchableEntity, DuplicableEntity, CorrelableEntity):
    result_template = 'novaideo:views/templates/proposal_result.pt'
    name = renamer()
    author = SharedUniqueProperty('author')
    working_group = SharedUniqueProperty('working_group', 'proposal')
    tokens = CompositeMultipleProperty('tokens')
    amendments = CompositeMultipleProperty('amendments', 'proposal')


    def __init__(self, **kwargs):
        super(Proposal, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.email_persons_contacted = PersistentList()

    @property
    def related_ideas(self):
        lists = [c.targets for c in self.source_correlations if ((c.type==1) and ('related_ideas' in c.tags))]
        return [target for targets in lists for target in targets]

    @property
    def persons_contacted(self):
        request = get_current_request()
        adapter = request.registry.queryMultiAdapter(
                (self, request),
                IUserLocator
                )
        if adapter is None:
            adapter = DefaultUserLocator(self, request)

        result = []
        for email in self.email_persons_contacted:
            user = adapter.get_user_by_email(email)
            if user is not None:
                result.append(user)
            else:
                result.append(email)

        return set(result)

