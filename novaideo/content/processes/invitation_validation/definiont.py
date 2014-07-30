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
from novaideo import _


@process_definition(name='invitationvalidation', id='invitationvalidation')
class InvitationValidation(ProcessDefinition, VisualisableElement):
    isUnique = True
    isVolatile = True

    def __init__(self, **kwargs):
        super(InvitationValidation, self).__init__(**kwargs)
        self.title = _('Invitation validation')
        self.description = _('Invitation validation')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                egar = ExclusiveGatewayDefinition(),
                accept = ActivityDefinition(contexts=[AcceptInvitation],
                                       description=_("Accept the invitation"),
                                       title=_("Accept the invitation"),
                                       groups=[]),
                refuse = ActivityDefinition(contexts=[RefuseInvitation],
                                       description=_("Refuse the invitation"),
                                       title=_("Refuse the invitation"),
                                       groups=[]),
                remove = ActivityDefinition(contexts=[RemoveInvitation],
                                       description=_("Remove the invitation"),
                                       title=_("Remove the invitation"),
                                       groups=[]),
                reinvite = ActivityDefinition(contexts=[ReinviteUser],
                                       description=_("Re-invite the person"),
                                       title=_("Re-invite the person"),
                                       groups=[]),
                remind = ActivityDefinition(contexts=[RemindInvitation],
                                       description=_("Remind the person"),
                                       title=_("Remind the person"),
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
