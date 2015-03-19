# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
"""
This module represent the Proposal management process definition 
powered by the dace engine.
"""

from persistent.list import PersistentList
from pyramid.threadlocal import get_current_registry, get_current_request

from dace.processdefinition.processdef import ProcessDefinition
from dace.util import getSite
from dace.processinstance.activity import (
  SubProcess as OriginSubProcess)
from dace.processdefinition.activitydef import (
  ActivityDefinition, 
  SubProcessDefinition as OriginSubProcessDefinition)
from dace.processdefinition.gatewaydef import (
    ExclusiveGatewayDefinition,
    ParallelGatewayDefinition)
from dace.processdefinition.transitiondef import TransitionDefinition
from dace.processdefinition.eventdef import (
    StartEventDefinition,
    EndEventDefinition,
    IntermediateCatchEventDefinition,
    TimerEventDefinition)
from dace.objectofcollaboration.services.processdef_container import (
  process_definition)
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
    FirstParticipate,
    SubmitProposal,
    VotingAmendments,
    AmendmentsResult,
    Amendable,
    SeeAmendments,
    AddParagraph,
    Alert,
    CorrectItem,
    PublishAsProposal,
    SupportProposal,
    OpposeProposal,
    WithdrawToken,
    SeeRelatedIdeas,
    ProofreadingDone,
    CompareProposal,
    MakeOpinion,
    DeleteProposal,
    close_votes,
    AMENDMENTS_CYCLE_DEFAULT_DURATION,
    calculate_amendments_cycle_duration,
    VOTE_PUBLISHING_MESSAGE,
    VOTE_DURATION_MESSAGE,
    VOTE_REOPENING_MESSAGE, 
    VOTE_AMENDMENTS_MESSAGE, 
    VP_DEFAULT_DURATION, 
    AMENDMENTS_VOTE_DEFAULT_DURATION,
    )
from novaideo import _
from novaideo.content.ballot import Ballot
from novaideo.utilities.text_analyzer import ITextAnalyzer


def eg3_publish_condition(process):
    report = process.vp_ballot.report
    if not getattr(process, 'first_vote', True):
        electeds = report.get_electeds()
        if electeds:
            return True
        else:
            return False

    report.calculate_votes()
    if report.result['False'] == 0:
        return True

    return False


def eg3_amendable_condition(process):
    return not eg3_publish_condition(process)


def eg4_votingamendments_condition(process):
    proposal = process.execution_context.created_entity('proposal')
    if any('published' in a.state for a in proposal.amendments):
        return True

    return False


def eg4_alert_condition(process):
    return not eg4_votingamendments_condition(process)


class SubProcess(OriginSubProcess):

    def __init__(self, definition):
        super(SubProcess, self).__init__(definition)

    def stop(self):
        request = get_current_request()
        for process in self.sub_processes:
            exec_ctx = process.execution_context
            vote_processes = exec_ctx.get_involved_collection('vote_processes')
            vote_processes = [process for process in vote_processes \
                              if not process._finished]
            if vote_processes:
                close_votes(None, request, vote_processes)
            
        super(SubProcess, self).stop()


class SubProcessDefinition(OriginSubProcessDefinition):
    """Run the voting process for proposal publishing 
       and working group configuration"""

    factory = SubProcess

    def _init_subprocess(self, process, subprocess):
        if not hasattr(process, 'first_vote'):
            process.first_vote = True
            #TODO Terminer le process stoper le timer??
            #dt run vote processes
            return
        else:
            process.first_vote = False

        root = getSite()
        proposal = process.execution_context.created_entity('proposal')
        wg = proposal.working_group
        electors = wg.members[:root.participants_mini]
        if not getattr(process, 'first_decision', True):
            electors = wg.members

        subjects = [proposal]
        ballot = Ballot('Referendum' , electors, subjects, VP_DEFAULT_DURATION)
        wg.addtoproperty('ballots', ballot)
        ballot.report.description = VOTE_PUBLISHING_MESSAGE
        ballot.title = _("Submit the proposal")
        processes = ballot.run_ballot()
        subprocess.ballots = PersistentList()
        subprocess.ballots.append(ballot)
        process.vp_ballot = ballot #vp for voting for publishing

        if not getattr(process, 'first_decision', True) and \
          'closed' in wg.state:
            subjects = [wg]
            ballot = Ballot('Referendum' , electors,
                            subjects, VP_DEFAULT_DURATION)
            wg.addtoproperty('ballots', ballot)
            ballot.report.description = VOTE_REOPENING_MESSAGE
            ballot.title = _('Reopening working group')
            processes.extend(ballot.run_ballot(context=proposal))
            subprocess.ballots.append(ballot)
            process.reopening_configuration_ballot = ballot

        if len(wg.members) <= root.participants_maxi:
            durations = list(AMENDMENTS_CYCLE_DEFAULT_DURATION.keys())
            group = sorted(durations, 
                           key=lambda e: AMENDMENTS_CYCLE_DEFAULT_DURATION[e])
            ballot = Ballot('FPTP' , electors, group, VP_DEFAULT_DURATION)
            wg.addtoproperty('ballots', ballot)
            ballot.title = _('Amendment duration')
            ballot.report.description = VOTE_DURATION_MESSAGE
            processes.extend(ballot.run_ballot(context=proposal))
            subprocess.ballots.append(ballot)
            process.duration_configuration_ballot = ballot

        subprocess.execution_context.add_involved_collection(
                                      'vote_processes', processes)
        subprocess.duration = VP_DEFAULT_DURATION


class SubProcessDefinitionAmendments(OriginSubProcessDefinition):
    """Run the voting process for amendments"""

    factory = SubProcess

    def _init_subprocess(self, process, subprocess):
        proposal = process.execution_context.created_entity('proposal')
        electors = proposal.working_group.members
        amendments = [a for a in proposal.amendments if 'published' in a.state]
        processes = []
        text_analyzer = get_current_registry().getUtility(
                                                  ITextAnalyzer,
                                                  'text_analyzer')
        groups = []
        for amendment in amendments:
            isadded = False
            related_ideas_amendment = list(amendment.related_ideas)
            for group in groups:
                for amt in group:
                    related_ideas_a = list(amt.related_ideas)
                    if text_analyzer.has_conflict(amt.text, 
                                                  [amendment.text]) or \
                       (related_ideas_amendment and \
                        any(e in related_ideas_amendment \
                            for e in related_ideas_a)):
                        group.append(amendment)
                        isadded = True
                        break

            if not isadded:
                groups.append([amendment])

        for amendment in amendments:
            commungroups = [group for group in groups if amendment in group]
            new_group = set()
            for group in commungroups:
                new_group.update(group)
                groups.pop(groups.index(group))

            groups.append(list(new_group))

        for group in groups:
            group.insert(0, proposal)

        subprocess.ballots = PersistentList()
        process.amendments_ballots = PersistentList()
        i = 1
        for group in groups:
            ballot = Ballot('MajorityJudgment' , electors, 
                       group, AMENDMENTS_VOTE_DEFAULT_DURATION)
            proposal.working_group.addtoproperty('ballots', ballot)
            ballot.report.description = VOTE_AMENDMENTS_MESSAGE
            ballot.title = _('Vote for amendments (group ${nbi})', 
                              mapping={'nbi': i})
            processes.extend(ballot.run_ballot(context=proposal))
            subprocess.ballots.append(ballot)
            process.amendments_ballots.append(ballot)
            i += 1

        subprocess.execution_context.add_involved_collection(
                       'vote_processes', processes)
        subprocess.duration = AMENDMENTS_VOTE_DEFAULT_DURATION


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
                eg4 = ExclusiveGatewayDefinition(),
                pg6 = ParallelGatewayDefinition(),
                creat = ActivityDefinition(contexts=[CreateProposal],
                                       description=_("Create a new proposal"),
                                       title=_("Create a proposal"),
                                       groups=[_('Add')]),
                delete = ActivityDefinition(contexts=[DeleteProposal],
                                       description=_("Delete the proposal"),
                                       title=_("Delete"),
                                       groups=[]),
                publishasproposal = ActivityDefinition(contexts=[PublishAsProposal],
                                       description=_("Transform the idea as a proposal"),
                                       title=_("Transform as a proposal"),
                                       groups=[]),
                duplicate = ActivityDefinition(contexts=[DuplicateProposal],
                                       description=_("Duplicate this proposal"),
                                       title=_("Duplicate"),
                                       groups=[]),
                submit = ActivityDefinition(contexts=[SubmitProposal],
                                       description=_("Publish the proposal"),
                                       title=_("Publish"),
                                       groups=[]),
                edit = ActivityDefinition(contexts=[EditProposal],
                                       description=_("Edit the proposal"),
                                       title=_("Edit"),
                                       groups=[]),
                participate = ActivityDefinition(contexts=[Participate],
                                       description=_("Participate"),
                                       title=_("Participate"),
                                       groups=[]),
                firstparticipate = ActivityDefinition(contexts=[FirstParticipate],
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
                alert = ActivityDefinition(contexts=[Alert],
                                       description=_("Alert"),
                                       title=_("Alert"),
                                       groups=[]),
                amendable = ActivityDefinition(contexts=[Amendable],
                                       description=_("Change the state to amendable"),
                                       title=_("Amendable"),
                                       groups=[]),
                timer = IntermediateCatchEventDefinition(TimerEventDefinition(time_date=calculate_amendments_cycle_duration)),
                publish = ActivityDefinition(contexts=[PublishProposal],
                                       description=_("Submit the proposal"),
                                       title=_("Submit"),
                                       groups=[]),
                support = ActivityDefinition(contexts=[SupportProposal],
                                       description=_("Support the proposal"),
                                       title=_("Support"),
                                       groups=[]),
                makeitsopinion = ActivityDefinition(contexts=[MakeOpinion],
                                       description=_("Make its opinion"),
                                       title=_("Make its opinion"),
                                       groups=[]),
                oppose = ActivityDefinition(contexts=[OpposeProposal],
                                       description=_("To oppose a proposal"),
                                       title=_("Oppose"),
                                       groups=[]),
                withdraw_token = ActivityDefinition(contexts=[WithdrawToken],
                                       description=_("Withdraw token from proposal"),
                                       title=_("Withdraw my token"),
                                       groups=[]),
                amendmentsresult = ActivityDefinition(contexts=[AmendmentsResult],
                                       description=_("Amendments result"),
                                       title=_("Amendments result"),
                                       groups=[]),
                present = ActivityDefinition(contexts=[PresentProposal],
                                       description=_("Submit the proposal to others"),
                                       title=_("Submit to others"),
                                       groups=[]),
                comment = ActivityDefinition(contexts=[CommentProposal],
                                       description=_("Discuss the proposal"),
                                       title=_("Discuss"),
                                       groups=[]),
                seeamendments = ActivityDefinition(contexts=[SeeAmendments],
                                       description=_("Amendments"),
                                       title=_("Amendments"),
                                       groups=[]),
                associate = ActivityDefinition(contexts=[Associate],
                                       description=_("Associate the proposal"),
                                       title=_("Associate"),
                                       groups=[]),
                seerelatedideas = ActivityDefinition(contexts=[SeeRelatedIdeas],
                                       description=_("Related ideas"),
                                       title=_("Related ideas"),
                                       groups=[]),
                correct = ActivityDefinition(contexts=[CorrectProposal],
                                       description=_("Correct the proposal"),
                                       title=_("Correct"),
                                       groups=[]),
                correctitem = ActivityDefinition(contexts=[CorrectItem],
                                       description=_("Correct item"),
                                       title=_("Correct"),
                                       groups=[]),
                proofreading = ActivityDefinition(contexts=[ProofreadingDone],
                                       description=_("Proofreading done"),
                                       title=_("Proofreading done"),
                                       groups=[]),
                addparagraph = ActivityDefinition(contexts=[AddParagraph],
                                       description=_("Add a paragraph"),
                                       title=_("Add a paragraph"),
                                       groups=[]),
                improve = ActivityDefinition(contexts=[ImproveProposal],
                                       description=_("Improve the proposal"),
                                       title=_("Improve"),
                                       groups=[]),
                compare = ActivityDefinition(contexts=[CompareProposal],
                                       description=_("Compare versions"),
                                       title=_("Compare"),
                                       groups=[]),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'eg0'),
                TransitionDefinition('eg0', 'creat'),
                TransitionDefinition('eg0', 'publishasproposal'),
                TransitionDefinition('eg0', 'duplicate'),
                TransitionDefinition('creat', 'eg1'),
                TransitionDefinition('publishasproposal', 'eg1'),
                TransitionDefinition('duplicate', 'eg1'),
                TransitionDefinition('eg1', 'pg2'),
                TransitionDefinition('pg2', 'submit'),
                TransitionDefinition('pg2', 'edit'),
                TransitionDefinition('pg2', 'delete'),
                TransitionDefinition('delete', 'end'),
                TransitionDefinition('pg2', 'seerelatedideas'),
                TransitionDefinition('submit', 'pg3'),
                TransitionDefinition('pg3', 'comment'),
                TransitionDefinition('pg3', 'compare'),
                TransitionDefinition('pg3', 'seeamendments'),
                TransitionDefinition('pg2', 'associate'),
                TransitionDefinition('pg3', 'present'),
                TransitionDefinition('pg3', 'resign'),
                TransitionDefinition('pg3', 'participate'),
                TransitionDefinition('pg3', 'firstparticipate'),
                TransitionDefinition('pg3', 'withdraw'),
                TransitionDefinition('pg3', 'correct'),
                TransitionDefinition('pg3', 'proofreading'),
                TransitionDefinition('pg3', 'correctitem'),
                TransitionDefinition('pg3', 'addparagraph'),
                TransitionDefinition('pg3', 'improve'),
                TransitionDefinition('pg3', 'eg2'),
                TransitionDefinition('eg2', 'votingpublication'),
                TransitionDefinition('votingpublication', 'eg3'),
                TransitionDefinition('eg3', 'amendable', eg3_amendable_condition, sync=True),
                TransitionDefinition('eg3', 'publish', eg3_publish_condition, sync=True),
                TransitionDefinition('publish', 'pg6'),
                TransitionDefinition('pg6', 'support'),
                TransitionDefinition('pg6', 'makeitsopinion'),
                TransitionDefinition('pg6', 'oppose'),
                TransitionDefinition('pg6', 'withdraw_token'),
                TransitionDefinition('amendable', 'timer'),
                TransitionDefinition('timer', 'eg4'),
                TransitionDefinition('eg4', 'votingamendments', eg4_votingamendments_condition, sync=True),
                TransitionDefinition('eg4', 'alert', eg4_alert_condition, sync=True),
                TransitionDefinition('alert', 'eg2'),
                TransitionDefinition('votingamendments', 'amendmentsresult'),
                TransitionDefinition('amendmentsresult', 'eg2'),
        )
