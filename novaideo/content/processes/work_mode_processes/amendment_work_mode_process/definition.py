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

import html_diff_wrapper
from dace.processinstance.activity import (
    SubProcess as OriginSubProcess)
from dace.processdefinition.processdef import ProcessDefinition
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

from novaideo.content.processes.proposal_management.behaviors import (
    calculate_amendments_cycle_duration)
from .behaviors import (
    ImproveProposal,
    VotingAmendments,
    Alert,
    AmendmentsResult,
    VOTE_AMENDMENTS_MESSAGE,
    AMENDMENTS_VOTE_DEFAULT_DURATION,
    close_votes
    )
from novaideo import _
from novaideo.content.ballot import Ballot


def eg4_votingamendments_condition(process):
    proposal = process.attachedTo.process.execution_context.created_entity(
        'proposal')
    if any('submitted' in a.state for a in proposal.amendments):
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
            vote_processes = [process for process in vote_processes
                              if not process._finished]
            if vote_processes:
                close_votes(None, request, vote_processes)

        super(SubProcess, self).stop()


class SubProcessDefinitionAmendments(OriginSubProcessDefinition):
    """Run the voting process for amendments"""

    factory = SubProcess

    def _init_subprocess(self, process, subprocess):
        proposal = process.attachedTo.process.execution_context.created_entity(
            'proposal')
        working_group = proposal.working_group
        electors = working_group.members
        amendments = [a for a in proposal.amendments if 'submitted' in a.state]
        processes = []
        groups = []
        for amendment in amendments:
            isadded = False
            related_ideas_amendment = list(amendment.related_ideas)
            for group in groups:
                for amt in group:
                    related_ideas_a = list(amt.related_ideas)
                    if html_diff_wrapper.has_conflict(amt.text,
                                                  [amendment.text]) or \
                       (related_ideas_amendment and \
                        any(e in related_ideas_amendment
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
        working_group.amendments_ballots = PersistentList()
        for index, group in enumerate(groups):
            ballot = Ballot('MajorityJudgment', electors,
                            group, AMENDMENTS_VOTE_DEFAULT_DURATION)
            working_group.addtoproperty('ballots', ballot)
            ballot.report.description = VOTE_AMENDMENTS_MESSAGE
            ballot.title = _('Vote for amendments (group ${nbi})',
                             mapping={'nbi': index+1})
            processes.extend(ballot.run_ballot(context=proposal))
            subprocess.ballots.append(ballot)
            working_group.amendments_ballots.append(ballot)

        subprocess.execution_context.add_involved_collection(
            'vote_processes', processes)
        subprocess.duration = AMENDMENTS_VOTE_DEFAULT_DURATION


@process_definition(name='amendmentworkmodeprocess', id='amendmentworkmodeprocess')
class AmendmentWorkModeProcess(ProcessDefinition, VisualisableElement):
    isControlled = True
    isSubProcess = True
    isVolatile = True

    def __init__(self, **kwargs):
        super(AmendmentWorkModeProcess, self).__init__(**kwargs)
        self.title = _('Change with amendments')
        self.description = _('Change with amendments')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                eg1 = ExclusiveGatewayDefinition(),
                pg1 = ParallelGatewayDefinition(),
                eg2 = ExclusiveGatewayDefinition(),
                votingamendments = SubProcessDefinitionAmendments(pd='ballotprocess', contexts=[VotingAmendments],
                                       description=_("Start voting for amendments"),
                                       title=_("Start voting for amendments"),
                                       groups=[]),
                alert = ActivityDefinition(contexts=[Alert],
                                       description=_("Alert"),
                                       title=_("Alert"),
                                       groups=[]),
                timer = IntermediateCatchEventDefinition(TimerEventDefinition(time_date=calculate_amendments_cycle_duration)),
                amendmentsresult = ActivityDefinition(contexts=[AmendmentsResult],
                                       description=_("Amendments result"),
                                       title=_("Amendments result"),
                                       groups=[]),
                improve = ActivityDefinition(contexts=[ImproveProposal],
                                       description=_("Improve the proposal"),
                                       title=_("Improve"),
                                       groups=[]),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg1'),
                TransitionDefinition('pg1', 'improve'),
                TransitionDefinition('pg1', 'timer'),
                TransitionDefinition('timer', 'eg1'),
                TransitionDefinition('eg1', 'votingamendments', eg4_votingamendments_condition, sync=True),
                TransitionDefinition('eg1', 'alert', eg4_alert_condition, sync=True),
                TransitionDefinition('alert', 'eg2'),
                TransitionDefinition('votingamendments', 'amendmentsresult'),
                TransitionDefinition('amendmentsresult', 'eg2'),
                TransitionDefinition('eg2', 'end'),
        )
