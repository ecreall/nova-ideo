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
    CreateProposal,
    DuplicateProposal,
    EditProposal,
    PublishProposal,
    CommentProposal,
    PresentProposal,
    Associate,
    ImproveProposal,
    CorrectProposal,
    FirstPublishDecision,
    Withdraw,
    Resign,
    Participate,
    SubmitProposal)
from novaideo import _


def eg3_publish_condition(process):
    vote_number = getattr(process, 'vote_number', 0)
    if vote_number == 3:
        return True

    return False

def eg3_pg5_condition(process):
    return not eg3_publish_condition(process)

@process_definition(name='proposalmanagement', id='proposalmanagement')
class ProposalManagement(ProcessDefinition, VisualisableElement):

    def __init__(self, **kwargs):
        super(ProposalManagement, self).__init__(**kwargs)
        self.title = _('Proposals management')
        self.description = _('Proposals management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                #egs = ExclusiveGatewayDefinition(),
                eg0 = ExclusiveGatewayDefinition(),
                pg2 = ParallelGatewayDefinition(),
                pg3 = ParallelGatewayDefinition(),
                pg4 = ParallelGatewayDefinition(),
                pg5 = ParallelGatewayDefinition(),
                eg1 = ExclusiveGatewayDefinition(),
                eg2 = ExclusiveGatewayDefinition(),
                eg3 = ExclusiveGatewayDefinition(),
                creat = ActivityDefinition(contexts=[CreateProposal],
                                       description=_("Create a new proposal"),
                                       title=_("Create a proposal"),
                                       groups=[_('Add')]),
                duplicate = ActivityDefinition(contexts=[DuplicateProposal],
                                       description=_("Duplicate this proposal"),
                                       title=_("Duplicate"),
                                       groups=[]),
                submit = ActivityDefinition(contexts=[SubmitProposal],
                                       description=_("Submit the proposal"),
                                       title=_("Submit"),
                                       groups=[]),
                edit = ActivityDefinition(contexts=[EditProposal],
                                       description=_("Edit the proposal"),
                                       title=_("Edit"),
                                       groups=[]),

                participate = ActivityDefinition(contexts=[Participate],
                                       description=_("Participate"),
                                       title=_("Participate"),
                                       groups=[]),
                resign = ActivityDefinition(contexts=[Resign],
                                       description=_("Resign"),
                                       title=_("Resign"),
                                       groups=[]),
                withdraw = ActivityDefinition(contexts=[Withdraw],
                                       description=_("Withdraw from the wating list"),
                                       title=_("Withdraw"),
                                       groups=[]),
                firstpublishdecision = ActivityDefinition(contexts=[FirstPublishDecision],
                                       description=_("Publish decision"),
                                       title=_("Publish"),
                                       groups=[]),

                publish = ActivityDefinition(contexts=[PublishProposal],
                                       description=_("Publish the proposal"),
                                       title=_("Publish"),
                                       groups=[]),
                present = ActivityDefinition(contexts=[PresentProposal],
                                       description=_("Present the proposal"),
                                       title=_("Present"),
                                       groups=[]),
                comment = ActivityDefinition(contexts=[CommentProposal],
                                       description=_("Comment the proposal"),
                                       title=_("Comment"),
                                       groups=[]),
                associate = ActivityDefinition(contexts=[Associate],
                                       description=_("Associate the proposal"),
                                       title=_("Associate"),
                                       groups=[]),
                correct = ActivityDefinition(contexts=[CorrectProposal],
                                       description=_("Correct proposal"),
                                       title=_("Correct"),
                                       groups=[]),

                improve = ActivityDefinition(contexts=[ImproveProposal],
                                       description=_("Improve proposal"),
                                       title=_("Improve"),
                                       groups=[]),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'eg0'),
                TransitionDefinition('eg0', 'creat'),
                TransitionDefinition('eg0', 'duplicate'),
                TransitionDefinition('creat', 'eg1'),
                TransitionDefinition('duplicate', 'eg1'),
                TransitionDefinition('eg1', 'pg2'),
                TransitionDefinition('pg2', 'submit'),
                TransitionDefinition('pg2', 'edit'),
                TransitionDefinition('submit', 'pg3'),
                TransitionDefinition('pg3', 'comment'),
                TransitionDefinition('pg3', 'associate'),
                TransitionDefinition('pg3', 'present'),
                TransitionDefinition('pg3', 'resign'),
                TransitionDefinition('pg3', 'eg2'),
                TransitionDefinition('eg2', 'participate'),
                TransitionDefinition('participate', 'pg4'),
                TransitionDefinition('pg4', 'eg2'),
                TransitionDefinition('pg4', 'firstpublishdecision'),
                TransitionDefinition('firstpublishdecision', 'eg3'),
                TransitionDefinition('eg3', 'publish', eg3_publish_condition),
                TransitionDefinition('eg3', 'pg5', eg3_pg5_condition),
                TransitionDefinition('pg5', 'correct'),
                TransitionDefinition('pg5', 'improve'),
                TransitionDefinition('publish', 'end'),
        )
