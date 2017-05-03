# -*- coding: utf-8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen SOUISSI

"""Tests for Idea management process
"""

from dace.util import getAllBusinessAction

from novaideo.testing import FunctionalTests
from novaideo.content.idea import Idea


class TestIdeaManagement(FunctionalTests): #pylint: disable=R0904
    """Test Vote integration"""

    def setUp(self):
        super(TestIdeaManagement, self).setUp()

    def test_creat_idea_default_conf(self):
        # SetUp the default Nova-Ideo configuration
        self.default_request_setUp()
        context = self.request.root
        idea = Idea(
            title="Idea title",
            text="Idea text",
            keywords=["keyword 1", "keyword 2"])
        # Find the 'creat' action of the idea management process
        actions = getAllBusinessAction(
            context, self.request,
            process_id='ideamanagement',
            node_id='creat')
        self.assertEqual(len(actions), 1)
        creat_action = actions[0]
        self.assertEqual(creat_action.node_id, 'creat')
        self.assertEqual(creat_action.process_id, 'ideamanagement')
        # Excute the action
        creat_action.execute(
            context, self.request, {'_object_data': idea})
        ideas = context.ideas
        self.assertEqual(len(ideas), 1)
        idea_result = ideas[0]
        self.assertIs(idea_result, idea)
        self.assertIs(idea_result.author, self.request.user)
        self.assertIn('to work', idea_result.state)
        # Test if we have a single action
        actions = getAllBusinessAction(
            context, self.request,
            process_id='ideamanagement',
            node_id='creat')
        self.assertEqual(len(actions), 1)

    def test_creat_and_publish_idea_default_conf(self):
        # SetUp the default Nova-Ideo configuration
        self.default_request_setUp()
        context = self.request.root
        idea = Idea(
            title="Idea title",
            text="Idea text",
            keywords=["keyword 1", "keyword 2"])
        # Find the 'creat' action of the idea management process
        actions = getAllBusinessAction(
            context, self.request,
            process_id='ideamanagement',
            node_id='creatandpublish')
        self.assertEqual(len(actions), 1)
        creat_action = actions[0]
        self.assertEqual(creat_action.node_id, 'creatandpublish')
        self.assertEqual(creat_action.process_id, 'ideamanagement')
        # Excute the action
        creat_action.execute(
            context, self.request, {'_object_data': idea})
        ideas = context.ideas
        self.assertEqual(len(ideas), 1)
        idea_result = ideas[0]
        self.assertIs(idea_result, idea)
        self.assertIs(idea_result.author, self.request.user)
        self.assertIn('published', idea_result.state)
        # Test if we have a single action
        actions = getAllBusinessAction(
            context, self.request,
            process_id='ideamanagement',
            node_id='creatandpublish')
        self.assertEqual(len(actions), 1)
