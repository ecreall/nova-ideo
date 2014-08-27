import colander
import datetime
from persistent.list import PersistentList
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer
from dace.objectofcollaboration.principal.util import grant_roles
from dace.objectofcollaboration.entity import Entity
from dace.util import find_service
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
    'vote',
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
    vote_process_id = 'referendumprocess'

    def __init__(self, report):
        self.report = report
        if isinstance(self.report.subjects, (list, tuple, PersistentList)):
            self.subject = self.report.subjects[0]
        else:
            self.subject =  self.report.subjects

    def run_ballot(self):
        processes = []
        def_container = find_service('process_definition_container')
        runtime = find_service('runtime')
        pd = def_container.get_definition(self.vote_process_id)
        for elector in self.report.electors:
            proc = pd()
            proc.__name__ = proc.id
            runtime.addtoproperty('processes', proc)
            proc.defineGraph(pd)
            proc.execution_context.add_involved_entity('elector', elector)
         
            proc.execution_context.add_involved_entity('subject', self.subject)
            grant_roles(elector, (('Elector', proc),))
            proc.ballot = self.report.ballot
            proc.execute()
            processes.append(proc)

        #TODO run processes referendumprocess pour chaque elector su
        return processes

    def calculate_votes(self, votes):
        result = {'True':0, 'False':0, 'None':0}
        for vote in votes:
            if vote is True:
                self.result['True'] += 1
            elif vote is False:
                self.result['False'] += 1
            else:
                self.result['None'] += 1

        return result

    def get_electeds(self, result):
        if result['True'] > result['False']:
            return [self.subject]

        return None


ballot_types = {'Referendum': Referendum}


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
        self.ballot = ballot_types[ballottype](self)
        self.result = None
        self.calculated = False

    def calculate_votes(self):
        if not self.calculated:
            votes = self.ballot.ballot_box.votes
            self.result = self.ballot.calculate_votes(votes)
            self.calculated = True
        else:
            return self.result

    def get_electeds(self):
        return self.ballot.get_electeds(self.result)


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

    def run_ballot(self):
        processes = self.report.ballot.run_ballot()
        self.run_at = datetime.datetime.today()
        return processes


