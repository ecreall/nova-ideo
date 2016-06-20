# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

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
    SelectEntity,
    DeselectEntity,
    AddDeadLine,
    EditDeadLine
    )
from novaideo import _


@process_definition(name='novaideoabstractprocess', id='novaideoabstractprocess')
class NovaIdeoAbstractProcess(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(NovaIdeoAbstractProcess, self).__init__(**kwargs)
        self.title = _('Abstract process')
        self.description = _('Abstract process')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                select = ActivityDefinition(contexts=[SelectEntity],
                                    description=_("Follow"),
                                    title=_("Follow"),
                                    groups=[]),
                deselect = ActivityDefinition(contexts=[DeselectEntity],
                                    description=_("Unfollow"),
                                    title=_("Unfollow"),
                                    groups=[]),
                adddeadline = ActivityDefinition(contexts=[AddDeadLine],
                                       description=_("Add the next deadline"),
                                       title=_("Add the next deadline"),
                                       groups=[_('Add')]),
                editdeadline = ActivityDefinition(contexts=[EditDeadLine],
                                       description=_("Edit the current deadline"),
                                       title=_("Edit the current deadline"),
                                       groups=[_('Edit')]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'select'),
                TransitionDefinition('select', 'eg'),
                TransitionDefinition('pg', 'deselect'),
                TransitionDefinition('deselect', 'eg'),
                TransitionDefinition('pg', 'adddeadline'),
                TransitionDefinition('adddeadline', 'eg'),
                TransitionDefinition('pg', 'editdeadline'),
                TransitionDefinition('editdeadline', 'eg'),
                TransitionDefinition('eg', 'end'),

        )
