# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
"""
This module represent the Ballot global process definition
powered by the dace engine. This process is unique, which means that
this process is instantiated only once. And is used as part of a sub-process.
And is vlolatile, which means that this process is automatically removed after
the end.
"""
import pytz
from datetime import datetime

from dace.processdefinition.processdef import ProcessDefinition
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
from dace.objectofcollaboration.services.processdef_container import (
    process_definition)
from pontus.core import VisualisableElement

from novaideo import _
from novaideo.content.processes.proposal_management.behaviors import (
    VP_DEFAULT_DURATION)


def time_duration(process):
    if hasattr(process, 'duration'):
        return getattr(process, 'duration')

    return VP_DEFAULT_DURATION


def event_condition(process):
    execution_context = process.execution_context
    processes = execution_context.get_involved_collection('vote_processes')
    if not processes:
        return True

    for ballot_process in processes:
        if not ballot_process._finished:
            return False

    for ballot in process.ballots:
        ballot.finished_at = datetime.now(tz=pytz.UTC)

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
                timer = IntermediateCatchEventDefinition(
                           TimerEventDefinition(time_duration=time_duration)),
                conditional = IntermediateCatchEventDefinition(
                             ConditionalEventDefinition(event_condition)),
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