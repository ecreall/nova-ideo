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

from .behaviors import InviteUsers, AddUsers


@process_definition(name='usermanagement', id='usermanagement')
class UserManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(UserManagement, self).__init__(**kwargs)
        self.title = 'Users management'
        self.description = 'Users management'

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                add = ActivityDefinition(contexts=[AddUsers],
                                       description="Upload users from xl file",
                                       title="Upload users",
                                       groups=['Add','User']),
                invite = ActivityDefinition(contexts=[InviteUsers],
                                       description="Invite users",
                                       title="Invite users",
                                       groups=['Add','User']),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'add'),
                TransitionDefinition('pg', 'invite'),
                TransitionDefinition('add', 'eg'),
                TransitionDefinition('invite', 'eg'),
                TransitionDefinition('eg', 'end'),
        )
