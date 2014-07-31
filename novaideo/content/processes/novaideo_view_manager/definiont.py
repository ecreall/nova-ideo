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
    AnonymousLogIn,
    SeeIdeas)
from novaideo import _


@process_definition(name='novaideoviewmanager', id='novaideoviewmanager')
class NovaIdeoViewManager(ProcessDefinition, VisualisableElement):
    isUnique = True
    isVolatile = True

    def __init__(self, **kwargs):
        super(NovaIdeoViewManager, self).__init__(**kwargs)
        self.title = _('User access manager')
        self.description = _('User access manager')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                login = ActivityDefinition(contexts=[AnonymousLogIn],
                                       description=_("Log in access"),
                                       title=_("Log in access"),
                                       groups=[]),
                seeideas = ActivityDefinition(contexts=[SeeIdeas],
                                       description=_("See ideas"),
                                       title=_("Ideas"),
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'login'),
                TransitionDefinition('login', 'eg'),
                TransitionDefinition('pg', 'seeideas'),
                TransitionDefinition('seeideas', 'eg'),
                TransitionDefinition('eg', 'end'),

        )
