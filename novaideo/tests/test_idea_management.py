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

    def create_idea(self):
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
        create_action = actions[0]
        # Excute the action
        create_action.execute(
            context, self.request, {'_object_data': idea})
        ideas = context.ideas
        return ideas[0]

    def test_create_idea_default_conf(self):
        # SetUp the default Nova-Ideo configuration
        self.default_novaideo_config()
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
        create_action = actions[0]
        self.assertEqual(create_action.node_id, 'creat')
        self.assertEqual(create_action.process_id, 'ideamanagement')
        # Execute the action
        create_action.execute(
            context, self.request, {'_object_data': idea})
        ideas = context.ideas
        self.assertEqual(len(ideas), 1)
        idea_result = ideas[0]
        self.assertIs(idea_result, idea)
        self.assertIs(idea_result.author, self.request.user)
        self.assertIn('to work', idea_result.state)
        # Test the merge of keywords
        self.assertEqual(len(context.keywords), 0)
        # Test if we have a single action
        actions = getAllBusinessAction(
            context, self.request,
            process_id='ideamanagement',
            node_id='creat')
        self.assertEqual(len(actions), 1)
        # Can publish
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        expected_actions = [
            'duplicate', 'edit',
            'publish', 'abandon',
            'associate', 'see']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 6)
        self.assertTrue(all(a in expected_actions
                            for a in actions_ids))

    def test_create_and_publish_idea_default_conf(self):
        # SetUp the default Nova-Ideo configuration
        self.default_novaideo_config()
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
        create_action = actions[0]
        self.assertEqual(create_action.node_id, 'creatandpublish')
        self.assertEqual(create_action.process_id, 'ideamanagement')
        # Execute the action
        create_action.execute(
            context, self.request, {'_object_data': idea})
        ideas = context.ideas
        self.assertEqual(len(ideas), 1)
        idea_result = ideas[0]
        self.assertIs(idea_result, idea)
        self.assertIs(idea_result.author, self.request.user)
        self.assertIn('published', idea_result.state)
        # Test the merge of keywords
        self.assertEqual(len(context.keywords), 2)
        self.assertIn('keyword 1', context.keywords)
        self.assertIn('keyword 2', context.keywords)
        # Test if we have a single action
        actions = getAllBusinessAction(
            context, self.request,
            process_id='ideamanagement',
            node_id='creatandpublish')
        self.assertEqual(len(actions), 1)
        # Can't publish
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        # User == sd Admin (No tokens, he can't support)
        expected_actions = [
            'seeworkinggroups', 'duplicate',
            'comment', 'present', 'associate',
            'see', 'moderationarchive']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 7)
        self.assertTrue(all(a in expected_actions
                            for a in actions_ids))

    def test_create_idea_moderation_conf(self):
        # SetUp the 'moderation' Nova-Ideo configuration
        self.moderation_novaideo_config()
        idea_result = self.create_idea()
        self.assertIn('to work', idea_result.state)
        # can submit, can't publish
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        expected_actions = [
            'duplicate', 'edit', 'abandon',
            'associate', 'see', 'submit']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 6)
        self.assertTrue(all(a in expected_actions
                            for a in actions_ids))

    def test_submit_idea_moderation_conf(self):
        # SetUp the 'moderation' Nova-Ideo configuration
        self.moderation_novaideo_config()
        idea_result = self.create_idea()
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement',
            node_id='submit')
        # Submit the idea
        submit_action = actions[0]
        submit_action.execute(
            idea_result, self.request, {})
        self.assertIn('submitted', idea_result.state)
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        expected_actions = [
            'duplicate', 'associate', 'see',
            'publish_moderation', 'archive']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 5)
        self.assertTrue(all(a in expected_actions
                            for a in actions_ids))

    def test_publish_idea_moderation_conf(self):
        # SetUp the 'moderation' Nova-Ideo configuration
        self.moderation_novaideo_config()
        idea_result = self.create_idea()
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement',
            node_id='submit')
        # Submit the idea
        submit_action = actions[0]
        submit_action.execute(
            idea_result, self.request, {})
        # Publish the idea
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement',
            node_id='publish_moderation')
        publish_action = actions[0]
        publish_action.execute(
            idea_result, self.request, {})
        self.assertIn('submitted_support', idea_result.state)
        self.assertIn('published', idea_result.state)
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        # User == sd Admin (No tokens, he can't support)
        expected_actions = [
            'seeworkinggroups', 'duplicate',
            'comment', 'present', 'associate',
            'see', 'moderationarchive']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 7)
        self.assertTrue(all(a in expected_actions
                            for a in actions_ids))
