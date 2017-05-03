# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import uuid
import pytz
import datetime
from persistent.list import PersistentList
from zope.interface import implementer

from substanced.content import content
from substanced.util import renamer, get_oid
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


DEFAULT_BALLOT_GROUP = {
    'group_id': 'ballotid',
    'group_title': _('Votes'),
    'group_activate': False,
    'group_activator_title': _('Vote'),
    'group_activator_class_css': 'vote-action',
    'group_activator_style_picto': 'glyphicon glyphicon-stats',
    'group_activator_order': 100
}


class Vote(VisualisableElement, Entity):

    def __init__(self, value=None, **kwargs):
        super(Vote, self).__init__(**kwargs)
        self.uid = uuid.uuid4().hex
        self.__name__ = self.uid

    @property
    def report(self):
        return self.__parent__.__parent__.report


@content(
    'referendumvote',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IVote)
class ReferendumVote(Vote):
    """Referendum vote"""
    name = renamer()
    templates = {'default': 'novaideo:views/templates/vote/referendum_vote_result.pt',
                 'bloc': 'novaideo:views/templates/vote/referendum_vote_result.pt',
                 'small': 'novaideo:views/templates/vote/referendum_vote_result.pt',
                 'popover': 'novaideo:views/templates/vote/referendum_vote_result.pt'}

    def __init__(self, value=None, **kwargs):
        super(ReferendumVote, self).__init__(**kwargs)
        self.value = value


@implementer(IBallotType)
class Referendum(object):
    """Referendum election"""
    vote_factory = ReferendumVote
    templates = {
        'detail': 'novaideo:views/templates/vote/referendum_type_detail.pt',
        'result': 'novaideo:views/templates/vote/referendum_type_result.pt',}

    def __init__(self, report, vote_process_id='referendumprocess', **kwargs):
        self.vote_process_id = vote_process_id
        self.report = report
        if isinstance(self.report.subjects, (list, tuple, PersistentList)):
            self.subject = self.report.subjects[0]
        else:
            self.subject = self.report.subjects

        self.false_val = kwargs.get('false_val', _('In favour'))
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
                     'Fairly good': 4,
                     'Pass': 3,
                     'Insufficient': 2,
                     'To be rejected': 1}

DEFAULT_JUDGMENTS_VALUES = {
    7: 'Excellent',
    6: 'Very good',
    5: 'Good',
    4: 'Fairly good',
    3: 'Pass',
    2: 'Insufficient',
    1: 'To be rejected'}

_JUDGMENTS_TRANSLATION = [_('Excellent'),
                          _('Very good'),
                          _('Good'),
                          _('Fairly good'),
                          _('Pass'),
                          _('Insufficient'),
                          _('To be rejected')]

@content(
    'majorityjudgmentvote',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IVote)
class MajorityJudgmentVote(Vote):
    """Majority judgment vote"""
    name = renamer()
    templates = {'default': 'novaideo:views/templates/vote/mj_vote_result.pt',
                 'bloc': 'novaideo:views/templates/vote/mj_vote_result.pt',
                 'small': 'novaideo:views/templates/vote/mj_vote_result.pt',
                 'popover': 'novaideo:views/templates/vote/mj_vote_result.pt'}

    def __init__(self, value=None, **kwargs):
        super(MajorityJudgmentVote, self).__init__(**kwargs)
        self.value = value
        #value  = {objectoid: 'Judgment', ...}


@implementer(IBallotType)
class MajorityJudgment(object):
    """Majority judgment election"""
    vote_factory = MajorityJudgmentVote
    templates = {
        'detail': 'novaideo:views/templates/vote/majorityjudgment_type_detail.pt',
        'result': 'novaideo:views/templates/vote/majorityjudgment_type_result.pt'
    }

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

    def get_median_notes(self, result):
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

        return object_results

    def get_electeds(self, result):
        """Return the elected subject"""
        sorted_results = self.get_median_notes(result)
        sorted_results = sorted(list(sorted_results.keys()),
                                key=lambda o: sorted_results[o],
                                reverse=True)
        if sorted_results:
            try:
                elected = get_obj(sorted_results[0])
                return [elected]
            except Exception:
                return None

        return None

    def get_vote_values(self, vote):
        return [(get_obj(oid), judgment) for
                oid, judgment in vote.items()]

    def get_vote_value(self, vote):
        result = self.get_vote_values(vote)
        return sorted(
            result,
            key=lambda e: DEFAULT_JUDGMENTS[e[1]],
            reverse=True)

    def get_options(self):
        return sorted(
            self.judgments,
            key=lambda e: DEFAULT_JUDGMENTS[e],
            reverse=True)

    def get_judgment(self, value):
        return DEFAULT_JUDGMENTS_VALUES.get(value, '')

    def get_judgment_value(self, judgment):
        return DEFAULT_JUDGMENTS.get(judgment, 0)


@content(
    'fptpvote',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IVote)
class FPTPVote(Vote):
    """FPTP vote class"""
    name = renamer()
    templates = {'default': 'novaideo:views/templates/vote/fptp_vote_result.pt',
                 'bloc': 'novaideo:views/templates/vote/fptp_vote_result.pt',
                 'small': 'novaideo:views/templates/vote/fptp_vote_result.pt',
                 'popover': 'novaideo:views/templates/vote/fptp_vote_result.pt'}

    def __init__(self, value=None, **kwargs):
        super(FPTPVote, self).__init__(**kwargs)
        self.value = value
        #value  = object_oid


@implementer(IBallotType)
class FPTP(object):
    """A first-past-the-post (abbreviated FPTP or FPP) election"""
    vote_factory = FPTPVote
    templates = {
        'detail': 'novaideo:views/templates/vote/fptp_type_detail.pt',
        'result': 'novaideo:views/templates/vote/fptp_type_result.pt',}

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

            subject_id = self.get_option_id(vote.value)
            if subject in self.report.subjects:
                result[subject_id] += 1

        return result

    def get_option_id(self, option):
        return get_oid(option, option)

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

    def get_options(self):
        values_mapping = self.group_values
        if values_mapping is None:
            return self.report.subjects
        values_mapping = dict(values_mapping)
        return [values_mapping.get(option) for option
                in self.report.subjects]

    def get_option(self, option):
        values_mapping = self.group_values
        if values_mapping is None:
            return option

        values_mapping = dict(values_mapping)
        return values_mapping.get(option, option)


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
class RangeVote(Vote):
    """Range vote class"""
    name = renamer()
    templates = {'default': 'novaideo:views/templates/vote/range_vote_result.pt',
                 'bloc': 'novaideo:views/templates/vote/range_vote_result.pt',
                 'small': 'novaideo:views/templates/vote/range_vote_result.pt',
                 'popover': 'novaideo:views/templates/vote/range_vote_result.pt'}

    def __init__(self, value=None, **kwargs):
        super(RangeVote, self).__init__(**kwargs)
        self.value = value
        #value  = object_oid


@implementer(IBallotType)
class RangeVoting(object):
    """Range voting class"""
    vote_factory = RangeVote
    templates = {
        'detail': 'novaideo:views/templates/vote/rangevoting_type_detail.pt',
        'result': 'novaideo:views/templates/vote/rangevoting_type_result.pt',}

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

    def __init__(self, ballottype, electors, subjects, **kwargs):
        kwargs['subjects'] = subjects
        kwargs['electors'] = electors
        super(Report, self).__init__(**kwargs)
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

    def __init__(self, **kwargs):
        super(BallotBox, self).__init__(**kwargs)
        self.vote_len = 0

    def addtoproperty(self, name, value, moving=None):
        super(BallotBox, self).addtoproperty(name, value, moving)
        if name == 'votes':
            self.vote_len += 1


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
    initiator = SharedUniqueProperty('initiator')
    subjects = SharedMultipleProperty('subjects')

    def __init__(self, ballot_type, electors, contexts, duration, **kwargs):
        super(Ballot, self).__init__(**kwargs)
        kwargs.pop('subjects', None)
        self.setproperty('ballot_box', BallotBox())
        self.setproperty('report', Report(ballot_type,
                                          electors,
                                          contexts,
                                          **kwargs))
        self.run_at = None
        self.duration = duration
        self.finished_at = None
        self.period_validity = kwargs.get(
            'period_validity', None)
        self.group = kwargs.get(
            'group', DEFAULT_BALLOT_GROUP)
        self.uid = uuid.uuid4().hex
        self.__name__ = self.uid

    @property
    def group_id(self):
        return self.group.get('group_id', None)

    @property
    def is_finished(self):
        if 'finished' in self.state:
            return True

        now = datetime.datetime.now(tz=pytz.UTC)
        if now > self.finished_at:
            self.state.append('finished')
            return True

        return False

    @property
    def decision_is_valide(self):
        if 'expired' in self.state:
            return False

        if self.period_validity is None:
            return True

        now = datetime.datetime.now(tz=pytz.UTC)
        end_decision = self.finished_at + self.period_validity
        if now > end_decision:
            self.state.append('expired')
            return False

        return True

    def finish_ballot(self):
        if 'finished' not in self.state:
            self.finished_at = datetime.datetime.now(tz=pytz.UTC)
            self.state = PersistentList(['finished'])

    def run_ballot(self, context=None):
        """Run the ballot"""
        self.run_at = datetime.datetime.now(tz=pytz.UTC)
        self.finished_at = self.run_at + self.duration
        return self.report.ballottype.run_ballot(context)
