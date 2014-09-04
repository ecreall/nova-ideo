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

from .behaviors import Favour, Against
from novaideo import _



def time_duration(process):
    return getattr(process.ballot, 'duration')


@process_definition(name='referendumprocess', id='referendumprocess')
class ReferendumProcess(ProcessDefinition, VisualisableElement):
    isUnique = True
    isVolatile = True
    isControlled = True

    def __init__(self, **kwargs):
        super(ReferendumProcess, self).__init__(**kwargs)
        self.title = _('Referendum Process')
        self.description = _('Referendum Process')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                eg = ExclusiveGatewayDefinition(),
                favour = ActivityDefinition(contexts=[Favour],
                                       description=_("Vote in favour"),
                                       title=_("Vote in favour"),
                                       groups=[]),
                against = ActivityDefinition(contexts=[Against],
                                       description=_("Vote against"),
                                       title=_("Vote against"),
                                       groups=[]),
                timer = IntermediateCatchEventDefinition(TimerEventDefinition(time_duration=time_duration)),
                eg1 = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'eg'),
                TransitionDefinition('eg', 'favour'),
                TransitionDefinition('eg', 'against'),
                TransitionDefinition('eg', 'timer'),
                TransitionDefinition('favour', 'eg1'),
                TransitionDefinition('against', 'eg1'),
                TransitionDefinition('timer', 'eg1'),
                TransitionDefinition('eg1', 'end'),

        )
