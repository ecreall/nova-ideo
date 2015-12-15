# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
from dace.processdefinition.processdef import ProcessDefinition
from dace.processdefinition.activitydef import ActivityDefinition
from dace.processdefinition.gatewaydef import (
    ExclusiveGatewayDefinition,
    ParallelGatewayDefinition)
from dace.processdefinition.eventdef import (
    IntermediateCatchEventDefinition,
    TimerEventDefinition)
from dace.processdefinition.transitiondef import TransitionDefinition
from dace.processdefinition.eventdef import (
    StartEventDefinition,
    EndEventDefinition)
from dace.objectofcollaboration.services.processdef_container import (
    process_definition)
from pontus.core import VisualisableElement

from .behaviors import (
    DeactivateUsers
    )
from novaideo import _


def calculate_next_date_block1(process):
    next_date = datetime.timedelta(days=1) + \
                datetime.datetime.today()
    return datetime.datetime.combine(next_date,
                              datetime.time(0, 0, 0, tzinfo=pytz.UTC))


# def calculate_next_date_block2(process):
#     #TODO
#     next_date = datetime.timedelta(days=1) + \
#                 datetime.datetime.today()
#     return datetime.datetime.combine(next_date,
#                               datetime.time(0, 0, 0, tzinfo=pytz.UTC))


@process_definition(name='systemprocess', 
                    id='systemprocess')
class SystemProcess(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(SystemProcess, self).__init__(**kwargs)
        self.title = _('System process')
        self.description = _('System process')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                #First loop
                pgblock1 = ParallelGatewayDefinition(),
                pgblock1sync = ParallelGatewayDefinition(),
                egblock1 = ExclusiveGatewayDefinition(),
                manage_users = ActivityDefinition(contexts=[DeactivateUsers],
                                       description=_("Deactivate users"),
                                       title=_("Deactivate users"),
                                       groups=[]),
                timerblock1 = IntermediateCatchEventDefinition(
                                 TimerEventDefinition(
                                   time_date=calculate_next_date_block1)),
                #Second loop
                # pgblock2 = ParallelGatewayDefinition(),
                # pgblock2sync = ParallelGatewayDefinition(),
                # egblock2 = ExclusiveGatewayDefinition(),
                # action2 = ActivityDefinition(contexts=[Action2],
                #                        description=_("actions2"),
                #                        title=_("actions2"),
                #                        groups=[]),
                # timerblock2 = IntermediateCatchEventDefinition(
                #                  TimerEventDefinition(
                #                    time_date=calculate_next_date_block2)),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                #First loop
                TransitionDefinition('pg', 'egblock1'),
                TransitionDefinition('egblock1', 'pgblock1'),
                TransitionDefinition('pgblock1', 'manage_users'),
                TransitionDefinition('manage_users', 'pgblock1sync'),
                TransitionDefinition('pgblock1sync', 'timerblock1'),
                TransitionDefinition('timerblock1', 'egblock1'),
                #Second loop
                # TransitionDefinition('pg', 'egblock2'),
                # TransitionDefinition('egblock2', 'pgblock2'),
                # TransitionDefinition('pgblock2', 'synchronizepublishsettings'),
                # TransitionDefinition('synchronizepublishsettings', 'pgblock2sync'),
                # TransitionDefinition('pgblock2sync', 'timerblock2'),
                # TransitionDefinition('timerblock2', 'egblock2'),
        )
