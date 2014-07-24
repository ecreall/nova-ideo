import colander
from zope.interface import implementer

from substanced.content import content
from substanced.property import PropertySheet
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.objectofcollaboration.application import Application
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import TableWidget, LineWidget, CheckboxChoiceWidget, SequenceWidget
from pontus.schema import Schema, omit
from dace.objectofcollaboration.object import(
                COMPOSITE_UNIQUE,
                SHARED_UNIQUE,
                COMPOSITE_MULTIPLE,
                SHARED_MULTIPLE,
                Object)

from .working_group import WorkingGroupSchema, WorkingGroup
from .organization import OrganizationSchema, Organization
from .interface import INovaIdeoApplication
from .invitation import InvitationSchema, Invitation


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
                    name="Title"
                    ),
                widget=SequenceWidget(),
                default=default_titles,
                title='List of titles'
                )

    invitations = colander.SchemaNode(
                        colander.Sequence(),
                        omit(InvitationSchema(factory=Invitation,
                                               editable=True,
                                               name='Invitations'),['_csrf_token_']),
                        title='List of invitation'
                        )

    working_groups = colander.SchemaNode(
                        colander.Sequence(),
                        omit(WorkingGroupSchema(widget=LineWidget(),
                                factory=WorkingGroup,
                                editable=True,
                                name='Working group'),['_csrf_token_']),
                        widget=TableWidget(),
                        title='Working groups'
                        )

    organizations = colander.SchemaNode(
                        colander.Sequence(),
                        omit(OrganizationSchema(widget=LineWidget(),
                                factory=Organization,
                                editable=True,
                                name='Organization'),['_csrf_token_']),
                        widget=TableWidget(),
                        title='Organizations'
                        )

    participants_mini = colander.SchemaNode(
                            colander.Integer(),
                            title='Minimum number of participants for a working group',
                            default=3
                            )

    participants_maxi = colander.SchemaNode(
                            colander.Integer(),
                            title='Maximum number of participants for a working group',
                            default=12
                            )

    participations_maxi = colander.SchemaNode(
                            colander.Integer(),
                            title='Maximum number of working group by member',
                            default=5
                            )

    tokens_mini = colander.SchemaNode(
                            colander.Integer(),
                            title='Minimum number of tokens by member',
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
    properties_def = {'working_groups':(COMPOSITE_MULTIPLE, None, False),
                      'organizations':(COMPOSITE_MULTIPLE, None, False),
                      'invitations':(COMPOSITE_MULTIPLE, None, False)}

    def __init__(self, **kwargs):
        super(NovaIdeoApplication, self).__init__(**kwargs)
        self.title = 'NovaIdeo'
        self.participants_mini = 3
        self.participants_maxi = 12
        self.participations_maxi = 5
        self.tokens_mini = 7
        self.titles = default_titles

    @property
    def working_groups(self):
        return self.getproperty('working_groups')

    def setworking_groups(self, working_groups):
        self.setproperty('working_groups', working_groups)

    @property
    def organizations(self):
        return self.getproperty('organizations')

    def setorganizations(self, organizations):
        self.setproperty('organizations', organizations)

    @property
    def invitations(self):
        return self.getproperty('invitations')

    def setinvitations(self, invitations):
        self.setproperty('invitations', invitations)
