# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import pytz
import datetime
from persistent.list import PersistentList
from zope.interface import implementer

from substanced.content import content
from substanced.util import renamer, get_oid
from dace.objectofcollaboration.principal.util import grant_roles
from dace.objectofcollaboration.entity import Entity
from dace.util import find_service, get_obj
from dace.descriptors import (
        CompositeUniqueProperty,
        CompositeMultipleProperty,
        SharedUniqueProperty,
        SharedMultipleProperty)
from pontus.core import VisualisableElement

from .interface import IVote, IBallotType, IReport, IBallot, IBallotBox
from novaideo import _

@content(
    'referendumvote',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IVote)
class ReferendumVote(VisualisableElement, Entity):
    """Referendum vote"""
    name = renamer()

    def __init__(self, value=None, **kwargs):
        super(ReferendumVote, self).__init__(**kwargs)
        self.value = value


@implementer(IBallotType)
class Referendum(object):
    """Referendum election"""
    vote_factory = ReferendumVote

    def __init__(self, report, vote_process_id='referendumprocess', **kwargs):
        self.vote_process_id = vote_process_id
        self.report = report
        if isinstance(self.report.subjects, (list, tuple, PersistentList)):
            self.subject = self.report.subjects[0]
        else:
            self.subject = self.report.subjects

        self.false_val = kwargs.get('false_val', _('Favour'))
        self.true_val = kwargs.get('true_val', _('Against'))

    def run_ballot(self, context=None):
        """Run referendum election processes for all electors"""

        processes = []
        def_container = find_service('process_definition_container')
        runtime = find_service('runtime')
        pd = def_container.get_definition(self.vote_process_id)
        if context is None:
            context = self.subject

        proc = pd()
        proc.__name__ = proc.id
        runtime.addtoproperty('processes', proc)
        proc.defineGraph(pd)
        proc.execution_context.add_involved_entity('subject', context)
        proc.ballot = self.report.ballot
        proc.execute()
        processes.append(proc)
        return processes

    def calculate_votes(self, votes):
        """Return the result of ballot"""

        result = {'True':0, 'False':0, 'None':0}
        for vote in votes:
            if vote.value is True:
                result['True'] += 1
            elif vote.value is False:
                result['False'] += 1
            else:
                result['None'] += 1

        return result

    def get_electeds(self, result):
        """Return the elected subject"""

        if result['True'] > result['False']:
            return [self.subject]

        return None


DEFAULT_JUDGMENTS = {'Excellent': 7,
                     'Very good': 6,
                     'Good': 5,
                     'Fairly well': 4,
                     'Passable': 3,
                     'Insufficient': 2,
                     'Reject': 1}

_JUDGMENTS_TRANSLATION = [_('Excellent'),
                          _('Very good'),
                          _('Good'),
                          _('Fairly well'),
                          _('Passable'),
                          _('Insufficient'),
                          _('Reject')]

@content(
    'majorityjudgmentvote',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IVote)
class MajorityJudgmentVote(VisualisableElement, Entity):
    """Majority judgment vote"""
    name = renamer()

    def __init__(self, value=None, **kwargs):
        super(MajorityJudgmentVote, self).__init__(**kwargs)
        self.value = value
        #value  = {objectoid: 'Judgment', ...}


@implementer(IBallotType)
class MajorityJudgment(object):
    """Majority judgment election"""
    vote_factory = MajorityJudgmentVote

    def __init__(self, report, vote_process_id='majorityjudgmentprocess', **kwargs):
        self.vote_process_id = vote_process_id
        self.report = report
        self.judgments = DEFAULT_JUDGMENTS

    def run_ballot(self, context=None):
        """Run MajorityJudgment election processes for all electors"""

        processes = []
        def_container = find_service('process_definition_container')
        runtime = find_service('runtime')
        pd = def_container.get_definition(self.vote_process_id)
        if context is None:
            context = self.report.subjects[0].__parent__

        proc = pd()
        proc.__name__ = proc.id
        runtime.addtoproperty('processes', proc)
        proc.defineGraph(pd)
        proc.execution_context.add_involved_entity('subject', context)
        proc.ballot = self.report.ballot
        proc.execute()
        processes.append(proc)
        return processes

    def calculate_votes(self, votes):
        """Return the result of ballot"""

        result = {}
        for subject in self.report.subjects:
            oid = get_oid(subject)
            result[oid] = {}
            for judgment in self.judgments.keys():
                result[oid][judgment] = 0

        for vote in votes:
            for oid, judgment in vote.value.items():
                subject = get_obj(oid)
                if subject in self.report.subjects:
                    result[oid][judgment] += 1

        return result

    def get_electeds(self, result):
        """Return the elected subject"""

        len_voters = len(self.report.voters)
        if len_voters == 0:
            return None

        judgments = sorted(list(self.judgments.keys()), 
                           key=lambda o: self.judgments[o])
        object_results = dict([(oid, 0) for oid in result.keys()])
        for oid in result.keys():
            object_result = 0
            for judgment in judgments:
                object_result += float(result[oid][judgment]) / \
                                       float(len_voters) * 100
                if object_result >= 50:
                    object_results[oid] = self.judgments[judgment]
                    break

        sorted_results = sorted(list(object_results.keys()), 
                                key=lambda o: object_results[o], 
                                reverse=True)
        if sorted_results:
            try:
                elected = get_obj(sorted_results[0])
                return [elected]
            except Exception:
                return None

        return None


@content(
    'fptpvote',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IVote)
class FPTPVote(VisualisableElement, Entity):
    """FPTP vote class"""
    name = renamer()

    def __init__(self, value=None, **kwargs):
        super(FPTPVote, self).__init__(**kwargs)
        self.value = value
        #value  = object_oid


@implementer(IBallotType)
class FPTP(object):
    """A first-past-the-post (abbreviated FPTP or FPP) election"""
    vote_factory = FPTPVote

    def __init__(self, report, vote_process_id='fptpprocess', **kwargs):
        self.vote_process_id = vote_process_id
        self.report = report
        self.group_title = kwargs.get('group_title', _('Choices'))
        self.group_values = kwargs.get('group_values', None)
        self.group_default = kwargs.get('group_default', None)

    def run_ballot(self, context=None):
        """Run FPTP election processes for all electors"""

        processes = []
        def_container = find_service('process_definition_container')
        runtime = find_service('runtime')
        pd = def_container.get_definition(self.vote_process_id)
        if context is None:
            context = self.report.subjects[0].__parent__

        proc = pd()
        proc.__name__ = proc.id
        runtime.addtoproperty('processes', proc)
        proc.defineGraph(pd)
        proc.execution_context.add_involved_entity('subject', context)
        proc.ballot = self.report.ballot
        proc.execute()
        processes.append(proc)

        return processes

    def calculate_votes(self, votes):
        """Return the result of ballot"""

        result = {}
        for subject in self.report.subjects:
            try:
                subject_id = get_oid(subject)
            except Exception:
                subject_id = subject

            result[subject_id] = 0

        for vote in votes:
            subject = get_obj(vote.value)
            if subject is None:
                subject = vote.value

            try:
                subject_id = get_oid(vote.value)
            except Exception:
                subject_id = vote.value
            
            if subject in self.report.subjects:
                result[subject_id] += 1

        return result

    def get_electeds(self, result):
        """Return the elected subject"""

        electeds_ids = sorted(list(result.keys()), 
                              key=lambda o: result[o], 
                              reverse=True)
        if electeds_ids:
            elected_id = electeds_ids[0]
            elected = get_obj(elected_id)
            if elected is None:
                elected = elected_id

            return [elected]

        return None


class DateSubjectMedian(object):
    vote_type = 'date'

    @classmethod
    def calculate_votes(cls, ballottype, votes):
        """Return the result of ballot"""
        return [vote.value for vote in votes]

    @classmethod
    def get_electeds(cls, ballottype, result):
        """Return the elected subject"""
        result_set = list(set(result))
        if len(result) == 0:
            return []

        sorted_results = sorted(result_set)
        len_result = len(result_set)
        median = len_result // 2
        if median == 0:
            return [sorted_results[-1]]
        else:
            if len_result % 2 == 0:
                return [sorted_results[median+1]]
            else:
                return [sorted_results[median]]


SUBJECT_TYPES_MANAGER = {'datemedian': DateSubjectMedian}

@content(
    'rangevote',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IVote)
class RangeVote(VisualisableElement, Entity):
    """Range vote class"""
    name = renamer()

    def __init__(self, value=None, **kwargs):
        super(RangeVote, self).__init__(**kwargs)
        self.value = value
        #value  = object_oid


@implementer(IBallotType)
class RangeVoting(object):
    """Range voting class"""
    vote_factory = RangeVote

    def __init__(self, report, vote_process_id='rangevotingprocess', **kwargs):
        self.vote_process_id = vote_process_id
        self.report = report
        self.subject_type = kwargs.get('subject_type', 'string').lower()
        self.subject_type_manager = SUBJECT_TYPES_MANAGER.get(self.subject_type,
                                                              None)

    def run_ballot(self, context=None):
        """Run range voting processes for all electors"""
        processes = []
        def_container = find_service('process_definition_container')
        runtime = find_service('runtime')
        pd = def_container.get_definition(self.vote_process_id)
        if context is None:
            context = self.report.subjects[0].__parent__

        proc = pd()
        proc.__name__ = proc.id
        runtime.addtoproperty('processes', proc)
        proc.defineGraph(pd)
        proc.execution_context.add_involved_entity('subject', context)
        proc.ballot = self.report.ballot
        proc.execute()
        processes.append(proc)
        return processes

    def calculate_votes(self, votes):
        """Return the result of ballot"""
        if self.subject_type_manager:
            return self.subject_type_manager.calculate_votes(self, votes)

        return None

    def get_electeds(self, result):
        """Return the elected subject"""
        if self.subject_type_manager:
            return self.subject_type_manager.get_electeds(self, result)

        return None


BALLOT_TYPES = {'RangeVoting': RangeVoting,
                'Referendum': Referendum,
                'MajorityJudgment': MajorityJudgment,
                'FPTP': FPTP}


@content(
    'report',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IReport)
class Report(VisualisableElement, Entity):
    """Report of ballot class"""
    name = renamer()
    electors = SharedMultipleProperty('electors')
    voters = SharedMultipleProperty('voters')
    subjects = SharedMultipleProperty('subjects')
    processes = SharedMultipleProperty('processes')
    ballot = SharedUniqueProperty('ballot', 'report')

    def __init__(self, ballottype , electors, subjects, **kwargs):
        super(Report, self).__init__(**kwargs)
        [self.addtoproperty('electors', elector) for elector in electors]
        [self.addtoproperty('subjects', subject) for subject in subjects]
        self.ballottype = BALLOT_TYPES[ballottype](self, **kwargs)
        if 'vote_process_id' in kwargs:
            self.ballottype.vote_process_id = kwargs['vote_process_id']

        self.result = None
        self.calculated = False

    def calculate_votes(self):
        """Return the result of ballot"""

        if not self.calculated:
            votes = self.ballot.ballot_box.votes
            self.result = self.ballottype.calculate_votes(votes)
            self.calculated = True
        else:
            return self.result

    def get_electeds(self):
        """Return the elected subject"""

        if not self.calculated:
            self.calculate_votes()

        return self.ballottype.get_electeds(self.result)


@content(
    'ballotbox',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IBallotBox)
class BallotBox(VisualisableElement, Entity):
    """Ballot box class"""
    name = renamer()
    votes = CompositeMultipleProperty('votes')


@content(
    'ballot',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IBallot)
class Ballot(VisualisableElement, Entity):
    """Ballot class"""
    name = renamer()
    ballot_box = CompositeUniqueProperty('ballot_box')
    report = CompositeUniqueProperty('report', 'ballot')

    def __init__(self, ballot_type, electors, subjects, duration, **kwargs):
        super(Ballot, self).__init__(**kwargs)
        self.setproperty('ballot_box', BallotBox())
        self.setproperty('report', Report(ballot_type,
                                          electors,
                                          subjects,
                                          **kwargs))
        self.run_at = None
        self.duration = duration
        self.finished_at = None

    def run_ballot(self, context=None):
        """Run the ballot"""
        self.run_at = datetime.datetime.now(tz=pytz.UTC)
        self.finished_at = self.run_at + self.duration
        processes = self.report.ballottype.run_ballot(context)
        return processes
