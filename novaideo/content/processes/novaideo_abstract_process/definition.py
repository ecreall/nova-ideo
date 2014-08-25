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
    SelectEntity,
    DeselectEntity)
from novaideo import _


@process_definition(name='novaideoabstractprocess', id='novaideoabstractprocess')
class NovaIdeoAbstractProcess(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(NovaIdeoAbstractProcess, self).__init__(**kwargs)
        self.title = _('Abstract process')
        self.description = _('Abstract process')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                select = ActivityDefinition(contexts=[SelectEntity],
                                       description=_("Add to my selections"),
                                       title=_("Add to my selections"),
                                       groups=[]),
                deselect = ActivityDefinition(contexts=[DeselectEntity],
                                       description=_("Remove from my selections"),
                                       title=_("Remove from my selections"),
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'select'),
                TransitionDefinition('select', 'eg'),
                TransitionDefinition('pg', 'deselect'),
                TransitionDefinition('deselect', 'eg'),
                TransitionDefinition('eg', 'end'),

        )
