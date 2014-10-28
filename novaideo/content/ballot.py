import colander
import datetime
from persistent.list import PersistentList
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer, get_oid
from dace.objectofcollaboration.principal.util import grant_roles
from dace.objectofcollaboration.entity import Entity
from dace.util import find_service, get_obj
from dace.descriptors import (
        CompositeUniqueProperty,
        CompositeMultipleProperty,
        SharedUniqueProperty,
        SharedMultipleProperty)
from pontus.widget import RichTextWidget
from pontus.core import VisualisableElement, VisualisableElementSchema

from .interface import IVote, IBallotType, IReport, IBallot, IBallotBox
from novaideo import _


@content(
    'referendumvote',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IVote)
class ReferendumVote(VisualisableElement, Entity):
    name = renamer()

    def __init__(self, value=None, **kwargs):
        super(ReferendumVote, self).__init__(**kwargs)
        self.value = value


@implementer(IBallotType)
class Referendum(object):
    vote_factory = ReferendumVote

    def __init__(self, report, vote_process_id='referendumprocess'):
        self.vote_process_id = vote_process_id
        self.report = report
        if isinstance(self.report.subjects, (list, tuple, PersistentList)):
            self.subject = self.report.subjects[0]
        else:
            self.subject =  self.report.subjects

    def run_ballot(self, context=None):
        processes = []
        def_container = find_service('process_definition_container')
        runtime = find_service('runtime')
        pd = def_container.get_definition(self.vote_process_id)
        if context is None:
            context = self.subject

        for elector in self.report.electors:
            proc = pd()
            proc.__name__ = proc.id
            runtime.addtoproperty('processes', proc)
            proc.defineGraph(pd)
            proc.execution_context.add_involved_entity('elector', elector)
            proc.execution_context.add_involved_entity('subject', context)
            grant_roles(elector, (('Elector', proc),))
            proc.ballot = self.report.ballot
            proc.execute()
            processes.append(proc)

        return processes

    def calculate_votes(self, votes):
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
        if result['True'] > result['False']:
            return [self.subject]

        return None


default_judgments = {'Excellent': 7,
                     'Very good': 6,
                     'Good': 5,
                     'Fairly well': 4,
                     'Passable': 3,
                     'Insufficient': 2,
                     'Reject': 1}


@content(
    'majorityjudgmentvote',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IVote)
class MajorityJudgmentVote(VisualisableElement, Entity):
    name = renamer()

    def __init__(self, value=None, **kwargs):
        super(MajorityJudgmentVote, self).__init__(**kwargs)
        self.value = value
        #value  = {objectoid: 'Judgment', ...}


@implementer(IBallotType)
class MajorityJudgment(object):
    vote_factory = MajorityJudgmentVote

    def __init__(self, report, vote_process_id='majorityjudgmentprocess'):
        self.vote_process_id = vote_process_id
        self.report = report
        self.judgments = default_judgments

    def run_ballot(self, context=None):
        processes = []
        def_container = find_service('process_definition_container')
        runtime = find_service('runtime')
        pd = def_container.get_definition(self.vote_process_id)
        if context is None:
            context = self.report.subjects[0].__parent__

        for elector in self.report.electors:
            proc = pd()
            proc.__name__ = proc.id
            runtime.addtoproperty('processes', proc)
            proc.defineGraph(pd)
            proc.execution_context.add_involved_entity('elector', elector)
            proc.execution_context.add_involved_entity('subject', context)
            grant_roles(elector, (('Elector', proc),))
            proc.ballot = self.report.ballot
            proc.execute()
            processes.append(proc)

        return processes

    def calculate_votes(self, votes):
        result = {}
        for subject in self.report.subjects:
            oid = get_oid(subject)
            result[oid] = {}
            for judgment in self.judgments.keys():
                result[oid][judgment] = 0

        for vote in votes:
            for oid, judgment in vote.value.items():
                object = get_obj(oid)
                if object in self.report.subjects:
                    result[oid][judgment] += 1

        return result

    def get_electeds(self, result):
        len_voters = len(self.report.voters)
        if len_voters == 0:
            return None

        judgments = sorted(list(self.judgments.keys()), key=lambda o: self.judgments[o])
        object_results = dict([(oid, 0) for oid in result.keys()])
        for oid in result.keys():
            object_result = 0
            for judgment in judgments:
                object_result += float(result[oid][judgment]) / float(len_voters) * 100
                if object_result >= 50:
                    object_results[oid] = self.judgments[judgment]
                    break

        sorted_results = sorted(list(object_results.keys()), key=lambda o: object_results[o], reverse=True)
        if sorted_results:
            try:
                object = get_obj(sorted_results[0])
                return [object]
            except Exception:
                return None

        return None


@content(
    'fptpvote',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IVote)
class FPTPVote(VisualisableElement, Entity):
    name = renamer()

    def __init__(self, value=None, **kwargs):
        super(FPTPVote, self).__init__(**kwargs)
        self.value = value
        #value  = object


@implementer(IBallotType)
class FPTP(object):
    vote_factory = FPTPVote

    def __init__(self, report, vote_process_id='fptpprocess'):
        self.vote_process_id = vote_process_id
        self.report = report

    def run_ballot(self, context=None):
        processes = []
        def_container = find_service('process_definition_container')
        runtime = find_service('runtime')
        pd = def_container.get_definition(self.vote_process_id)
        if context is None:
            context = self.report.subjects[0].__parent__

        for elector in self.report.electors:
            proc = pd()
            proc.__name__ = proc.id
            runtime.addtoproperty('processes', proc)
            proc.defineGraph(pd)
            proc.execution_context.add_involved_entity('elector', elector)
            proc.execution_context.add_involved_entity('subject', context)
            grant_roles(elector, (('Elector', proc),))
            proc.ballot = self.report.ballot
            proc.execute()
            processes.append(proc)

        return processes

    def calculate_votes(self, votes):
        result = {}
        for subject in self.report.subjects:
            try:
                id = get_oid(subject)
            except Exception:
                id = subject

            result[id] = 0

        for vote in votes:
            object = get_obj(vote.value)
            if object is None:
                object = vote.value

            id = get_oid(vote.value)
            if object in self.report.subjects:
                    result[id] += 1

        return result

    def get_electeds(self, result):
        electeds_ids = sorted(list(result.keys()), key=lambda o: result[o], reverse=True)
        electeds = []
        if electeds_ids:
            elected_id = electeds_ids[0]
            elected = get_obj(elected_id)
            if elected is None:
                elected = elected_id

            return [elected]

        return None

ballot_types = {'Referendum': Referendum,
                'MajorityJudgment': MajorityJudgment,
                'FPTP': FPTP} #TODO add ballot types


@content(
    'report',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IReport)
class Report(VisualisableElement, Entity):
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
        self.ballottype = ballot_types[ballottype](self)
        if 'vote_process_id' in kwargs:
            self.ballottype.vote_process_id = kwargs['vote_process_id']

        self.result = None
        self.calculated = False

    def calculate_votes(self):
        if not self.calculated:
            votes = self.ballot.ballot_box.votes
            self.result = self.ballottype.calculate_votes(votes)
            self.calculated = True
        else:
            return self.result

    def get_electeds(self):
        if not self.calculated:
            self.calculate_votes()

        return self.ballottype.get_electeds(self.result)


@content(
    'ballotbox',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IBallotBox)
class BallotBox(VisualisableElement, Entity):
    name = renamer()
    votes = CompositeMultipleProperty('votes')


@content(
    'ballot',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IBallot)
class Ballot(VisualisableElement, Entity):
    name = renamer()
    ballot_box = CompositeUniqueProperty('ballot_box')
    report = CompositeUniqueProperty('report', 'ballot')

    def __init__(self, ballot_type , electors, subjects, duration,**kwargs):
        super(Ballot, self).__init__(**kwargs)
        self.setproperty('ballot_box', BallotBox())
        self.setproperty('report', Report(ballottype=ballot_type, electors=electors, subjects=subjects))
        self.run_at = None
        self.duration = duration
        self.finished_at = None

    def run_ballot(self, context=None):
        processes = self.report.ballottype.run_ballot(context)
        self.run_at = datetime.datetime.today()
        self.finished_at = self.run_at + self.duration
        return processes


