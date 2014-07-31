import colander
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.objectofcollaboration.application import Application
from dace.descriptors import CompositeMultipleProperty
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import SequenceWidget
from pontus.schema import omit

from .working_group import WorkingGroupSchema, WorkingGroup
from .organization import OrganizationSchema, Organization
from .interface import INovaIdeoApplication
from .invitation import InvitationSchema, Invitation
from novaideo import _



default_titles = ['Mr', 'Madam', 'Miss']


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
                title=_('List of titles')
                )

    invitations = colander.SchemaNode(
                        colander.Sequence(),
                        omit(InvitationSchema(factory=Invitation,
                                               editable=True,
                                               name=_('Invitations')),['_csrf_token_']),
                        title=_('List of invitation')
                        )

    working_groups = colander.SchemaNode(
                        colander.Sequence(),
                        omit(WorkingGroupSchema(factory=WorkingGroup,
                                editable=True,
                                name=_('Working group')),['_csrf_token_']),
                        title=_('Working groups')
                        )

    organizations = colander.SchemaNode(
                        colander.Sequence(),
                        omit(OrganizationSchema(factory=Organization,
                                editable=True,
                                name=_('Organization')),['_csrf_token_']),
                        title=_('Organizations')
                        )

    participants_mini = colander.SchemaNode(
                            colander.Integer(),
                            title=_('Minimum number of participants for a working group'),
                            default=3
                            )

    participants_maxi = colander.SchemaNode(
                            colander.Integer(),
                            title=_('Maximum number of participants for a working group'),
                            default=12
                            )

    participations_maxi = colander.SchemaNode(
                            colander.Integer(),
                            title=_('Maximum number of working group by member'),
                            default=5
                            )

    tokens_mini = colander.SchemaNode(
                            colander.Integer(),
                            title=_('Minimum number of tokens by member'),
                            default=7
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
    organizations = CompositeMultipleProperty('organizations')
    invitations = CompositeMultipleProperty('invitations')


    def __init__(self, **kwargs):
        super(NovaIdeoApplication, self).__init__(**kwargs)
        self.title = 'NovaIdeo'
        self.participants_mini = 3
        self.participants_maxi = 12
        self.participations_maxi = 5
        self.tokens_mini = 7
        self.titles = default_titles

    def setworking_groups(self, working_groups):
        self.setproperty('working_groups', working_groups)

    def setorganizations(self, organizations):
        self.setproperty('organizations', organizations)

    def setinvitations(self, invitations):
        self.setproperty('invitations', invitations)
