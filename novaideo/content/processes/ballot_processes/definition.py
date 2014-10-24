from datetime import timedelta, datetime
from persistent.list import PersistentList

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

from novaideo import _


def time_duration(process):
    return process.duration + datetime.today()


def event_condition(process):
    processes = process.execution_context.get_involved_collection('vote_processes')
    for p in processes:
        if not p._finished:
            return False

    for ballot in process.ballots:
        ballot.finished_at = datetime.today()

    return True


@process_definition(name='ballotprocess', id='ballotprocess')
class BallotProcess(ProcessDefinition, VisualisableElement):
    isControlled = True
    isSubProcess = True
    isVolatile = True
    id = 'ballotprocess'

    def __init__(self, **kwargs):
        super(BallotProcess, self).__init__(**kwargs)
        self.title = _('Ballot Process')
        self.description = _('Ballot Process')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                timer = IntermediateCatchEventDefinition(TimerEventDefinition(time_date=time_duration)),
                conditional = IntermediateCatchEventDefinition(ConditionalEventDefinition(event_condition)),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'timer'),
                TransitionDefinition('pg', 'conditional'),
                TransitionDefinition('conditional', 'eg'),
                TransitionDefinition('timer', 'eg'),
                TransitionDefinition('eg', 'end'),

        )
