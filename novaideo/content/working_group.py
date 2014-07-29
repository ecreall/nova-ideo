from zope.interface import implementer

from substanced.content import content
from substanced.util import renamer
from substanced.schema import NameSchemaNode

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import CompositeUniqueProperty
from pontus.schema import omit
from pontus.core import VisualisableElement, VisualisableElementSchema

from .action_proposal import ActionProposalSchema, ActionProposal
from .interface import IWorkingGroup


def context_is_a_workinggroup(context, request):
    return request.registry.content.istype(context, 'workinggroup')


class WorkingGroupSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_workinggroup,
        )

    action_proposal = omit(ActionProposalSchema(name='action proposal',
                                                factory=ActionProposal,
                                                editable=True),['_csrf_token_'])


@content(
    'workinggroup',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IWorkingGroup)
class WorkingGroup(VisualisableElement, Entity):
    name = renamer()
    template = 'pontus:templates/visualisable_templates/object.pt'
    action_proposal = CompositeUniqueProperty('action_proposal', 'myparent')

    def __init__(self, **kwargs):
        super(WorkingGroup, self).__init__(**kwargs)

    def setaction_proposal(self, action_proposal):
        self.setproperty('action_proposal', action_proposal)


