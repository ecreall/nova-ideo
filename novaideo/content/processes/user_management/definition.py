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
    Registration,
    Edit,
    Activate,
    Deactivate,
    SeePerson)
from novaideo import _


@process_definition(name='usermanagement', id='usermanagement')
class UserManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(UserManagement, self).__init__(**kwargs)
        self.title = _('User management')
        self.description = _('User management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                registration = ActivityDefinition(contexts=[Registration],
                                       description=_("User registration"),
                                       title=_("User registration"),
                                       groups=[]),
                edit = ActivityDefinition(contexts=[Edit],
                                       description=_("Edit"),
                                       title=_("Edit"),
                                       groups=[]),
                deactivate = ActivityDefinition(contexts=[Deactivate],
                                       description=_("Deactivate"),
                                       title=_("Deactivate"),
                                       groups=[]),
                activate = ActivityDefinition(contexts=[Activate],
                                       description=_("Activate"),
                                       title=_("Activate"),
                                       groups=[]),
                see = ActivityDefinition(contexts=[SeePerson],
                                       description=_("Details"),
                                       title=_("Details"),
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'registration'),
                TransitionDefinition('pg', 'edit'),
                TransitionDefinition('edit', 'eg'),
                TransitionDefinition('registration', 'eg'),
                TransitionDefinition('pg', 'deactivate'),
                TransitionDefinition('deactivate', 'eg'),
                TransitionDefinition('pg', 'activate'),
                TransitionDefinition('activate', 'eg'),
                TransitionDefinition('pg', 'see'),
                TransitionDefinition('see', 'eg'),
                TransitionDefinition('eg', 'end'),

        )
