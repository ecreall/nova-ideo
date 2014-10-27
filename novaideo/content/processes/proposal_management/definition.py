import datetime
from persistent.list import PersistentList
from pyramid.threadlocal import get_current_registry

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
    EditAmendments,
    AddParagraph,
    Alert,
    CorrectItem,
    PublishAsProposal,
#    AddIdeas,
    SupportProposal,
    OpposeProposal,
    WithdrawToken,
#    DelIdeas,
    SeeRelatedIdeas,
    ProofreadingDone,
    CompareProposal
    )
from novaideo import _
from novaideo.content.ballot import Ballot
from novaideo.utilities.text_analyzer import ITextAnalyzer


vote_publishing_message =_("Vote for publishing.")

vote_duration_message =_("Voting results may not be known until the end of the period for voting. In the case where the majority are for the continuation of improvements of the proposal, your vote for the duration of the amendment period will be useful.")

vote_reopening_message =_("Voting results may not be known until the end of the period for voting. In the case where the majority are for the continuation of improvements of the proposal, your vote for reopening working group will be useful.")

vote_amendments_message =_("Vote for amendments.")

vp_default_duration = datetime.timedelta(minutes=30)

amendments_cycle_default_duration = {"Three minutes": datetime.timedelta(minutes=3),#pour les testes
                                     "Three days": datetime.timedelta(days=3),
                                     "One week": datetime.timedelta(weeks=1),
                                     "Two weeks": datetime.timedelta(weeks=2)}

amendments_vote_default_duration = datetime.timedelta(minutes=30) #TODO



def amendments_cycle_duration(process):
    duration_ballot = getattr(process, 'duration_configuration_ballot', None)
    if duration_ballot is not None:
        electeds = duration_ballot.report.get_electeds()
        if electeds:
            return amendments_cycle_default_duration[electeds[0]]+datetime.datetime.today()

    return amendments_cycle_default_duration["One week"]+datetime.datetime.today()


def eg3_publish_condition(process):
    report = process.vp_ballot.report
    if not getattr(process, 'first_decision', True):
        electeds = report.get_electeds()
        if electeds:
            return True
        else:
            return False

    voters_len = len(report.voters)
    electors_len = len(report.electors)
    if voters_len != electors_len:
        return False

    report.calculate_votes()
    if report.result['False'] == 0:
        return True

    return False


def eg3_amendable_condition(process):
    return not eg3_publish_condition(process)


def eg4_votingamendments_condition(process):
    proposal = process.execution_context.created_entity('proposal')
    if [a for a in proposal.amendments if 'published' in a.state]:
        return True

    return False


def eg4_alert_condition(process):
    return not eg4_votingamendments_condition(process)



class SubProcessDefinition(OriginSubProcessDefinition):


    def _init_subprocess(self, process, subprocess):
        root = getSite()
        proposal = process.execution_context.created_entity('proposal')
        wg = proposal.working_group
        electors = wg.members[:root.participants_mini]
        if not getattr(process, 'first_decision', True):
            electors = wg.members

        subjects = [proposal]
        ballot = Ballot('Referendum' , electors, subjects, vp_default_duration)
        ballot.report.description = vote_publishing_message
        ballot.title = _("Publish the proposal")
        #TODO add ballot informations
        processes = ballot.run_ballot()
        wg.addtoproperty('ballots', ballot)
        subprocess.ballots = PersistentList()
        subprocess.ballots.append(ballot)
        process.vp_ballot = ballot #vp for voting for publishing

        if not getattr(process, 'first_decision', True):
            #@TODO Lancement du vote sur reouverture
            subjects = [wg]
            ballot = Ballot('Referendum' , electors, subjects, vp_default_duration)
            ballot.report.description = vote_reopening_message
            ballot.title = 'Reopening working group'
            #TODO add ballot informations
            processes.extend(ballot.run_ballot(context=proposal))
            wg.addtoproperty('ballots', ballot)
            subprocess.ballots.append(ballot)
            process.reopening_configuration_ballot = ballot

        if len(wg.members) <= root.participants_maxi:
            group = list(amendments_cycle_default_duration.keys())#@TODO Durees
            ballot = Ballot('FPTP' , electors, group, vp_default_duration)
            ballot.title = _('Amendment duration')
            ballot.report.description = vote_duration_message
            #TODO add ballot informations
            processes.extend(ballot.run_ballot(context=proposal))
            wg.addtoproperty('ballots', ballot)
            subprocess.ballots.append(ballot)
            process.duration_configuration_ballot = ballot

        subprocess.execution_context.add_involved_collection('vote_processes', processes)
        subprocess.duration = vp_default_duration


class SubProcessDefinitionAmendments(OriginSubProcessDefinition):

    def _get_commun_groups(self, amendment, groups):
        result = []
        for group in groups:
            if amendment in group:
                result.append(group)

        return result

    def _contains_any(self, list1, list2):
        for e in list1:
            if e in list2:
                return True

        return False

    def _init_subprocess(self, process, subprocess):
        root = getSite()
        proposal = process.execution_context.created_entity('proposal')
        electors = proposal.working_group.members
        amendments = [a for a in proposal.amendments if 'published' in a.state]
        processes = []
        text_analyzer = get_current_registry().getUtility(ITextAnalyzer,'text_analyzer')
        groups = []
        for amendment in amendments:
            isadded = False
            related_ideas_amendment = list(amendment.edited_ideas)
            related_ideas_amendment.extend(list(amendment.removed_ideas))
            related_ideas_amendment = list(set(related_ideas_amendment))
            for group in groups:
                for a in group:
                    related_ideas_a = list(a.edited_ideas)
                    related_ideas_a.extend(list(a.removed_ideas))
                    related_ideas_a = list(set(related_ideas_a))
                    if text_analyzer.has_conflict(a.text, [amendment.text]) or \
                       (related_ideas_amendment and self._contains_any(related_ideas_amendment, related_ideas_a)):
                        group.append(amendment)
                        isadded = True

                    if isadded:
                        break

            if not isadded:
                groups.append([amendment])

        for amendment in amendments:
            commungroups = self._get_commun_groups(amendment, groups)
            new_group = set()
            for g in commungroups:
                new_group.update(g)
                groups.pop(groups.index(g))

            groups.append(list(new_group))

        for group in groups:
            group.insert(0, proposal)

        #TODO calcul des groups d'amendements. Pour chaque groupe creer un ballot de type Jugement Majoritaire
        #TODO Start For
        subprocess.ballots = PersistentList()
        process.amendments_ballots = PersistentList()
        i = 1
        for group in groups:
            ballot = Ballot('MajorityJudgment' , electors, group, amendments_vote_default_duration)
            ballot.report.description = vote_amendments_message
            ballot.title = _('Group of independent amendments')+ '('+str(i)+')'
            #TODO add ballot informations
            processes.extend(ballot.run_ballot(context=proposal))
            proposal.working_group.addtoproperty('ballots', ballot)
            subprocess.ballots.append(ballot)
            process.amendments_ballots.append(ballot)
            i += 1
        #TODO End For
        subprocess.execution_context.add_involved_collection('vote_processes', processes)
        subprocess.duration = amendments_vote_default_duration




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
                alert = ActivityDefinition(contexts=[Alert],
                                       description=_("Alert"),
                                       title=_("Alert"),
                                       groups=[]),
                amendable = ActivityDefinition(contexts=[Amendable],
                                       description=_("Change the state to amendable"),
                                       title=_("Amendable"),
                                       groups=[]),
                timer = IntermediateCatchEventDefinition(TimerEventDefinition(time_date=amendments_cycle_duration)),
                publish = ActivityDefinition(contexts=[PublishProposal],
                                       description=_("Publish the proposal"),
                                       title=_("Publish"),
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
                                       description=_("Present the proposal"),
                                       title=_("Present"),
                                       groups=[]),
                comment = ActivityDefinition(contexts=[CommentProposal],
                                       description=_("Comment the proposal"),
                                       title=_("Comment"),
                                       groups=[]),
                editamendments = ActivityDefinition(contexts=[EditAmendments],
                                       description=_("Edit amendments"),
                                       title=_("Edit amendments"),
                                       groups=[]),
                associate = ActivityDefinition(contexts=[Associate],
                                       description=_("Associate the proposal"),
                                       title=_("Associate"),
                                       groups=[]),
                seerelatedideas = ActivityDefinition(contexts=[SeeRelatedIdeas],
                                       description=_("Related ideas"),
                                       title=_("Related ideas"),
                                       groups=[]),
#                addideas = ActivityDefinition(contexts=[AddIdeas],
#                                       description=_("Add an idea to the proposal"),
#                                       title=_("Add an idea"),
#                                       groups=[]),
#                delideas = ActivityDefinition(contexts=[DelIdeas],
#                                       description=_("Remove an idea from the proposal"),
#                                       title=_("Remove an idea"),
#                                       groups=[]),
                correct = ActivityDefinition(contexts=[CorrectProposal],
                                       description=_("Correct proposal"),
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
                                       description=_("Improve proposal"),
                                       title=_("Improve"),
                                       groups=[]),
                compare = ActivityDefinition(contexts=[CompareProposal],
                                       description=_("Compare"),
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
#                TransitionDefinition('pg2', 'addideas'),
#                TransitionDefinition('pg2', 'delideas'),
                TransitionDefinition('pg2', 'seerelatedideas'),
                TransitionDefinition('submit', 'pg3'),
                TransitionDefinition('pg3', 'comment'),
                TransitionDefinition('pg3', 'compare'),
                TransitionDefinition('pg3', 'editamendments'),
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
                #TransitionDefinition('publish', 'end'),
        )
