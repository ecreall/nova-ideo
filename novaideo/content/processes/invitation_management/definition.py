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
from dace.objectofcollaboration.services.processdef_container import process_definition
from pontus.core import VisualisableElement

from .behaviors import (
    InviteUsers,
    UploadUsers,
    SeeInvitation,
    SeeInvitations,
    EditInvitations,
    EditInvitation,
    AcceptInvitation,
    RefuseInvitation,
    RemoveInvitation,
    RemindInvitation,
    ReinviteUser)
from novaideo import _


@process_definition(name='invitationmanagement', id='invitationmanagement')
class InvitationManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(InvitationManagement, self).__init__(**kwargs)
        self.title = _('Invitations management')
        self.description = _('Invitations management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                add = ActivityDefinition(contexts=[UploadUsers],
                                       description="Upload users from xl file",
                                       title="Upload users",
                                       groups=['Invite']),
                invite = ActivityDefinition(contexts=[InviteUsers],
                                       description=_("Invite users"),
                                       title=_("Invite users"),
                                       groups=[_('Add')]),
                seeinvitation = ActivityDefinition(contexts=[SeeInvitation],
                                       description=_("See the invitation"),
                                       title=_("Details"),
                                       groups=[]),
                seeinvitations = ActivityDefinition(contexts=[SeeInvitations],
                                       description=_("See the invitations"),
                                       title=_("Invitations"),
                                       groups=[_('See')]),
                edits = ActivityDefinition(contexts=[EditInvitations],
                                       description=_("Edit invitations"),
                                       title=_("Edit invitations"),
                                       groups=[_('Edit')]),
                edit = ActivityDefinition(contexts=[EditInvitation],
                                       description=_("Edit the invitation"),
                                       title=_("Edit the invitation"),
                                       groups=[_('Edit')]),
                accept = ActivityDefinition(contexts=[AcceptInvitation],
                                       description=_("Accept the invitation"),
                                       title=_("Accept the invitation"),
                                       groups=[]),
                refuse = ActivityDefinition(contexts=[RefuseInvitation],
                                       description=_("Refuse the invitation"),
                                       title=_("Refuse the invitation"),
                                       groups=[]),
                remove = ActivityDefinition(contexts=[RemoveInvitation],
                                       description=_("Remove the invitation"),
                                       title=_("Remove the invitation"),
                                       groups=[]),
                reinvite = ActivityDefinition(contexts=[ReinviteUser],
                                       description=_("Re-invite the person"),
                                       title=_("Re-invite the person"),
                                       groups=[]),
                remind = ActivityDefinition(contexts=[RemindInvitation],
                                       description=_("Remind the person"),
                                       title=_("Remind the person"),
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'add'),
                TransitionDefinition('pg', 'invite'),
                TransitionDefinition('pg', 'edits'),
                TransitionDefinition('pg', 'edit'),
                TransitionDefinition('pg', 'seeinvitation'),
                TransitionDefinition('pg', 'seeinvitations'),
                TransitionDefinition('pg', 'accept'),
                TransitionDefinition('pg', 'refuse'),
                TransitionDefinition('pg', 'remove'),
                TransitionDefinition('pg', 'reinvite'),
                TransitionDefinition('pg', 'remind'),
                TransitionDefinition('accept', 'eg'),
                TransitionDefinition('refuse', 'eg'),
                TransitionDefinition('remove', 'eg'),
                TransitionDefinition('reinvite', 'eg'),
                TransitionDefinition('remind', 'eg'),
                TransitionDefinition('add', 'eg'),
                TransitionDefinition('seeinvitation', 'eg'),
                TransitionDefinition('seeinvitations', 'eg'),
                TransitionDefinition('invite', 'eg'),
                TransitionDefinition('edits', 'eg'),
                TransitionDefinition('edit', 'eg'),
                TransitionDefinition('eg', 'end'),
        )
