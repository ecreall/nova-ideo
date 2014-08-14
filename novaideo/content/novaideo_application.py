import colander
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.objectofcollaboration.application import Application
from dace.descriptors import CompositeMultipleProperty
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import SequenceWidget, LineWidget, TableWidget
from pontus.schema import omit

from .working_group import WorkingGroupSchema, WorkingGroup
from .organization import OrganizationSchema, Organization
from .idea import IdeaSchema, Idea
from .interface import INovaIdeoApplication
from .invitation import InvitationSchema, Invitation
from .keyword import KeywordSchema, Keyword
from novaideo import _


default_titles = [_('Mr'), _('Madam'), _('Miss')]

default_comment_intentions = [_('Ironie'), _('Humour'), _('Remarque')]

default_correlation_intentions = [_('Ironie'), _('Humour'), _('Remarque')]

default_idea_intentions = [_('Ammelioration'), _('Humour'), _('Ironie')]


def context_is_a_root(context, request):
    return request.registry.content.istype(context, 'Root')


class NovaIdeoApplicationSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_root,
        )

    titles = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            colander.String(),
            name=_("Title")
            ),
        widget=SequenceWidget(),
        default=default_titles,
        title=_('List of titles'),
        )

    comment_intention = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            colander.String(),
            name=_("Comment intention")
            ),
        widget=SequenceWidget(),
        default=default_comment_intentions,
        title=_('Comment intentions'),
        )

    idea_intention = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            colander.String(),
            name=_("Idea intention")
            ),
        widget=SequenceWidget(),
        default=default_idea_intentions,
        title=_('Idea intentions'),
        )

    invitations = colander.SchemaNode(
        colander.Sequence(),
        omit(InvitationSchema(factory=Invitation,
                               editable=True,
                               name=_('Invitations')),['_csrf_token_']),
        title=_('List of invitation'),
        )

    working_groups = colander.SchemaNode(
        colander.Sequence(),
        omit(WorkingGroupSchema(factory=WorkingGroup,
                editable=True,
                name=_('Working group')),['_csrf_token_']),
        title=_('Working groups'),
        )

    organizations = colander.SchemaNode(
        colander.Sequence(),
        omit(OrganizationSchema(factory=Organization,
                editable=True,
                name=_('Organization')),['_csrf_token_']),
        title=_('Organizations'),
        )

    keywords = colander.SchemaNode(
        colander.Sequence(),
        omit(KeywordSchema(widget=LineWidget(),
                           factory=Keyword,
                           editable=True,
                           name='Keyword'),['_csrf_token_']),
        widget=TableWidget(min_len=1),
        title='Keywords',
        )

    ideas = colander.SchemaNode(
        colander.Sequence(),
        omit(IdeaSchema(factory=Idea,
                        name=_('Idea')),['_csrf_token_']),
        title=_('Ideas'),
        )

    participants_mini = colander.SchemaNode(
        colander.Integer(),
        title=_('Minimum number of participants for a working group'),
        default=3,
        )

    participants_maxi = colander.SchemaNode(
        colander.Integer(),
        title=_('Maximum number of participants for a working group'),
        default=12,
        )

    participations_maxi = colander.SchemaNode(
        colander.Integer(),
        title=_('Maximum number of working group by member'),
        default=5,
        )

    tokens_mini = colander.SchemaNode(
        colander.Integer(),
        title=_('Minimum number of tokens by member'),
        default=7,
        )


@content(
    'Root',
    icon='glyphicon glyphicon-home',
    after_create='after_create',
    )
@implementer(INovaIdeoApplication)
class NovaIdeoApplication(VisualisableElement, Application):
    name = renamer()
    working_groups = CompositeMultipleProperty('working_groups')
    proposals = CompositeMultipleProperty('proposals')
    organizations = CompositeMultipleProperty('organizations')
    invitations = CompositeMultipleProperty('invitations')
    ideas = CompositeMultipleProperty('ideas')
    keywords = CompositeMultipleProperty('keywords')
    correlations = CompositeMultipleProperty('correlations')

    def __init__(self, **kwargs):
        super(NovaIdeoApplication, self).__init__(**kwargs)
        self.title = 'NovaIdeo'
        self.participants_mini = 3
        self.participants_maxi = 12
        self.participations_maxi = 5
        self.tokens_mini = 7
        self.titles = default_titles
        self.comment_intentions = default_comment_intentions
        self.correlation_intentions = default_correlation_intentions
        self.idea_intentions = default_idea_intentions

    @property
    def keywords_ids(self):
        return dict([(k.title, k) for k in self.keywords])

    def get_keywords(self, keywords_ids):
        result = []
        newkeywords = []
        for k in keywords_ids:
            if k in self.keywords_ids.keys():
                result.append(self.keywords_ids[k])
            else:
                key = Keyword(title=k)
                newkeywords.append(key)

        return result, newkeywords
