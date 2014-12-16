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
    CreateFile,
    SeeFile,
    EditFile,
    AddDeadLine,
    EditDeadLine,
    SeeOrderedProposal
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
                                    description=_("Add to my selections"),
                                    title=_("Add to my selections"),
                                    groups=[]),
                deselect = ActivityDefinition(contexts=[DeselectEntity],
                                    description=_("Remove from my selections"),
                                    title=_("Remove from my selections"),
                                    groups=[]),
                creat = ActivityDefinition(contexts=[CreateFile],
                                       description=_("Create a file"),
                                       title=_("Create a file"),
                                       groups=[_('Add')]),
                editfile = ActivityDefinition(contexts=[EditFile],
                                       description=_("Edit the file"),
                                       title=_("Edit the file"),
                                       groups=[]),
                seefile = ActivityDefinition(contexts=[SeeFile],
                                       description=_("Details"),
                                       title=_("Details"),
                                       groups=[]),
                adddeadline = ActivityDefinition(contexts=[AddDeadLine],
                                       description=_("Add the next deadline"),
                                       title=_("Add the next deadline"),
                                       groups=[]),
                editdeadline = ActivityDefinition(contexts=[EditDeadLine],
                                       description=_("Edit the current deadline"),
                                       title=_("Edit the current deadline"),
                                       groups=[]),
                seeorderedproposal = ActivityDefinition(contexts=[SeeOrderedProposal],
                                       description=_("Proposals to examine"),
                                       title=_("Proposals to examine"),
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'select'),
                TransitionDefinition('select', 'eg'),
                TransitionDefinition('pg', 'creat'),
                TransitionDefinition('creat', 'eg'),
                TransitionDefinition('pg', 'seefile'),
                TransitionDefinition('seefile', 'eg'),
                TransitionDefinition('pg', 'editfile'),
                TransitionDefinition('editfile', 'eg'),
                TransitionDefinition('pg', 'deselect'),
                TransitionDefinition('deselect', 'eg'),
                TransitionDefinition('pg', 'adddeadline'),
                TransitionDefinition('adddeadline', 'eg'),
                TransitionDefinition('pg', 'editdeadline'),
                TransitionDefinition('editdeadline', 'eg'),
                TransitionDefinition('pg', 'seeorderedproposal'),
                TransitionDefinition('seeorderedproposal', 'eg'),
                TransitionDefinition('eg', 'end'),

        )
