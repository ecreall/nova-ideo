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
    AddOrganizations,
    CreatOrganizations,
    EditOrganizations,
    SeeOrganizations,
    EditOrganization,
    SeeOrganization)


@process_definition(name='organizationmanagement', id='organizationmanagement')
class OrganizationManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(OrganizationManagement, self).__init__(**kwargs)
        self.title = 'Orgaizations management'
        self.description = 'Orgaizations management'

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                add = ActivityDefinition(contexts=[AddOrganizations],
                                       description="Upload organizations from xl file",
                                       title="Upload organizations",
                                       groups=['Add', 'Organization']),
                creat = ActivityDefinition(contexts=[CreatOrganizations],
                                       description="Creat organizations",
                                       title="Creat organizations",
                                       groups=['Add','Organization']),
                edits = ActivityDefinition(contexts=[EditOrganizations],
                                       description="Edit organizations",
                                       title="Edit organizations",
                                       groups=[]),
                sees = ActivityDefinition(contexts=[SeeOrganizations],
                                       description="See organizations",
                                       title="Organizations",
                                       groups=[]),
                edit = ActivityDefinition(contexts=[EditOrganization],
                                       description="Edit organization",
                                       title="Edit organizations",
                                       groups=[]),
                see = ActivityDefinition(contexts=[SeeOrganization],
                                       description="See organization",
                                       title="Details",
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'add'),
                TransitionDefinition('pg', 'creat'),
                TransitionDefinition('pg', 'see'),
                TransitionDefinition('pg', 'edit'),
                TransitionDefinition('add', 'eg'),
                TransitionDefinition('pg', 'edits'),
                TransitionDefinition('edits', 'eg'),
                TransitionDefinition('pg', 'sees'),
                TransitionDefinition('sees', 'eg'),
                TransitionDefinition('creat', 'eg'),
                TransitionDefinition('edit', 'eg'),
                TransitionDefinition('see', 'eg'),
                TransitionDefinition('eg', 'end'),
        )


