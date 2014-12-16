# -*- coding: utf-8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Sophie Jazwiecki

"""Tests for vote, vote calculation & results, vote decisions
"""

from novaideo.testing import FunctionalTests
from novaideo.content.ballot import (
    ReferendumVote, 
    Report, 
    FPTPVote, 
    MajorityJudgmentVote)
from novaideo.tests.example.app import SubjectType, User
from substanced.util import get_oid


class TestVoteIntegration(FunctionalTests): #pylint: disable=R0904
    """Test Vote integration"""


    def setUp(self):
        super(TestVoteIntegration, self).setUp()
        self.user1 = self.root['principals']['users']['user1'] = User()
        self.user2 = self.root['principals']['users']['user2'] = User()
        self.user3 = self.root['principals']['users']['user3'] = User()
        self.user4 = self.root['principals']['users']['user4'] = User()
        self.subject1 = self.root['subject1'] = SubjectType(title='subject1')
        self.subject2 = self.root['subject2'] = SubjectType(title='subject2')
        self.subject3 = self.root['subject3'] = SubjectType(title='subject3')
        self.subject4 = self.root['subject4'] = SubjectType(title='subject4')
        self.oid_subject1 = get_oid(self.subject1)
        self.oid_subject2 = get_oid(self.subject2)
        self.oid_subject3 = get_oid(self.subject3)
        self.oid_subject4 = get_oid(self.subject4)

    def init_referendum_tests(self):
        electors = [self.user1, self.user2, self.user3, self.user4]
        subjects = [self.root['subject1']]
        report = Report('Referendum', electors, subjects)
        self.vote_type = report.ballottype

    def test_referendum_majority_false(self):
        # Pour chaque type de vote, tester calculate et get_elected.
        self.init_referendum_tests()
        vote1 = ReferendumVote(False)
        vote2 = ReferendumVote(False)
        vote3 = ReferendumVote(True)
        vote4 = ReferendumVote(False)
        votes = [vote1, vote2, vote3, vote4]
        result = self.vote_type.calculate_votes(votes)
        self.assertEqual(result['True'], 1)
        self.assertEqual(result['None'], 0)
        self.assertEqual(result['False'], 3)
        electeds = self.vote_type.get_electeds(result)
        self.assertEqual(electeds, None)

    def test_referendum_majority_True(self):
        self.init_referendum_tests()
        vote1 = ReferendumVote(True)
        vote2 = ReferendumVote(True)
        vote3 = ReferendumVote(None)
        vote4 = ReferendumVote(False)
        votes = [vote1, vote2, vote3, vote4]
        result = self.vote_type.calculate_votes(votes)
        self.assertEqual(result['True'], 2)
        self.assertEqual(result['None'], 1)
        self.assertEqual(result['False'], 1)
        electeds = self.vote_type.get_electeds(result)
        self.assertEqual(electeds[0].title, 'subject1')

    def test_referendum_equality(self):
        self.init_referendum_tests()
        vote1 = ReferendumVote(True)
        vote2 = ReferendumVote(False)
        vote3 = ReferendumVote(True)
        vote4 = ReferendumVote(False)
        votes = [vote1, vote2, vote3, vote4]
        result = self.vote_type.calculate_votes(votes)
        self.assertEqual(result['True'], 2)
        self.assertEqual(result['None'], 0)
        self.assertEqual(result['False'], 2)
        electeds = self.vote_type.get_electeds(result)
        self.assertEqual(electeds, None)

    def init_FPTP_tests(self):
        electors = [self.user1, self.user2, self.user3, self.user4]
        subjects = [self.root['subject1'], self.root['subject2'], 
                    self.root['subject3'], self.root['subject4']]
        report = Report('FPTP', electors, subjects)
        self.vote_type = report.ballottype

    def test_FPTP_subject1_elected(self):
        self.init_FPTP_tests()
        vote1 = FPTPVote(self.root['subject1'])
        vote2 = FPTPVote(self.root['subject1'])
        vote3 = FPTPVote(self.root['subject2'])
        vote4 = FPTPVote(self.root['subject3'])
        votes = [vote1, vote2, vote3, vote4]
        result = self.vote_type.calculate_votes(votes)
        self.assertEqual(result[self.oid_subject1], 2)
        self.assertEqual(result[self.oid_subject2], 1)
        self.assertEqual(result[self.oid_subject3], 1)
        electeds = self.vote_type.get_electeds(result)
        self.assertEqual(electeds[0].title, 'subject1')

    def test_FPTP_subject2_elected(self):
        self.init_FPTP_tests()
        vote1 = FPTPVote(self.root['subject1'])
        vote2 = FPTPVote(self.root['subject2'])
        vote3 = FPTPVote(self.root['subject2'])
        vote4 = FPTPVote(self.root['subject3'])
        votes = [vote1, vote2, vote3, vote4]
        result = self.vote_type.calculate_votes(votes)
        self.assertEqual(result[self.oid_subject1], 1)
        self.assertEqual(result[self.oid_subject2], 2)
        self.assertEqual(result[self.oid_subject3], 1)
        electeds = self.vote_type.get_electeds(result)
        self.assertEqual(electeds[0].title, 'subject2')

    def test_FPTP_equality(self):
        self.init_FPTP_tests()
        vote1 = FPTPVote(self.root['subject4'])
        vote2 = FPTPVote(self.root['subject3'])
        vote3 = FPTPVote(self.root['subject1'])
        vote4 = FPTPVote(self.root['subject2'])
        votes = [vote1, vote2, vote3, vote4]
        result = self.vote_type.calculate_votes(votes)
        self.assertEqual(result[self.oid_subject1], 1)
        self.assertEqual(result[self.oid_subject2], 1)
        self.assertEqual(result[self.oid_subject3], 1)
        self.assertEqual(result[self.oid_subject4], 1)
        electeds = self.vote_type.get_electeds(result)
        self.assertEqual(len(electeds), 1)        
        self.assertIn(electeds[0], self.vote_type.report.subjects)

    def test_FPTP_more_votes_than_users(self):
        self.init_FPTP_tests()
        vote1 = FPTPVote(self.root['subject4'])#+1
        vote2 = FPTPVote(self.root['subject3'])
        vote3 = FPTPVote(self.root['subject1'])
        vote4 = FPTPVote(self.root['subject2'])
        vote5 = FPTPVote(self.root['subject4'])#+1
        votes = [vote1, vote2, vote3, vote4, vote5]
        result = self.vote_type.calculate_votes(votes)
        electeds = self.vote_type.get_electeds(result)
        self.assertEqual(len(electeds), 1)
        self.assertIn(self.root['subject4'], electeds)

    def init_majority_judgment_tests(self):
        electors = [self.user1, self.user2, self.user3, self.user4]
        subjects = [self.root['subject1'], self.root['subject2'],
                    self.root['subject3']]
        report = Report('MajorityJudgment', electors, subjects)
        self.vote_type = report.ballottype
        return report

    def test_MajorityJudgment_one_subject(self):
        report = self.init_majority_judgment_tests()
        report.setproperty('voters', report.electors) # add voters
        vote1 = MajorityJudgmentVote({self.oid_subject1: 'Very good'})
        vote2 = MajorityJudgmentVote({self.oid_subject1: 'Insufficient'})
        vote3 = MajorityJudgmentVote({self.oid_subject1: 'Good'})
        vote4 = MajorityJudgmentVote({self.oid_subject1: 'Good'})
        votes = [vote1, vote2, vote3, vote4]
        result = self.vote_type.calculate_votes(votes)
        self.assertEqual(result[self.oid_subject1]['Very good'], 1)
        self.assertEqual(result[self.oid_subject1]['Insufficient'], 1)
        self.assertEqual(result[self.oid_subject1]['Good'], 2)
        electeds = self.vote_type.get_electeds(result)
        self.assertEqual(len(electeds), 1)
        self.assertIn(self.root['subject1'], electeds)

    def test_MajorityJudgment_Equality(self):
        report = self.init_majority_judgment_tests()
        report.setproperty('voters', report.electors)
        vote1 = MajorityJudgmentVote({self.oid_subject1: 'Fairly well', 
                                      self.oid_subject2: 'Fairly well', 
                                      self.oid_subject3: 'Good'})
        vote2 = MajorityJudgmentVote({self.oid_subject1: 'Fairly well', 
                                      self.oid_subject2: 'Very good', 
                                      self.oid_subject3: 'Good'})
        vote3 = MajorityJudgmentVote({self.oid_subject1: 'Good', 
                                      self.oid_subject2: 'Passable', 
                                      self.oid_subject3: 'Fairly well'})
        vote4 = MajorityJudgmentVote({self.oid_subject1: 'Good', 
                                      self.oid_subject2: 'Passable', 
                                      self.oid_subject3: 'Fairly well'})
        votes = [vote1, vote2, vote3, vote4]
        result = self.vote_type.calculate_votes(votes)
        self.assertEqual(result[self.oid_subject1]['Good'], 2)
        self.assertEqual(result[self.oid_subject1]['Fairly well'], 2)
        self.assertEqual(result[self.oid_subject2]['Fairly well'], 1)
        self.assertEqual(result[self.oid_subject2]['Very good'], 1)
        self.assertEqual(result[self.oid_subject2]['Passable'], 2)
        self.assertEqual(result[self.oid_subject3]['Good'], 2)
        self.assertEqual(result[self.oid_subject3]['Fairly well'], 2)
        electeds = self.vote_type.get_electeds(result)
        self.assertEqual(len(electeds), 1)
        self.assertIn(electeds[0], [self.root['subject1'], 
                                    self.root['subject3']])

    def test_MajorityJudgment_several_subjects(self):
        report = self.init_majority_judgment_tests()
        report.setproperty('voters', report.electors)
        vote1 = MajorityJudgmentVote({self.oid_subject1: 'Very good', 
                                      self.oid_subject2: 'Very good', 
                                      self.oid_subject3: 'Fairly well'})
        vote2 = MajorityJudgmentVote({self.oid_subject1: 'Insufficient', 
                                      self.oid_subject2: 'Very good', 
                                      self.oid_subject3: 'Reject'})
        vote3 = MajorityJudgmentVote({self.oid_subject1: 'Good', 
                                      self.oid_subject2: 'Passable', 
                                      self.oid_subject3: 'Fairly well'})
        vote4 = MajorityJudgmentVote({self.oid_subject1: 'Good', 
                                      self.oid_subject2: 'Passable', 
                                      self.oid_subject3: 'Fairly well'})
        votes = [vote1, vote2, vote3, vote4]
        result = self.vote_type.calculate_votes(votes)
        self.assertEqual(result[self.oid_subject1]['Very good'], 1)
        self.assertEqual(result[self.oid_subject1]['Insufficient'], 1)
        self.assertEqual(result[self.oid_subject1]['Good'], 2) #Median 16
        self.assertEqual(result[self.oid_subject2]['Very good'], 2)
        self.assertEqual(result[self.oid_subject2]['Insufficient'], 0)
        self.assertEqual(result[self.oid_subject2]['Good'], 0)
        self.assertEqual(result[self.oid_subject2]['Passable'], 2)#Median 12
        self.assertEqual(result[self.oid_subject3]['Very good'], 0)
        self.assertEqual(result[self.oid_subject3]['Insufficient'], 0)
        self.assertEqual(result[self.oid_subject3]['Good'], 0)
        self.assertEqual(result[self.oid_subject3]['Fairly well'], 3)
        self.assertEqual(result[self.oid_subject3]['Reject'], 1)
        electeds = self.vote_type.get_electeds(result)
        self.assertEqual(len(electeds), 1)
        self.assertIn(self.root['subject1'], electeds)

    def test_MajorityJudgment_unanimity(self):
        report = self.init_majority_judgment_tests()
        report.setproperty('voters', report.electors)
        vote1 = MajorityJudgmentVote({self.oid_subject1: 'Good', 
                                      self.oid_subject2: 'Very good', 
                                      self.oid_subject3: 'Fairly well'})
        vote2 = MajorityJudgmentVote({self.oid_subject1: 'Insufficient', 
                                      self.oid_subject2: 'Very good', 
                                      self.oid_subject3: 'Reject'})
        vote3 = MajorityJudgmentVote({self.oid_subject1: 'Good', 
                                      self.oid_subject2: 'Very good', 
                                      self.oid_subject3: 'Fairly well'})
        vote4 = MajorityJudgmentVote({self.oid_subject1: 'Good', 
                                      self.oid_subject2: 'Very good', 
                                      self.oid_subject3: 'Fairly well'})
        votes = [vote1, vote2, vote3, vote4]
        result = self.vote_type.calculate_votes(votes)
        self.assertEqual(result[self.oid_subject1]['Very good'], 0)
        self.assertEqual(result[self.oid_subject1]['Insufficient'], 1)
        self.assertEqual(result[self.oid_subject1]['Good'], 3)
        self.assertEqual(result[self.oid_subject2]['Very good'], 4)
        self.assertEqual(result[self.oid_subject3]['Very good'], 0)
        self.assertEqual(result[self.oid_subject3]['Good'], 0)
        self.assertEqual(result[self.oid_subject3]['Fairly well'], 3)
        self.assertEqual(result[self.oid_subject3]['Reject'], 1)
        electeds = self.vote_type.get_electeds(result)
        self.assertEqual(len(electeds), 1)
        self.assertIn(self.root['subject2'], electeds)
