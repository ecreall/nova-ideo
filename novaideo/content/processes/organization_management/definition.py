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
    SeeOrganization,
    RemoveOrganization,
    AddMembers,
    RemoveMembers,
    UserEditOrganization,
    WithdrawUser
    )
from novaideo import _


@process_definition(name='organizationmanagement', id='organizationmanagement')
class OrganizationManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(OrganizationManagement, self).__init__(**kwargs)
        self.title = _('Organizations management')
        self.description = _('Organizations management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                add = ActivityDefinition(contexts=[AddOrganizations],
                                       description=_("Upload organizations from spreadsheet file"),
                                       title=_("Upload organizations"),
                                       groups=[_('Add')]),
                creat = ActivityDefinition(contexts=[CreatOrganizations],
                                       description=_("Create organizations"),
                                       title=_("Create organizations"),
                                       groups=[_('Add')]),
                edits = ActivityDefinition(contexts=[EditOrganizations],
                                       description=_("Edit organizations"),
                                       title=_("Edit organizations"),
                                       groups=[_('Edit')]),
                sees = ActivityDefinition(contexts=[SeeOrganizations],
                                       description=_("See organizations"),
                                       title=_("The Organizations"),
                                       groups=[_('See')]),
                edit = ActivityDefinition(contexts=[EditOrganization],
                                       description=_("Edit the organization"),
                                       title=_("Edit"),
                                       groups=[_('Edit')]),
                see = ActivityDefinition(contexts=[SeeOrganization],
                                       description=_("See organization"),
                                       title=_("Details"),
                                       groups=[]),
                remove = ActivityDefinition(contexts=[RemoveOrganization],
                                       description=_("Remove organization"),
                                       title=_("Remove"),
                                       groups=[]),
                add_members = ActivityDefinition(contexts=[AddMembers],
                                       description=_("Add Members"),
                                       title=_("Add Members"),
                                       groups=[]),
                remove_members = ActivityDefinition(contexts=[RemoveMembers],
                                       description=_("Remove Members"),
                                       title=_("Remove Members"),
                                       groups=[]),
                user_edit_organization = ActivityDefinition(contexts=[UserEditOrganization],
                                       description=_("Edit the organization"),
                                       title=_("Edit the organization"),
                                       groups=[]),
                withdraw_user = ActivityDefinition(contexts=[WithdrawUser],
                                       description=_("Withdraw from the organization"),
                                       title=_("Withdraw from the organization"),
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'add'),
                TransitionDefinition('pg', 'creat'),
                TransitionDefinition('pg', 'add_members'),
                TransitionDefinition('pg', 'remove_members'),
                TransitionDefinition('pg', 'user_edit_organization'),
                TransitionDefinition('pg', 'withdraw_user'),
                TransitionDefinition('pg', 'remove'),
                TransitionDefinition('pg', 'see'),
                TransitionDefinition('pg', 'edit'),
                TransitionDefinition('add', 'eg'),
                TransitionDefinition('pg', 'edits'),
                TransitionDefinition('edits', 'eg'),
                TransitionDefinition('pg', 'sees'),
                TransitionDefinition('sees', 'eg'),
                TransitionDefinition('creat', 'eg'),
                TransitionDefinition('add_members', 'eg'),
                TransitionDefinition('remove_members', 'eg'),
                TransitionDefinition('user_edit_organization', 'eg'),
                TransitionDefinition('withdraw_user', 'eg'),
                TransitionDefinition('remove', 'eg'),
                TransitionDefinition('edit', 'eg'),
                TransitionDefinition('see', 'eg'),
                TransitionDefinition('eg', 'end'),
        )
