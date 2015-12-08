# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
"""
This module represent the Proposal management process definition 
powered by the dace engine.
"""

from persistent.list import PersistentList
from pyramid.threadlocal import get_current_request

from dace.processdefinition.processdef import ProcessDefinition
from dace.util import getSite, find_service
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
    EndEventDefinition,)
from dace.objectofcollaboration.services.processdef_container import (
    process_definition)
from pontus.core import VisualisableElement

from .behaviors import (
    CreateProposal,
    SeeProposal,
    DuplicateProposal,
    EditProposal,
    PublishProposal,
    CommentProposal,
    PresentProposal,
    Associate,
    Work,
    VotingPublication,
    Withdraw,
    Resign,
    Participate,
    FirstParticipate,
    SubmitProposal,
    SeeAmendments,
    PublishAsProposal,
    SupportProposal,
    OpposeProposal,
    WithdrawToken,
    SeeRelatedIdeas,
    CompareProposal,
    MakeOpinion,
    DeleteProposal,
    close_votes,
    AMENDMENTS_CYCLE_DEFAULT_DURATION,
    VOTE_PUBLISHING_MESSAGE,
    VOTE_DURATION_MESSAGE,
    VOTE_REOPENING_MESSAGE,
    VP_DEFAULT_DURATION,
    VOTE_MODEWORK_MESSAGE,
    publish_condition
    )
from novaideo import _
from novaideo.content.ballot import Ballot


def amendable_condition(process):
    return not publish_condition(process)


class SubProcessFirstVote(OriginSubProcess):

    def __init__(self, definition):
        super(SubProcessFirstVote, self).__init__(definition)

    def _start_subprocess(self, action):
        proposal = self.process.execution_context.created_entity('proposal')
        working_group = proposal.working_group
        if not hasattr(working_group, 'first_vote'):
            working_group.first_vote = True
            return None
        else:
            working_group.first_vote = False
            return super(SubProcessFirstVote, self)._start_subprocess(action)

    def stop(self):
        request = get_current_request()
        for process in self.sub_processes:
            exec_ctx = process.execution_context
            vote_processes = exec_ctx.get_involved_collection('vote_processes')
            vote_processes = [process for process in vote_processes
                              if not process._finished]
            if vote_processes:
                close_votes(None, request, vote_processes)

        super(SubProcessFirstVote, self).stop()


class SubProcessDefinition(OriginSubProcessDefinition):
    """Run the voting process for proposal publishing
       and working group configuration"""

    factory = SubProcessFirstVote

    def _init_subprocess(self, process, subprocess):
        root = getSite()
        proposal = process.execution_context.created_entity('proposal')
        working_group = proposal.working_group
        work_mode = getattr(proposal, 'work_mode', None)
        participants_mini = work_mode.participants_mini if work_mode else root.participants_mini
        participants_maxi = work_mode.participants_maxi if work_mode else root.participants_maxi
        electors = working_group.members[:participants_mini]
        if not getattr(working_group, 'first_decision', True):
            electors = working_group.members

        subjects = [proposal]
        ballot = Ballot('Referendum', electors, subjects, VP_DEFAULT_DURATION,
                        true_val=_("Submit the proposal"),
                        false_val=_("Continue to improve the proposal"))
        working_group.addtoproperty('ballots', ballot)
        ballot.report.description = VOTE_PUBLISHING_MESSAGE
        ballot.title = _("Continue to improve the proposal or not")
        processes = ballot.run_ballot()
        subprocess.ballots = PersistentList()
        subprocess.ballots.append(ballot)
        working_group.vp_ballot = ballot #vp for voting for publishing
        root_modes = root.get_work_modes()
        if len(root_modes) > 1:
            modes = [(m, root_modes[m].title) for m in root_modes
                     if root_modes[m].participants_mini <= len(wg.members)]
            modes = sorted(modes,
                           key=lambda e: root_modes[e[0]].order)
            group = [m[0] for m in modes]
            default_mode = proposal.work_mode.work_id
            if default_mode not in root_modes:
                default_mode = modes[0][0]

            ballot = Ballot('FPTP', electors, group, VP_DEFAULT_DURATION,
                            group_title=_('Work mode'),
                            group_values=modes,
                            group_default=default_mode)
            working_group.addtoproperty('ballots', ballot)
            ballot.title = _('Work modes')
            ballot.report.description = VOTE_MODEWORK_MESSAGE
            processes.extend(ballot.run_ballot(context=proposal))
            subprocess.ballots.append(ballot)
            working_group.work_mode_configuration_ballot = ballot

        if not getattr(working_group, 'first_decision', True) and \
           'closed' in working_group.state:
            subjects = [working_group]
            ballot = Ballot('Referendum', electors,
                            subjects, VP_DEFAULT_DURATION)
            working_group.addtoproperty('ballots', ballot)
            ballot.report.description = VOTE_REOPENING_MESSAGE
            ballot.title = _('Reopening working group')
            processes.extend(ballot.run_ballot(context=proposal))
            subprocess.ballots.append(ballot)
            working_group.reopening_configuration_ballot = ballot

        if len(working_group.members) <= participants_maxi:
            durations = list(AMENDMENTS_CYCLE_DEFAULT_DURATION.keys())
            group = sorted(durations,
                           key=lambda e: AMENDMENTS_CYCLE_DEFAULT_DURATION[e])
            ballot = Ballot('FPTP', electors, group, VP_DEFAULT_DURATION,
                            group_title=_('Delay'),
                            group_default='One week')
            working_group.addtoproperty('ballots', ballot)
            ballot.title = _('Amendment duration')
            ballot.report.description = VOTE_DURATION_MESSAGE
            processes.extend(ballot.run_ballot(context=proposal))
            subprocess.ballots.append(ballot)
            working_group.duration_configuration_ballot = ballot

        subprocess.execution_context.add_involved_collection(
            'vote_processes', processes)
        subprocess.duration = VP_DEFAULT_DURATION


class WorkSubProcess(OriginSubProcess):

    def __init__(self, definition):
        super(WorkSubProcess, self).__init__(definition)

    def _start_subprocess(self, action):
        proposal = self.process.execution_context.created_entity('proposal')
        work_mode_ballot = getattr(
            proposal.working_group, 'work_mode_configuration_ballot', None)
        if work_mode_ballot is not None and work_mode_ballot.report.voters:
            electeds = work_mode_ballot.report.get_electeds()
            if electeds:
                proposal.work_mode_id = electeds[0]

        root = proposal.__parent__
        work_mode = getattr(
            proposal, 'work_mode', root.get_default_work_mode())
        def_container = find_service('process_definition_container')
        pd = def_container.get_definition(
            work_mode.work_mode_process_id)
        proc = pd()
        proc.__name__ = proc.id
        runtime = find_service('runtime')
        runtime.addtoproperty('processes', proc)
        proc.defineGraph(pd)
        self.definition._init_subprocess(self.process, proc)
        proc.attachedTo = action
        proc.execute()
        self.sub_processes.append(proc)
        return proc


class WorkSubProcessDefinition(OriginSubProcessDefinition):
    """Run the voting process for proposal publishing
       and working group configuration"""

    factory = WorkSubProcess


@process_definition(name='proposalmanagement', id='proposalmanagement')
class ProposalManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(ProposalManagement, self).__init__(**kwargs)
        self.title = _('Proposals management')
        self.description = _('Proposals management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                eg = ExclusiveGatewayDefinition(),
                pg = ParallelGatewayDefinition(),
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
                publish = ActivityDefinition(contexts=[PublishProposal],
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
                compare = ActivityDefinition(contexts=[CompareProposal],
                                       description=_("Compare versions"),
                                       title=_("Compare"),
                                       groups=[]),
                seeproposal = ActivityDefinition(contexts=[SeeProposal],
                                       description=_("Details"),
                                       title=_("Details"),
                                       groups=[]),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'creat'),
                TransitionDefinition('pg', 'publishasproposal'),
                TransitionDefinition('pg', 'duplicate'),
                TransitionDefinition('pg', 'publish'),
                TransitionDefinition('pg', 'edit'),
                TransitionDefinition('pg', 'delete'),
                TransitionDefinition('pg', 'seerelatedideas'),
                TransitionDefinition('pg', 'comment'),
                TransitionDefinition('pg', 'compare'),
                TransitionDefinition('pg', 'seeamendments'),
                TransitionDefinition('pg', 'associate'),
                TransitionDefinition('pg', 'present'),
                TransitionDefinition('pg', 'resign'),
                TransitionDefinition('pg', 'participate'),
                TransitionDefinition('pg', 'firstparticipate'),
                TransitionDefinition('pg', 'withdraw'),
                TransitionDefinition('pg', 'support'),
                TransitionDefinition('pg', 'makeitsopinion'),
                TransitionDefinition('pg', 'oppose'),
                TransitionDefinition('pg', 'withdraw_token'),
                TransitionDefinition('pg', 'seeproposal'),
                TransitionDefinition('seeproposal', 'eg'),
                TransitionDefinition('creat', 'eg'),
                TransitionDefinition('publishasproposal', 'eg'),
                TransitionDefinition('duplicate', 'eg'),
                TransitionDefinition('publish', 'eg'),
                TransitionDefinition('edit', 'eg'),
                TransitionDefinition('delete', 'eg'),
                TransitionDefinition('seerelatedideas', 'eg'),
                TransitionDefinition('comment', 'eg'),
                TransitionDefinition('compare', 'eg'),
                TransitionDefinition('seeamendments', 'eg'),
                TransitionDefinition('associate', 'eg'),
                TransitionDefinition('present', 'eg'),
                TransitionDefinition('resign', 'eg'),
                TransitionDefinition('participate', 'eg'),
                TransitionDefinition('firstparticipate', 'eg'),
                TransitionDefinition('withdraw', 'eg'),
                TransitionDefinition('support', 'eg'),
                TransitionDefinition('makeitsopinion', 'eg'),
                TransitionDefinition('oppose', 'eg'),
                TransitionDefinition('withdraw_token', 'eg'),
                TransitionDefinition('eg', 'end')
        )


@process_definition(name='proposalimprovementcycle',
                    id='proposalimprovementcycle')
class ProposalImprovementCycle(ProcessDefinition, VisualisableElement):
    isControlled = True
    isVolatile = True

    def __init__(self, **kwargs):
        super(ProposalImprovementCycle, self).__init__(**kwargs)
        self.title = _('Proposals improvement cycle')
        self.description = _('Proposals improvement cycle')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                eg = ExclusiveGatewayDefinition(),
                eg1 = ExclusiveGatewayDefinition(),
                votingpublication = SubProcessDefinition(pd='ballotprocess', contexts=[VotingPublication],
                                       description=_("Start voting for publication"),
                                       title=_("Start voting for publication"),
                                       groups=[]),
                work = WorkSubProcessDefinition(pd='None', contexts=[Work],
                                       description=_("Start work"),
                                       title=_("Start work"),
                                       groups=[]),
                submit = ActivityDefinition(contexts=[SubmitProposal],
                                       description=_("Submit the proposal"),
                                       title=_("Submit"),
                                       groups=[]),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'eg'),
                TransitionDefinition('eg', 'votingpublication'),
                TransitionDefinition('votingpublication', 'eg1'),
                TransitionDefinition('eg1', 'work', amendable_condition, sync=True),
                TransitionDefinition('eg1', 'submit', publish_condition, sync=True),
                TransitionDefinition('submit', 'end'),
                TransitionDefinition('work', 'eg'),
        )
