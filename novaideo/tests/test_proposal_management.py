# -*- coding: utf-8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen SOUISSI

"""Tests for proposal management
"""

from novaideo.testing import FunctionalTests
from novaideo.views.novaideo_view_manager.see_ordered_proposals import (
    sort_proposals)


class Proposal(object):
	pass


class TestProposalManagement(FunctionalTests): #pylint: disable=R0904
    """Test TestProposalManagement"""

    def test_sort_proposal(self):
        proposal1 = Proposal()
        proposal1.tokens_support = [1, 1, 1] #+3
        proposal1.tokens_opposition = [1, 1] #-2

        proposal2 = Proposal()
        proposal2.tokens_support = [1, 1, 1, 1]#+4
        proposal2.tokens_opposition = [1, 1, 1]#-3

        proposal3 = Proposal()
        proposal3.tokens_support = [1, 1]#+2
        proposal3.tokens_opposition = [1, 1]#-2

        proposal4 = Proposal()
        proposal4.tokens_support = [1, 1, 1, 1]#+4
        proposal4.tokens_opposition = [1, 1, 1, 1, 1]#-5

        proposals = [proposal3, proposal2, proposal4, proposal1]
        ordered_proposals = sort_proposals(proposals)
        self.assertEqual(len(ordered_proposals), 4)
        self.assertIn(proposal1, ordered_proposals)
        self.assertIn(proposal2, ordered_proposals)
        self.assertIn(proposal3, ordered_proposals)
        self.assertIn(proposal4, ordered_proposals)
        self.assertEqual(ordered_proposals.index(proposal2), 0)
        self.assertEqual(ordered_proposals.index(proposal1), 1)
        self.assertEqual(ordered_proposals.index(proposal3), 2)
        self.assertEqual(ordered_proposals.index(proposal4), 3)
