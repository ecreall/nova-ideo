# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
"""
This module represent the Correlation management process definition 
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

from .behaviors import CommentCorrelation, SeeCorrelation
from novaideo import _


@process_definition(name='correlationmanagement', id='correlationmanagement')
class CorrelationManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(CorrelationManagement, self).__init__(**kwargs)
        self.title = _('correlation management')
        self.description = _('correlation management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                comment = ActivityDefinition(contexts=[CommentCorrelation],
                                       description=_("Comment"),
                                       title=_("Comment"),
                                       groups=[]),
                see = ActivityDefinition(contexts=[SeeCorrelation],
                                       description=_("Detail"),
                                       title=_("Detail"),
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'comment'),
                TransitionDefinition('comment', 'eg'),
                TransitionDefinition('pg', 'see'),
                TransitionDefinition('see', 'eg'),
                TransitionDefinition('eg', 'end'),
        )