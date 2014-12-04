# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
"""
This module represent the Proposal management process definition 
powered by the dace engine.
"""
import datetime
from persistent.list import PersistentList
from pyramid.threadlocal import get_current_registry

from dace.processdefinition.processdef import ProcessDefinition
from dace.util import getSite
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
    AMENDMENTS_CYCLE_DEFAULT_DURATION,
    calculate_amendments_cycle_duration
    )
from novaideo import _
from novaideo.content.ballot import Ballot
from novaideo.utilities.text_analyzer import ITextAnalyzer


VOTE_PUBLISHING_MESSAGE = _("Vote for submission")


VOTE_DURATION_MESSAGE = _("Voting results may not be known until the end of"
                          " the period for voting. In the case where the"
                          " majority are for the continuation of improvements"
                          " of the proposal, your vote for the duration of the"
                          " amendment period will be useful")


VOTE_REOPENING_MESSAGE = _("Voting results may not be known until the end of"
                           " the period for voting. In the case where the"
                           " majority are for the continuation of improvements"
                           " of the proposal, your vote for reopening working"
                           " group will be useful")


VOTE_AMENDMENTS_MESSAGE = _("Vote for amendments")


VP_DEFAULT_DURATION = datetime.timedelta(days=1)


AMENDMENTS_VOTE_DEFAULT_DURATION = datetime.timedelta(days=1)


def eg3_publish_condition(process):
    report = process.vp_ballot.report
    if not getattr(process, 'first_decision', True):
        electeds = report.get_electeds()
        if electeds:
            return True
        else:
            return False

    if len(report.voters) != len(report.electors):
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


class SubProcessDefinition(OriginSubProcessDefinition):
    """Run the voting process for proposal publishing 
       and working group configuration"""

    def _init_subprocess(self, process, subprocess):
        root = getSite()
        proposal = process.execution_context.created_entity('proposal')
        wg = proposal.working_group
        electors = wg.members[:root.participants_mini]
        if not getattr(process, 'first_decision', True):
            electors = wg.members

        subjects = [proposal]
        ballot = Ballot('Referendum' , electors, subjects, VP_DEFAULT_DURATION)
        ballot.report.description = VOTE_PUBLISHING_MESSAGE
        ballot.title = _("Submit the proposal")
        processes = ballot.run_ballot()
        wg.addtoproperty('ballots', ballot)
        subprocess.ballots = PersistentList()
        subprocess.ballots.append(ballot)
        process.vp_ballot = ballot #vp for voting for publishing

        if not getattr(process, 'first_decision', True) and \
          'closed' in wg.state:
            subjects = [wg]
            ballot = Ballot('Referendum' , electors,
                            subjects, VP_DEFAULT_DURATION)
            ballot.report.description = VOTE_REOPENING_MESSAGE
            ballot.title = _('Reopening working group')
            processes.extend(ballot.run_ballot(context=proposal))
            wg.addtoproperty('ballots', ballot)
            subprocess.ballots.append(ballot)
            process.reopening_configuration_ballot = ballot

        if len(wg.members) <= root.participants_maxi:
            group = list(AMENDMENTS_CYCLE_DEFAULT_DURATION.keys())
            ballot = Ballot('FPTP' , electors, group, VP_DEFAULT_DURATION)
            ballot.title = _('Amendment duration')
            ballot.report.description = VOTE_DURATION_MESSAGE
            processes.extend(ballot.run_ballot(context=proposal))
            wg.addtoproperty('ballots', ballot)
            subprocess.ballots.append(ballot)
            process.duration_configuration_ballot = ballot

        subprocess.execution_context.add_involved_collection(
                                      'vote_processes', processes)
        subprocess.duration = VP_DEFAULT_DURATION


class SubProcessDefinitionAmendments(OriginSubProcessDefinition):
    """Run the voting process for amendments"""

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
            related_ideas_amendment = list(amendment.edited_ideas)
            related_ideas_amendment.extend(list(amendment.removed_ideas))
            related_ideas_amendment = list(set(related_ideas_amendment))
            for group in groups:
                for amt in group:
                    related_ideas_a = list(amt.edited_ideas)
                    related_ideas_a.extend(list(amt.removed_ideas))
                    related_ideas_a = list(set(related_ideas_a))
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
            ballot.report.description = VOTE_AMENDMENTS_MESSAGE
            ballot.title = _('Vote for amendments (group ${nbi})', 
                              mapping={'nbi': i})
            processes.extend(ballot.run_ballot(context=proposal))
            proposal.working_group.addtoproperty('ballots', ballot)
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
                TransitionDefinition('pg2', 'seerelatedideas'),
                TransitionDefinition('submit', 'pg3'),
                TransitionDefinition('pg3', 'comment'),
                TransitionDefinition('pg3', 'compare'),
                TransitionDefinition('pg3', 'seeamendments'),
                TransitionDefinition('pg2', 'associate'),
                TransitionDefinition('pg3', 'present'),
                TransitionDefinition('pg3', 'resign'),
                TransitionDefinition('pg3', 'participate'),
                TransitionDefinition('pg3', 'withdraw'),
                TransitionDefinition('pg3', 'correct'),
                TransitionDefinition('pg3', 'proofreading'),
                TransitionDefinition('pg3', 'correctitem'),
                TransitionDefinition('pg3', 'addparagraph'),
                TransitionDefinition('pg3', 'improve'),
                TransitionDefinition('pg3', 'eg2'),
                TransitionDefinition('eg2', 'votingpublication'),
                TransitionDefinition('votingpublication', 'eg3'),
                TransitionDefinition('eg3', 'amendable', eg3_amendable_condition),
                TransitionDefinition('eg3', 'publish', eg3_publish_condition),
                TransitionDefinition('publish', 'pg6'),
                TransitionDefinition('pg6', 'support'),
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
