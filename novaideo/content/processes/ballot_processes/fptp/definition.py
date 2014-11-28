# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
"""
This module represent the FPTP election process definition 
powered by the dace engine. This process is vlolatile, which means 
that this process is automatically removed after the end. And is controlled, 
which means that this process is not automatically instanciated.
"""

import datetime
from dace.processdefinition.processdef import ProcessDefinition
from dace.processdefinition.activitydef import ActivityDefinition
from dace.processdefinition.gatewaydef import (
    ExclusiveGatewayDefinition)
from dace.processdefinition.transitiondef import TransitionDefinition
from dace.processdefinition.eventdef import (
    StartEventDefinition,
    EndEventDefinition,
    IntermediateCatchEventDefinition,
    TimerEventDefinition)
from dace.objectofcollaboration.services.processdef_container import(
    process_definition)
from pontus.core import VisualisableElement

from .behaviors import Vote
from novaideo import _



def time_duration(process):
    return getattr(process.ballot, 'duration') + datetime.datetime.today()


@process_definition(name='fptpprocess', id='fptpprocess')
class FPTPProcess(ProcessDefinition, VisualisableElement):
    isVolatile = True
    isControlled = True
    discriminator = 'Vote process'

    def __init__(self, **kwargs):
        super(FPTPProcess, self).__init__(**kwargs)
        self.title = _('FPTP Process')
        self.description = _('FPTP Process')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                eg = ExclusiveGatewayDefinition(),
                vote = ActivityDefinition(contexts=[Vote],
                                       description=_("Vote"),
                                       title=_("Vote"),
                                       groups=[]),
                timer = IntermediateCatchEventDefinition(
                            TimerEventDefinition(time_date=time_duration)),
                eg1 = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'eg'),
                TransitionDefinition('eg', 'vote'),
                TransitionDefinition('eg', 'timer'),
                TransitionDefinition('vote', 'eg1'),
                TransitionDefinition('timer', 'eg1'),
                TransitionDefinition('eg1', 'end'),
        )
