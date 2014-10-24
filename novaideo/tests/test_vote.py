# -*- coding: utf-8 -*-
"""Tests for vote, vote calculation & results, vote decisions
"""

from novaideo.testing import FunctionalTests
from novaideo.content.ballot import ReferendumVote, Report
from novaideo.tests.example.app import SubjectType, User

class TestVoteIntegration(FunctionalTests): #pylint: disable=R0904
    """Test Vote integration"""


    def setUp(self):
        super(TestVoteIntegration, self).setUp()
        self.user1 = self.root['principals']['users']['user1'] = User()
        self.user2 = self.root['principals']['users']['user2'] = User()
        self.user3 = self.root['principals']['users']['user3'] = User()
        self.user4 = self.root['principals']['users']['user4'] = User()
        self.root['subject1'] = SubjectType()
        self.root['subjetc2'] = SubjectType()
        self.root['subject3'] = SubjectType()
        self.root['subject4'] = SubjectType()
        users = [self.user1, self.user2, self.user3, self.user4];
        subjects =[self.root['subject1']]
        report = Report('Referendum',users, subjects)
        self.vote_type = report.ballottype

    def test_referendum_equality(self):
        vote1 = ReferendumVote(True)
        vote2 = ReferendumVote(False)
        votes = [vote1, vote2]
        result = self.vote_type.calculate_votes(votes)
        self.assertEqual(result['True'], 1)
        self.assertEqual(result['None'], 0)
        self.assertEqual(result['False'], 1)
        electeds = self.vote_type.get_electeds(result)
        self.assertEqual(electeds, None)

    def test_referendum_majority_false(self):
        vote1 = ReferendumVote(False)
        vote2 = ReferendumVote(False)
        votes = [vote1, vote2]
        result = self.vote_type.calculate_votes(votes)
        self.assertEqual(result['True'], 0)
        self.assertEqual(result['None'], 0)
        self.assertEqual(result['False'], 2)
        electeds = self.vote_type.get_electeds(result)
        self.assertEqual(electeds, False)

    def test_referendum_majority_True(self):
        vote1 = ReferendumVote(True)
        vote2 = ReferendumVote(True)
        votes = [vote1, vote2]
        result = self.vote_type.calculate_votes(votes)
        self.assertEqual(result['True'], 2)
        self.assertEqual(result['None'], 0)
        self.assertEqual(result['False'], 0)
        electeds = self.vote_type.get_electeds(result)
        self.assertEqual(electeds, True)




# def test_MajorityJudgment(self):

# def test_FPTP(self):
