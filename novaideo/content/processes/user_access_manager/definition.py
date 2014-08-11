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
    LogIn,
    LogOut)
from novaideo import _


@process_definition(name='useraccessmanager', id='useraccessmanager')
class UserAccessManager(ProcessDefinition, VisualisableElement):
    isUnique = True
    isVolatile = True

    def __init__(self, **kwargs):
        super(UserAccessManager, self).__init__(**kwargs)
        self.title = _('User access manager')
        self.description = _('User access manager')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                login = ActivityDefinition(contexts=[LogIn],
                                       description=_("Log in"),
                                       title=_("Log in"),
                                       groups=[_("Access")]),
                logout = ActivityDefinition(contexts=[LogOut],
                                       description=_("Log out"),
                                       title=_("Log out"),
                                       groups=[_("Access")]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'login'),
                TransitionDefinition('pg', 'logout'),
                TransitionDefinition('login', 'eg'),
                TransitionDefinition('logout', 'eg'),
                TransitionDefinition('eg', 'end'),

        )
