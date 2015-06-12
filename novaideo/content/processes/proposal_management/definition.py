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
    eg3_publish_condition
    )
from novaideo import _
from novaideo.content.ballot import Ballot


def eg3_amendable_condition(process):
    return not eg3_publish_condition(process)


class SubProcessFirstVote(OriginSubProcess):

    def __init__(self, definition):
        super(SubProcessFirstVote, self).__init__(definition)

    def _start_subprocess(self, action):
        if not hasattr(self.process, 'first_vote'):
            self.process.first_vote = True
            # next
            return None
        else:
            self.process.first_vote = False
            return super(SubProcessFirstVote, self)._start_subprocess(action)

    def stop(self):
        request = get_current_request()
        for process in self.sub_processes:
            exec_ctx = process.execution_context
            vote_processes = exec_ctx.get_involved_collection('vote_processes')
            vote_processes = [process for process in vote_processes \
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
        wg = proposal.working_group
        participants_mini = root.participants_mini
        participants_maxi = root.participants_maxi
        work_mode = getattr(proposal, 'work_mode', None)
        if work_mode:
            participants_mini = work_mode.participants_mini
            participants_maxi = work_mode.participants_maxi

        electors = wg.members[:participants_mini]
        if not getattr(process, 'first_decision', True):
            electors = wg.members

        subjects = [proposal]
        ballot = Ballot('Referendum', electors, subjects, VP_DEFAULT_DURATION,
                        true_val=_("Submit the proposal"),
                        false_val=_("Continue to improve the proposal"))
        wg.addtoproperty('ballots', ballot)
        ballot.report.description = VOTE_PUBLISHING_MESSAGE
        ballot.title = _("Continue to improve the proposal or not")
        processes = ballot.run_ballot()
        subprocess.ballots = PersistentList()
        subprocess.ballots.append(ballot)
        process.vp_ballot = ballot #vp for voting for publishing

        root_modes = root.get_work_modes()
        if len(root_modes) > 1:
            modes = [(m, root_modes[m].title) for m in root_modes \
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
            wg.addtoproperty('ballots', ballot)
            ballot.title = _('Work modes')
            ballot.report.description = VOTE_MODEWORK_MESSAGE
            processes.extend(ballot.run_ballot(context=proposal))
            subprocess.ballots.append(ballot)
            process.work_mode_configuration_ballot = ballot

        if not getattr(process, 'first_decision', True) and \
          'closed' in wg.state:
            subjects = [wg]
            ballot = Ballot('Referendum', electors,
                            subjects, VP_DEFAULT_DURATION)
            wg.addtoproperty('ballots', ballot)
            ballot.report.description = VOTE_REOPENING_MESSAGE
            ballot.title = _('Reopening working group')
            processes.extend(ballot.run_ballot(context=proposal))
            subprocess.ballots.append(ballot)
            process.reopening_configuration_ballot = ballot

        if len(wg.members) <= participants_maxi:
            durations = list(AMENDMENTS_CYCLE_DEFAULT_DURATION.keys())
            group = sorted(durations,
                           key=lambda e: AMENDMENTS_CYCLE_DEFAULT_DURATION[e])
            ballot = Ballot('FPTP', electors, group, VP_DEFAULT_DURATION,
                            group_title=_('Delay'),
                            group_default='One week')
            wg.addtoproperty('ballots', ballot)
            ballot.title = _('Amendment duration')
            ballot.report.description = VOTE_DURATION_MESSAGE
            processes.extend(ballot.run_ballot(context=proposal))
            subprocess.ballots.append(ballot)
            process.duration_configuration_ballot = ballot

        subprocess.execution_context.add_involved_collection(
                                      'vote_processes', processes)
        subprocess.duration = VP_DEFAULT_DURATION


class WorkSubProcess(OriginSubProcess):

    def __init__(self, definition):
        super(WorkSubProcess, self).__init__(definition)

    def _start_subprocess(self, action):
        proposal = self.process.execution_context.created_entity('proposal')
        work_mode_ballot = getattr(self.process,
                            'work_mode_configuration_ballot', None)
        if work_mode_ballot is not None and work_mode_ballot.report.voters:
            electeds = work_mode_ballot.report.get_electeds()
            if electeds:
                proposal.work_mode_id = electeds[0]

        root = proposal.__parent__
        work_mode = getattr(proposal, 'work_mode',
                                  root.get_default_work_mode())
        def_container = find_service('process_definition_container')
        pd = def_container.get_definition(work_mode.work_mode_process_id)
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
                work = WorkSubProcessDefinition(pd='None', contexts=[Work],
                                       description=_("Start work"),
                                       title=_("Start work"),
                                       groups=[]),
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
                TransitionDefinition('pg3', 'eg2'),
                TransitionDefinition('eg2', 'votingpublication'),
                TransitionDefinition('votingpublication', 'eg3'),
                TransitionDefinition('eg3', 'work', eg3_amendable_condition, sync=True),
                TransitionDefinition('eg3', 'publish', eg3_publish_condition, sync=True),
                TransitionDefinition('publish', 'pg6'),
                TransitionDefinition('pg6', 'support'),
                TransitionDefinition('pg6', 'makeitsopinion'),
                TransitionDefinition('pg6', 'oppose'),
                TransitionDefinition('pg6', 'withdraw_token'),
                TransitionDefinition('work', 'eg2'),
        )
