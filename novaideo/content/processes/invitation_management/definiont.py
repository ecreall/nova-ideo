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
    InviteUsers,
    UploadUsers,
    SeeInvitation,
    SeeInvitations,
    EditInvitations,
    EditInvitation)


@process_definition(name='invitationmanagement', id='invitationmanagement')
class InvitationManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(InvitationManagement, self).__init__(**kwargs)
        self.title = 'Invitations management'
        self.description = 'Invitations management'

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                add = ActivityDefinition(contexts=[UploadUsers],
                                       description="Upload users from xl file",
                                       title="Upload users",
                                       groups=['Invite']),
                invite = ActivityDefinition(contexts=[InviteUsers],
                                       description="Invite users",
                                       title="Invite users",
                                       groups=['Invite']),
                seeinvitation = ActivityDefinition(contexts=[SeeInvitation],
                                       description="See the invitation",
                                       title="Details",
                                       groups=[]),
                seeinvitations = ActivityDefinition(contexts=[SeeInvitations],
                                       description="See the invitations",
                                       title="Invitations",
                                       groups=[]),
                edits = ActivityDefinition(contexts=[EditInvitations],
                                       description="Edit invitations",
                                       title="Edit invitations",
                                       groups=['Edit']),
                edit = ActivityDefinition(contexts=[EditInvitation],
                                       description="Edit invitation",
                                       title="Edit invitation",
                                       groups=['Edit']),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'add'),
                TransitionDefinition('pg', 'invite'),
                TransitionDefinition('pg', 'edits'),
                TransitionDefinition('pg', 'edit'),
                TransitionDefinition('add', 'eg'),
                TransitionDefinition('pg', 'seeinvitation'),
                TransitionDefinition('seeinvitation', 'eg'),
                TransitionDefinition('pg', 'seeinvitations'),
                TransitionDefinition('seeinvitations', 'eg'),
                TransitionDefinition('invite', 'eg'),
                TransitionDefinition('edits', 'eg'),
                TransitionDefinition('edit', 'eg'),
                TransitionDefinition('eg', 'end'),
        )
