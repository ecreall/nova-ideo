# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
"""
This module represent the Channel management process definition
powered by the dace engine. This process is unique, which means that
this process is instantiated only once.
"""
from dace.processdefinition.processdef import ProcessDefinition
from dace.processdefinition.activitydef import ActivityDefinition
from dace.processdefinition.gatewaydef import (
    ExclusiveGatewayDefinition,
    ParallelGatewayDefinition)
from dace.processdefinition.transitiondef import TransitionDefinition
from dace.processdefinition.eventdef import (
    StartEventDefinition,
    EndEventDefinition)
from dace.objectofcollaboration.services.processdef_container import (
    process_definition)
from pontus.core import VisualisableElement

from .behaviors import (
    Subscribe,
    Unsubscribe)
from novaideo import _


@process_definition(name='channelmanagement', id='channelmanagement')
class ChannelManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(ChannelManagement, self).__init__(**kwargs)
        self.title = _('Channel management')
        self.description = _('Channel management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                subscribe = ActivityDefinition(contexts=[Subscribe],
                                       description=_("Subscribe to the discussion"),
                                       title=_("Subscribe"),
                                       groups=[]),
                unsubscribe = ActivityDefinition(contexts=[Unsubscribe],
                                       description=_("Unsubscribe from the discussion"),
                                       title=_("Unsubscribe", context="channel"),
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'subscribe'),
                TransitionDefinition('subscribe', 'eg'),
                TransitionDefinition('pg', 'unsubscribe'),
                TransitionDefinition('unsubscribe', 'eg'),
                TransitionDefinition('eg', 'end'),
        )
