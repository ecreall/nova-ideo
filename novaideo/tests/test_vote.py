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
        self.root['subject1'] = SubjectType()
        self.root['subjetc2'] = SubjectType()
        self.root['subject3'] = SubjectType()
        self.root['subject4'] = SubjectType()

    def test_Referendum(self):
        # Pour chaque type de vote, tester calculate et get_elected.
        users = [self.user1, self.user2];
        subjects=[self.root['subject1']]
        report  = Report('Referendum',users, subjects)
        vote_type = report.ballottype
        vote1 = ReferendumVote(True)
        vote2 = ReferendumVote(False)
        votes=[vote1, vote2]
        result = vote_type.calculate_votes(votes)
        self.assertEqual(result['True'], 1)
        self.assertEqual(result['None'], 0)
        self.assertEqual(result['False'], 1)
        electeds = vote_type.get_electeds(result)
        self.assertEqual(electeds, None)


# def test_MajorityJudgment(self):

# def test_FPTP(self):
