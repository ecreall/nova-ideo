# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import datetime
from zope.interface import implementer
from persistent.list import PersistentList

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer
from substanced.property import PropertySheet

from dace.objectofcollaboration.application import Application
from dace.descriptors import CompositeMultipleProperty
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import (
    SequenceWidget, LineWidget, TableWidget, SimpleMappingWidget)
from pontus.schema import omit, select

from .working_group import WorkingGroupSchema, WorkingGroup
from .organization import OrganizationSchema, Organization
from .idea import IdeaSchema, Idea
from .interface import INovaIdeoApplication
from .invitation import InvitationSchema, Invitation
from .keyword import KeywordSchema, Keyword
from novaideo import _


DEFAULT_TITLES = [_('Mr'), _('Madam'), _('Miss')]

DEFAULT_COMMENT_INTENTIONS = [_('Irony'), _('Humor'), _('Remark')]

DEFAULT_CORRELATION_INTENTIONS = [_('Irony'), _('Humor'), _('Remark')]

DEFAULT_IDEA_INTENTIONS = [_('Improvement'), _('Humor'), _('Irony')]

DEFAULT_AMENDMENT_INTENTIONS = [
            _('Changer une idée'),
            _('Proposer des améliorations'),
            _('Reformuler'),
            _('Généraliser'),
            _('Détailler'),
            _('Poser une question'),
            _('Donner un avis'),
            _('Ironiser'),
            _('Faire de l\'humour')
]


def context_is_a_root(context, request):
    return request.registry.content.istype(context, 'Root')


class NovaIdeoApplicationSchema(VisualisableElementSchema):
    """Schema for Nova-Ideo configuration"""

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
        default=DEFAULT_TITLES,
        title=_('List of titles'),
        )

    comment_intention = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            colander.String(),
            name=_("Comment intention")
            ),
        widget=SequenceWidget(),
        default=DEFAULT_COMMENT_INTENTIONS,
        title=_('Comment intentions'),
        )

    idea_intention = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            colander.String(),
            name=_("Idea intention")
            ),
        widget=SequenceWidget(),
        default=DEFAULT_IDEA_INTENTIONS,
        title=_('Idea intentions'),
        )

    amendment_intention = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            colander.String(),
            name=_("Amendment intention")
            ),
        widget=SequenceWidget(),
        default=DEFAULT_AMENDMENT_INTENTIONS,
        title=_('Amendment intentions'),
        )

    invitations = colander.SchemaNode(
        colander.Sequence(),
        omit(InvitationSchema(factory=Invitation,
                               editable=True,
                               name=_('Invitations'),
                               widget=SimpleMappingWidget(css_class='object-well invitation-well')),
            ['_csrf_token_']),
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
                name=_('Organization'),
                widget=SimpleMappingWidget(css_class='object-well invitation-well'),
                omit=['managers']),
            ['_csrf_token_']),
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

    deadline = colander.SchemaNode(
                colander.DateTime(),
                title=_('Deadline')
                )


class NovaIdeoApplicationPropertySheet(PropertySheet):
    schema = select(NovaIdeoApplicationSchema(), ['title',
                                                  'participants_mini', 
                                                  'participants_maxi',
                                                  'participations_maxi',
                                                  'tokens_mini'])


@content(
    'Root',
    icon='glyphicon glyphicon-home',
    propertysheets = (
        ('Basic', NovaIdeoApplicationPropertySheet),
        ),
    after_create='after_create',
    )
@implementer(INovaIdeoApplication)
class NovaIdeoApplication(VisualisableElement, Application):
    """Nova-Ideo class (Root)"""

    name = renamer()
    working_groups = CompositeMultipleProperty('working_groups')
    proposals = CompositeMultipleProperty('proposals')
    organizations = CompositeMultipleProperty('organizations')
    invitations = CompositeMultipleProperty('invitations')
    ideas = CompositeMultipleProperty('ideas')
    keywords = CompositeMultipleProperty('keywords')
    correlations = CompositeMultipleProperty('correlations')
    files = CompositeMultipleProperty('files')

    def __init__(self, **kwargs):
        super(NovaIdeoApplication, self).__init__(**kwargs)
        self.initialization()

    def initialization(self):
        self.participants_mini = 3
        self.participants_maxi = 12
        self.participations_maxi = 5
        self.tokens_mini = 7
        self.titles = DEFAULT_TITLES
        self.comment_intentions = DEFAULT_COMMENT_INTENTIONS
        self.correlation_intentions = DEFAULT_CORRELATION_INTENTIONS
        self.idea_intentions = DEFAULT_IDEA_INTENTIONS
        self.amendment_intentions = DEFAULT_AMENDMENT_INTENTIONS
        self.deadlines = PersistentList([datetime.datetime.today()])

    @property
    def keywords_ids(self):
        """Return titles of keywords"""

        return dict([(k.title, k) for k in self.keywords])

    def get_keywords(self, keywords_ids):
        """
        Return existing Keywords objects in the application 
        if keyword is in the application otherwise return a new key object
        """
        result = []
        newkeywords = []
        for k in keywords_ids:
            if k in self.keywords_ids.keys():
                result.append(self.keywords_ids[k])
            else:
                key = Keyword(title=k)
                newkeywords.append(key)

        return result, newkeywords
