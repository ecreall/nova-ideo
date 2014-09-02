from datetime import timedelta
from persistent.list import PersistentList

from dace.processdefinition.processdef import ProcessDefinition
from dace.util import getSite
from dace.processdefinition.activitydef import ActivityDefinition, SubProcessDefinition as OriginSubProcessDefinition
from dace.processdefinition.gatewaydef import (
    ExclusiveGatewayDefinition,
    ParallelGatewayDefinition)
from dace.processdefinition.transitiondef import TransitionDefinition
from dace.processdefinition.eventdef import (
    StartEventDefinition,
    EndEventDefinition,
    IntermediateCatchEventDefinition,
    TimerEventDefinition)
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
    VotingPublication,
    Withdraw,
    Resign,
    Participate,
    SubmitProposal,
    VotingAmendments,
    AmendmentsResult,
    Amendable,
    AmendmentsResult)
from novaideo import _
from novaideo.content.ballot import Ballot


vp_default_duration = timedelta(minutes=30)


amendments_default_duration = timedelta(minutes=30)



def amendments_duration(process):
    return amendments_default_duration


def eg3_publish_condition(process):
    report = process.vp_ballot.report
    if hasattr(process, 'first_decision'):
        electeds = report.get_electeds()
        if electeds:
            return True
        else:
            return False

    voters_len = len(report.voters)
    electors_len = len(report.electors)
    if voters_len != electors_len:
        return False

    if report.result['False'] == 0:
        return True

    return False


def eg3_amendable_condition(process):
    return not eg3_publish_condition(process)


class SubProcessDefinition(OriginSubProcessDefinition):

    
    def _init_subprocess(self, process, subprocess):

        root = getSite()
        proposal = process.execution_context.created_entity('proposal')
        electors = proposal.working_group.members[:root.participants_mini]
        if hasattr(process, 'first_decision'):
            electors = proposal.working_group.members

        subjects = [proposal]
        ballot = Ballot('Referendum' , electors, subjects, vp_default_duration)
        #TODO add ballot informations
        processes = ballot.run_ballot()
        subprocess.execution_context.add_involved_collection('vote_processes', processes)
        proposal.working_group.addtoproperty('ballots', ballot)
        subprocess.ballots = PersistentList()
        subprocess.ballots.append(ballot)
        subprocess.duration = vp_default_duration
        process.vp_ballot = ballot #vp for voting for publishing


class SubProcessDefinitionAmendments(OriginSubProcessDefinition):

    
    def _init_subprocess(self, process, subprocess):
        root = getSite()
        proposal = process.execution_context.created_entity('proposal')
        electors = proposal.working_group.members
        subjects = proposal.amendments
        processes = []
        #TODO calcul des groups d'amendements. Pour chaque groupe creer un ballot de type Jugement Majoritaire
        #TODO Start For
        ballot = Ballot('Referendum' , electors, subjects, amendments_default_duration)
        #TODO add ballot informations
        processes.extend(ballot.run_ballot())
        proposal.working_group.addtoproperty('ballots', ballot)
        subprocess.ballots = PersistentList()
        subprocess.ballots.append(ballot)
        process.amendments_ballots = PersistentList()
        process.amendments_ballots.append(ballot)
        #TODO End For
        subprocess.execution_context.add_involved_collection('vote_processes', processes)
        subprocess.duration = amendments_default_duration


@process_definition(name='proposalmanagement', id='proposalmanagement')
class ProposalManagement(ProcessDefinition, VisualisableElement):

    def __init__(self, **kwargs):
        super(ProposalManagement, self).__init__(**kwargs)
        self.title = _('Proposals management')
        self.description = _('Proposals management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
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
                votingpublication = SubProcessDefinition(pd='ballotprocess', contexts=[VotingPublication],
                                       description=_("Start voting for publication"),
                                       title=_("Start voting for publication"),
                                       groups=[]),
                votingamendments = SubProcessDefinitionAmendments(pd='ballotprocess', contexts=[VotingAmendments],
                                       description=_("Start voting for amendments"),
                                       title=_("Start voting for amendments"),
                                       groups=[]),
                amendable = ActivityDefinition(contexts=[Amendable],
                                       description=_("Change the state to amendable"),
                                       title=_("Amendable"),
                                       groups=[]),
                timer = IntermediateCatchEventDefinition(TimerEventDefinition(time_duration=amendments_duration)),
                publish = ActivityDefinition(contexts=[PublishProposal],
                                       description=_("Publish the proposal"),
                                       title=_("Publish"),
                                       groups=[]),
                amendmentsresult = ActivityDefinition(contexts=[AmendmentsResult],
                                       description=_("Amendments result"),
                                       title=_("Amendments result"),
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
                TransitionDefinition('pg3', 'participate'),
                TransitionDefinition('pg3', 'correct'),
                TransitionDefinition('pg3', 'improve'),
                TransitionDefinition('pg3', 'eg2'),
                TransitionDefinition('eg2', 'votingpublication'),
                TransitionDefinition('votingpublication', 'eg3'),
                TransitionDefinition('eg3', 'amendable', eg3_amendable_condition),
                TransitionDefinition('eg3', 'publish', eg3_publish_condition),
                TransitionDefinition('amendable', 'timer'),
                TransitionDefinition('timer', 'votingamendments'),
                TransitionDefinition('votingamendments', 'amendmentsresult'),
                TransitionDefinition('amendmentsresult', 'eg2'),
                TransitionDefinition('publish', 'end'),
        )
