# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
"""
This module represent the Idea management process definition
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
    SeeConnectors,
    AddConnectors)
from novaideo import _


@process_definition(name='connectorsmanagement', id='connectorsmanagement')
class ConnectorsProcess(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(ConnectorsProcess, self).__init__(**kwargs)
        self.title = _('Connectors process')
        self.description = _('Connectors process')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                #egs = ExclusiveGatewayDefinition(),
                see = ActivityDefinition(contexts=[SeeConnectors],
                                       description=_("See all connectors"),
                                       title=_("Connectors"),
                                       groups=[_('See')]),
                add = ActivityDefinition(contexts=[AddConnectors],
                                       description=_("Add connectors"),
                                       title=_("Connectors"),
                                       groups=[_('Add')]),
                pg = ParallelGatewayDefinition(),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'see'),
                TransitionDefinition('see', 'eg'),
                TransitionDefinition('pg', 'add'),
                TransitionDefinition('add', 'eg'),
                TransitionDefinition('eg', 'end'),
        )
