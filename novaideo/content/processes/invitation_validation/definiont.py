from dace.interfaces import IProcessDefinition
from dace.processdefinition.processdef import ProcessDefinition
from dace.processdefinition.activitydef import ActivityDefinition
from dace.processdefinition.gatewaydef import (
    ExclusiveGatewayDefinition, 
    ParallelGatewayDefinition)
from dace.processdefinition.transitiondef import TransitionDefinition
from dace.processdefinition.eventdef import (
    StartEventDefinition,
    EndEventDefinition,
    IntermediateCatchEventDefinition,
    ConditionalEventDefinition,
    TimerEventDefinition)
from dace.objectofcollaboration.services.processdef_container import process_definition

from pontus.core import VisualisableElement

from .behaviors import (
    AcceptInvitation,
    RefuseInvitation,
    RemoveInvitation,
    RemindInvitation,
    ReinviteUser)


@process_definition(name='invitationvalidation', id='invitationvalidation')
class InvitationValidation(ProcessDefinition, VisualisableElement):
    isUnique = True
    isVolatile = True

    def __init__(self, **kwargs):
        super(InvitationValidation, self).__init__(**kwargs)
        self.title = 'Invitation validation'
        self.description = 'Invitation validation'

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                egar = ExclusiveGatewayDefinition(),
                accept = ActivityDefinition(contexts=[AcceptInvitation],
                                       description="Accept the invitation",
                                       title="Accept the invitation",
                                       groups=[]),
                refuse = ActivityDefinition(contexts=[RefuseInvitation],
                                       description="Refuse the invitation",
                                       title="Refuse the invitation",
                                       groups=[]),
                remove = ActivityDefinition(contexts=[RemoveInvitation],
                                       description="Remove the invitation",
                                       title="Remove the invitation",
                                       groups=[]),
                reinvite = ActivityDefinition(contexts=[ReinviteUser],
                                       description="Re-invite the person",
                                       title="Re-invite the person",
                                       groups=[]),
                remind = ActivityDefinition(contexts=[RemindInvitation],
                                       description="Remind the person",
                                       title="Remind the person",
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'egar'),
                TransitionDefinition('egar', 'accept'),
                TransitionDefinition('egar', 'refuse'),
                TransitionDefinition('pg', 'remove'),
                TransitionDefinition('accept', 'eg'),
                TransitionDefinition('refuse', 'reinvite'),
                TransitionDefinition('reinvite', 'egar'),
                TransitionDefinition('remove', 'eg'),
                TransitionDefinition('pg', 'remind'),
                TransitionDefinition('remind', 'eg'),
                TransitionDefinition('eg', 'end'),

        )
