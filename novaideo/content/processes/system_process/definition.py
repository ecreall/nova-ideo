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
    DeactivateUsers,
    INACTIVITY_DURATION,
    INACTIVITY_ALERTS,
    Alert1Users,
    Alert2Users,
    Alert3Users,
    )
from novaideo import _


def calculate_next_date_block1(process):
    next_date = datetime.timedelta(days=INACTIVITY_DURATION) + \
                datetime.datetime.today()
    return datetime.datetime.combine(next_date,
                              datetime.time(0, 0, 0, tzinfo=pytz.UTC))


def calculate_next_date_block2(process):
    next_date = datetime.timedelta(days=INACTIVITY_ALERTS[0]) + \
                datetime.datetime.today()
    return datetime.datetime.combine(next_date,
                              datetime.time(0, 0, 0, tzinfo=pytz.UTC))


def calculate_next_date_block3(process):
    next_date = datetime.timedelta(days=INACTIVITY_ALERTS[1]) + \
                datetime.datetime.today()
    return datetime.datetime.combine(next_date,
                              datetime.time(0, 0, 0, tzinfo=pytz.UTC))


def calculate_next_date_block4(process):
    next_date = datetime.timedelta(days=INACTIVITY_ALERTS[2]) + \
                datetime.datetime.today()
    return datetime.datetime.combine(next_date,
                              datetime.time(0, 0, 0, tzinfo=pytz.UTC))


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
                egblock1 = ExclusiveGatewayDefinition(),
                manage_users = ActivityDefinition(contexts=[DeactivateUsers],
                                       description=_("Deactivate users"),
                                       title=_("Deactivate users"),
                                       groups=[]),
                timerblock1 = IntermediateCatchEventDefinition(
                                 TimerEventDefinition(
                                   time_date=calculate_next_date_block1)),
                #Loop 2
                egblock2 = ExclusiveGatewayDefinition(),
                alert1_users = ActivityDefinition(contexts=[Alert1Users],
                                       description=_("Alert users"),
                                       title=_("Alert users"),
                                       groups=[]),
                timerblock2 = IntermediateCatchEventDefinition(
                                 TimerEventDefinition(
                                   time_date=calculate_next_date_block2)),
                #Loop 3
                egblock3 = ExclusiveGatewayDefinition(),
                alert2_users = ActivityDefinition(contexts=[Alert2Users],
                                       description=_("Alert users"),
                                       title=_("Alert users"),
                                       groups=[]),
                timerblock3 = IntermediateCatchEventDefinition(
                                 TimerEventDefinition(
                                   time_date=calculate_next_date_block3)),
                #Loop 4
                egblock4 = ExclusiveGatewayDefinition(),
                alert3_users = ActivityDefinition(contexts=[Alert3Users],
                                       description=_("Alert users"),
                                       title=_("Alert users"),
                                       groups=[]),
                timerblock4 = IntermediateCatchEventDefinition(
                                 TimerEventDefinition(
                                   time_date=calculate_next_date_block4)),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                #First loop
                TransitionDefinition('pg', 'egblock1'),
                TransitionDefinition('egblock1', 'manage_users'),
                TransitionDefinition('manage_users', 'timerblock1'),
                TransitionDefinition('timerblock1', 'egblock1'),
                #Loop 2
                TransitionDefinition('pg', 'egblock2'),
                TransitionDefinition('egblock2', 'alert1_users'),
                TransitionDefinition('alert1_users', 'timerblock2'),
                TransitionDefinition('timerblock2', 'egblock2'),
                #Loop 3
                TransitionDefinition('pg', 'egblock3'),
                TransitionDefinition('egblock3', 'alert2_users'),
                TransitionDefinition('alert2_users', 'timerblock3'),
                TransitionDefinition('timerblock3', 'egblock3'),
                #Loop 4
                TransitionDefinition('pg', 'egblock4'),
                TransitionDefinition('egblock4', 'alert3_users'),
                TransitionDefinition('alert3_users', 'timerblock4'),
                TransitionDefinition('timerblock4', 'egblock4')
        )
