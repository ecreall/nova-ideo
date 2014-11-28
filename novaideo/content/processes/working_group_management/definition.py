# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from dace.processdefinition.processdef import ProcessDefinition
from dace.processdefinition.activitydef import ActivityDefinition
from dace.processdefinition.transitiondef import TransitionDefinition
from dace.processdefinition.eventdef import (
    StartEventDefinition,
    EndEventDefinition)
from dace.objectofcollaboration.services.processdef_container import (
  process_definition)
from pontus.core import VisualisableElement

from .behaviors import EditAction


@process_definition(name='workinggroupmanagement', id='workinggroupmanagement')
class WorkingGroupManagement(ProcessDefinition, VisualisableElement):

    def __init__(self, **kwargs):
        super(WorkingGroupManagement, self).__init__(**kwargs)
        self.title = 'Processus de gestion des groupes de travail'
        self.description = 'Ce processus permet de gerer les groupes de travail'

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                edit = ActivityDefinition(contexts=[EditAction],
                                       description="L'action permet de...",
                                       title="Edit",
                                       groups=['Edit']),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'edit'),
                TransitionDefinition('edit', 'end'),
        )
