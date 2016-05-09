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
    SendNewsLetter,
    DeactivateUsers,
    INACTIVITY_DURATION,
    NEWSLETTER_DURATION
    )
from novaideo import _


def calculate_next_date_newsletter(process):
    next_date = datetime.timedelta(days=NEWSLETTER_DURATION) + \
        datetime.datetime.now(tz=pytz.UTC)
    return datetime.datetime.combine(
        next_date,
        datetime.time(0, 0, 0, tzinfo=pytz.UTC))


def calculate_next_date_block1(process):
    next_date = datetime.timedelta(days=INACTIVITY_DURATION) + \
        datetime.datetime.today()
    return datetime.datetime.combine(
        next_date, datetime.time(0, 0, 0, tzinfo=pytz.UTC))


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
                #Newsletter loop
                nl_egblock = ExclusiveGatewayDefinition(),
                send_newsletter = ActivityDefinition(contexts=[SendNewsLetter],
                                       description=_("News letter"),
                                       title=_("News letter"),
                                       groups=[]),
                timernewsletter = IntermediateCatchEventDefinition(
                                 TimerEventDefinition(
                                   time_date=calculate_next_date_newsletter)),
                #First loop
                egblock1 = ExclusiveGatewayDefinition(),
                manage_users = ActivityDefinition(contexts=[DeactivateUsers],
                                       description=_("Deactivate users"),
                                       title=_("Deactivate users"),
                                       groups=[]),
                timerblock1 = IntermediateCatchEventDefinition(
                                 TimerEventDefinition(
                                   time_date=calculate_next_date_block1)),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                #Newsletter loop
                TransitionDefinition('pg', 'nl_egblock'),
                TransitionDefinition('nl_egblock', 'send_newsletter'),
                TransitionDefinition('send_newsletter', 'timernewsletter'),
                TransitionDefinition('timernewsletter', 'nl_egblock'),
                #First loop
                TransitionDefinition('pg', 'egblock1'),
                TransitionDefinition('egblock1', 'manage_users'),
                TransitionDefinition('manage_users', 'timerblock1'),
                TransitionDefinition('timerblock1', 'egblock1'),
        )
