# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
"""
This module represent the Proposal management process definition 
powered by the dace engine.
"""

from dace.processdefinition.processdef import ProcessDefinition
from dace.processdefinition.activitydef import (
    ActivityDefinition)
from dace.processdefinition.gatewaydef import (
    ExclusiveGatewayDefinition,
    ParallelGatewayDefinition)
from dace.processdefinition.transitiondef import TransitionDefinition
from dace.processdefinition.eventdef import (
    StartEventDefinition,
    EndEventDefinition,
    IntermediateCatchEventDefinition,
    TimerEventDefinition)
from dace.objectofcollaboration.services.processdef_container import (
    process_definition)
from pontus.core import VisualisableElement

from novaideo.content.processes.proposal_management.behaviors import (
    calculate_amendments_cycle_duration)
from .behaviors import (
    CorrectProposal,
    CorrectItem,
    CloseWork
    )
from novaideo import _


@process_definition(name='correctionworkmodeprocess', id='correctionworkmodeprocess')
class CorrectionWorkModeProcess(ProcessDefinition, VisualisableElement):
    isControlled = True
    isSubProcess = True
    isVolatile = True

    def __init__(self, **kwargs):
        super(CorrectionWorkModeProcess, self).__init__(**kwargs)
        self.title = _('Change with validation')
        self.description = _('Change with validation')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                eg1 = ExclusiveGatewayDefinition(),
                pg1 = ParallelGatewayDefinition(),
                eg2 = ExclusiveGatewayDefinition(),
                correct = ActivityDefinition(contexts=[CorrectProposal],
                                       description=_("Improve the proposal"),
                                       title=_("Improve"),
                                       groups=[]),
                correctitem = ActivityDefinition(contexts=[CorrectItem],
                                       description=_("Correct item"),
                                       title=_("Correct"),
                                       groups=[]),
                close_work = ActivityDefinition(contexts=[CloseWork],
                                       description=_("Close work"),
                                       title=_("Close work"),
                                       groups=[]),
                timer = IntermediateCatchEventDefinition(TimerEventDefinition(time_date=calculate_amendments_cycle_duration)),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg1'),
                TransitionDefinition('pg1', 'correct'),
                TransitionDefinition('pg1', 'correctitem'),
                TransitionDefinition('pg1', 'timer'),
                TransitionDefinition('timer', 'close_work'),
                TransitionDefinition('close_work', 'end'),
        )
