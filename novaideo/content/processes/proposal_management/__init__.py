# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import venusian
import datetime

from dace.objectofcollaboration.entity import Entity
from dace.util import getSite

from novaideo.content.ballot import Ballot
from novaideo.core import _
from novaideo.utilities.alerts_utility import alert
from novaideo.content.alert import InternalAlertKind


AMENDMENTS_CYCLE_DEFAULT_DURATION_T = [
    _("Three minutes"),
    _("Five minutes"),
    _("Ten minutes"),
    _("Twenty minutes"),
    _("One hour"),
    _("Four hours"),
    _("One day"),
    _("Three days"),
    _("One week"),
    _("Two weeks")]


WORK_MODES = {}


FIRST_VOTE_DURATION_MESSAGE = _(
    "You have decided to join the working group. Your first decision is to vote "
    "whether the proposal should or not be improved. The ballot is closed as soon as "
    "the working group has three participants. If « Improve » wins a majority, "
    "an improvement cycle begins. If not, the proposal is not improved. It is directly submitted "
    "as is to the evaluation of the other members of the platform.")


FIRST_VOTE_PUBLISHING_MESSAGE = _("Vote for submission")


VP_DEFAULT_DURATION = datetime.timedelta(days=1)


AMENDMENTS_CYCLE_DEFAULT_DURATION = {
    "Three minutes": datetime.timedelta(minutes=3),
    "Five minutes": datetime.timedelta(minutes=5),
    "Ten minutes": datetime.timedelta(minutes=10),
    "Twenty minutes": datetime.timedelta(minutes=20),
    "One hour": datetime.timedelta(hours=1),
    "Four hours": datetime.timedelta(hours=4),
    "One day": datetime.timedelta(days=1),
    "Three days": datetime.timedelta(days=3),
    "One week": datetime.timedelta(weeks=1),
    "Two weeks": datetime.timedelta(weeks=2)}


class work_mode(object):
    """ Decorator for novaideo access actions.
    An access action allows to view an object"""

    def __call__(self, wrapped):
        def callback(scanner, name, ob):
            WORK_MODES[ob.work_id] = ob()

        venusian.attach(wrapped, callback)
        return wrapped


class WorkMode(Entity):

    work_mode_process_id = NotImplemented
    participants_mini = NotImplemented
    participants_maxi = 12
    title = _('Working mode')
    description = _('Working mode for the improvement of the proposal')
    work_id = 'work_mode'
    order = 0


@work_mode()
class WikiWorkMode(WorkMode):

    work_mode_process_id = 'wikiworkmodeprocess'
    participants_mini = 1
    title = _('Change without validation (At least one member)')
    work_id = 'wiki'
    order = 0


@work_mode()
class CorrectionWorkMode(WorkMode):

    work_mode_process_id = 'correctionworkmodeprocess'
    participants_mini = 2
    title = _('Change with validation (At least two members)')
    work_id = 'correction'
    order = 1


@work_mode()
class AmendmentWorkMode(WorkMode):

    work_mode_process_id = 'amendmentworkmodeprocess'
    participants_mini = 3
    title = _('Change with amendments (At least three members)')
    work_id = 'amendment'
    order = 2


def init_proposal_ballots(proposal):
    wg = proposal.working_group
    electors = []
    subjects = [proposal]
    ballot = Ballot('Referendum', electors, subjects, VP_DEFAULT_DURATION,
                    true_val=_("Submit the proposal as is"),
                    false_val=_("Continue to improve the proposal"))
    wg.addtoproperty('ballots', ballot)
    ballot.report.description = FIRST_VOTE_PUBLISHING_MESSAGE
    ballot.title = _("Submit the proposal or not")
    wg.vp_ballot = ballot #vp for voting for publishing
    durations = list(AMENDMENTS_CYCLE_DEFAULT_DURATION.keys())
    group = sorted(durations,
                   key=lambda e: AMENDMENTS_CYCLE_DEFAULT_DURATION[e])
    ballot = Ballot('FPTP', electors, group, VP_DEFAULT_DURATION,
                    group_title=_('Duration of the amendment cycle'),
                    group_default='One week')
    wg.addtoproperty('ballots', ballot)
    ballot.title = _('Duration of the amendment cycle')
    ballot.report.description = FIRST_VOTE_DURATION_MESSAGE
    wg.duration_configuration_ballot = ballot


def add_files_to_workspace(files_data, workspace):
    files = []
    for file_data in files_data:
        file_ = file_data.get('_object_data', None)
        if file_:
            workspace.addtoproperty('files', file_)
            files.append(file_)

    root = getSite()
    members = workspace.working_group.members
    alert('internal', [root], members,
          internal_kind=InternalAlertKind.working_group_alert,
          subjects=[workspace.proposal], alert_kind='add_files')
    return files


def add_attached_files(appstruct, proposal):
    files = appstruct.get('add_files', None)
    files_to_add = []
    if files is not None:
        attached_files = files.get('attached_files', [])
        if attached_files:
            workspace = proposal.workspace
            files_to_add = add_files_to_workspace(attached_files, workspace)

        ws_files = files.get('ws_files', [])
        if ws_files:
            files_to_add.extend(ws_files)

    proposal.setproperty('attached_files', files_to_add)


def end_work(proposal, request):
    """Close the improvement cycle process"""
    from novaideo.content.processes.ballot_processes import (
        remove_vote_processes)
    runtime = request.root['runtime']
    # The improvement cycle
    proc = proposal.working_group.improvement_cycle_proc
    if proc:
        # Work sub process
        work_actions = proc.get_actions('work')
        # Voting publication sub process
        vote_actions = proc.get_actions('votingpublication')
        if work_actions:
            work_proc = work_actions[0].sub_process
            if work_proc:
                # If amendment mode
                a_vote_actions = work_proc.get_actions('votingamendments')
                if a_vote_actions:
                    remove_vote_processes(a_vote_actions[0], runtime)

                runtime.delfromproperty('processes', work_proc)
        elif vote_actions:
            remove_vote_processes(vote_actions[0], runtime)

        runtime.delfromproperty('processes', proc)


def remove_participant_from_ballots(proposal, request, user):
    """Close the improvement cycle process"""
    from novaideo.content.processes.ballot_processes import (
        remove_elector_vote_processes)
    # The improvement cycle
    proc = proposal.working_group.improvement_cycle_proc
    if proc:
        # Work sub process
        work_actions = proc.get_actions('work')
        # Voting publication sub process
        vote_actions = proc.get_actions('votingpublication')
        if work_actions:
            work_proc = work_actions[0].sub_process
            if work_proc:
                # If amendment mode
                a_vote_actions = work_proc.get_actions('votingamendments')
                if a_vote_actions:
                    remove_elector_vote_processes(a_vote_actions[0], user)

        elif vote_actions:
            remove_elector_vote_processes(vote_actions[0], user)
