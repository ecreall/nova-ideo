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
    AddOrganizations,
    CreatOrganizations,
    EditOrganizations,
    SeeOrganizations,
    EditOrganization,
    SeeOrganization)
from novaideo import _


@process_definition(name='organizationmanagement', id='organizationmanagement')
class OrganizationManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(OrganizationManagement, self).__init__(**kwargs)
        self.title = _('Orgaizations management')
        self.description = _('Orgaizations management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                add = ActivityDefinition(contexts=[AddOrganizations],
                                       description=_("Upload organizations from xl file"),
                                       title=_("Upload organizations"),
                                       groups=[_('Add')]),
                creat = ActivityDefinition(contexts=[CreatOrganizations],
                                       description=_("Creat organizations"),
                                       title=_("Creat organizations"),
                                       groups=[_('Add')]),
                edits = ActivityDefinition(contexts=[EditOrganizations],
                                       description=_("Edit organizations"),
                                       title=_("Edit organizations"),
                                       groups=[_('Edit')]),
                sees = ActivityDefinition(contexts=[SeeOrganizations],
                                       description=_("See organizations"),
                                       title=_("Organizations"),
                                       groups=[_('See')]),
                edit = ActivityDefinition(contexts=[EditOrganization],
                                       description=_("Edit organization"),
                                       title=_("Edit organizations"),
                                       groups=[_('Edit')]),
                see = ActivityDefinition(contexts=[SeeOrganization],
                                       description=_("See organization"),
                                       title=_("Details"),
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
