# -*- coding: utf-8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen SOUISSI

"""Tests for Idea management process
"""
from substanced.util import get_oid

from dace.util import getAllBusinessAction

from novaideo.testing import FunctionalTests
from novaideo.content.idea import Idea
from novaideo.tests.example.app import add_user


class TestIdeaManagement(FunctionalTests): #pylint: disable=R0904
    """Test Idea management process"""

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
        # Owner actions
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
        # Other member actions
        alice = add_user({
            'first_name': 'Alice',
            'last_name': 'Alice'
        }, self.request)
        self.request.user = alice
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 0)

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
        # Other member actions
        alice = add_user({
            'first_name': 'Alice',
            'last_name': 'Alice'
        }, self.request)
        self.request.user = alice
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        expected_actions = [
            'seeworkinggroups', 'duplicate',
            'comment', 'present', 'associate',
            'see', 'support', 'oppose']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 8)
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
    def test_edit_idea(self):
        # SetUp the default Nova-Ideo configuration
        self.default_novaideo_config()
        alice = add_user({
            'first_name': 'Alice',
            'last_name': 'Alice'
        }, self.request)
        self.request.user = alice
        idea_result = self.create_idea()
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement',
            node_id='edit')
        # Edit the idea
        edit_action = actions[0]
        edit_action.execute(
            idea_result, self.request, {
                'title': 'Edited idea',
                'text': 'Edited idea text',
                'keywords': ['edit 1'],
                'attached_files': []
            })
        self.assertIn('to work', idea_result.state)
        self.assertEqual('Edited idea', idea_result.title)
        self.assertEqual('Edited idea text', idea_result.text)
        keywords = ['edit 1']
        self.assertTrue(all(a in keywords
                            for a in idea_result.keywords))
        # New version
        version = idea_result.version
        self.assertTrue(version is not None)
        self.assertIn('version', version.state)
        self.assertIn('archived', version.state)
        self.assertEqual('Idea title', version.title)
        self.assertEqual('Idea text', version.text)
        keywords = ["keyword 1", "keyword 2"]
        self.assertTrue(all(a in keywords
                            for a in version.keywords))
        # version actions
        actions = getAllBusinessAction(
            version, self.request,
            process_id='ideamanagement')
        expected_actions = ['duplicate', 'associate', 'see']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 3)
        self.assertTrue(all(a in expected_actions
                            for a in actions_ids))

    def test_abandon_recuperate_del_idea(self):
        # SetUp the default Nova-Ideo configuration
        self.default_novaideo_config()
        alice = add_user({
            'first_name': 'Alice',
            'last_name': 'Alice'
        }, self.request)
        self.request.user = alice
        idea_result = self.create_idea()
        self.assertEqual(len(alice.ideas), 1)
        self.assertEqual(len(alice.contents), 1)
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement',
            node_id='abandon')
        # abandon the idea
        abandon_action = actions[0]
        abandon_action.execute(
            idea_result, self.request, {})
        self.assertIn('archived', idea_result.state)
        # actions
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        expected_actions = ['delidea', 'recuperate', 'associate', 'see']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 4)
        self.assertTrue(all(a in expected_actions
                            for a in actions_ids))
        # recuperate
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement',
            node_id='recuperate')
        # recuperate the idea
        recuperate_action = actions[0]
        recuperate_action.execute(
            idea_result, self.request, {})
        self.assertIn('to work', idea_result.state)
        # abandon
        abandon_action.execute(
            idea_result, self.request, {})
        # delete
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement',
            node_id='delidea')
        # delete the idea
        delidea_action = actions[0]
        delidea_action.execute(
            idea_result, self.request, {})
        self.assertEqual(len(self.request.root.ideas), 0)
        self.assertEqual(len(alice.ideas), 0)
        self.assertEqual(len(alice.contents), 0)

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
        # Other member actions
        alice = add_user({
            'first_name': 'Alice',
            'last_name': 'Alice'
        }, self.request)
        self.request.user = alice
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 0)

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

    def test_create_and_publish_idea_moderation_conf(self):
        # SetUp the 'moderation' Nova-Ideo configuration
        self.moderation_novaideo_config()
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
        self.assertIn('submitted', idea_result.state)
        # Test the merge of keywords
        self.assertEqual(len(context.keywords), 0)
        # Admin (Owner) actions
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        # User == sd Admin (No tokens, he can't support)
        expected_actions = [
            'duplicate', 'associate', 'see',
            'publish_moderation', 'archive']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 5)
        self.assertTrue(all(a in expected_actions
                            for a in actions_ids))
        # Other member actions
        alice = add_user({
            'first_name': 'Alice',
            'last_name': 'Alice'
        }, self.request)
        self.request.user = alice
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 0)
    
    def test_support_no_support_novaideo_config(self):
        # SetUp the 'no_support' Nova-Ideo configuration
        self.no_support_novaideo_config()
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
        # Execute the action
        actions[0].execute(
            context, self.request, {'_object_data': idea})
        idea_result = context.ideas[0]
        # Members can't support the published idea
        alice = add_user({
            'first_name': 'Alice',
            'last_name': 'Alice'
        }, self.request)
        self.request.user = alice
        alice_oid = get_oid(alice)
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        expected_actions = [
            'seeworkinggroups', 'duplicate',
            'comment', 'present', 'associate', 'see']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 6)
        self.assertTrue(all(a in expected_actions
                            for a in actions_ids))
        

    def test_support_withdraw_oppose_idea(self):
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
        # Execute the action
        actions[0].execute(
            context, self.request, {'_object_data': idea})
        idea_result = context.ideas[0]
        # Other member actions
        alice = add_user({
            'first_name': 'Alice',
            'last_name': 'Alice'
        }, self.request)
        self.request.user = alice
        alice_oid = get_oid(alice)
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement',
            node_id='support')
        support_action = actions[0]
        support_action.execute(
            idea_result, self.request, {})
        self.assertEqual(idea_result.len_support, 1)
        self.assertIs(idea_result.tokens_support[0].owner, alice)
        self.assertEqual(idea_result.len_opposition, 0)
        self.assertEqual(len(alice.supports), 1)
        self.assertEqual(len(idea_result._support_history), 1)
        # _support_history = [(user_oid, date, type[1, 0, -1])]
        self.assertIs(idea_result._support_history[0][0], alice_oid)
        # 1 == support
        self.assertEqual(idea_result._support_history[0][2], 1)
        # Alice can't support. Alice can withdraw the token
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        expected_actions = [
            'seeworkinggroups', 'duplicate',
            'comment', 'present', 'associate',
            'see', 'withdraw_token']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 7)
        self.assertTrue(all(a in expected_actions
                            for a in actions_ids))
        # Withdraw
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement',
            node_id='withdraw_token')
        withdraw_token_action = actions[0]
        withdraw_token_action.execute(
            idea_result, self.request, {})
        self.assertEqual(idea_result.len_support, 0)
        self.assertEqual(idea_result.len_opposition, 0)
        self.assertEqual(len(alice.supports), 0)
        self.assertEqual(len(idea_result._support_history), 2)
        self.assertIs(idea_result._support_history[1][0], alice_oid)
        # -1 == withdraw
        self.assertEqual(idea_result._support_history[1][2], -1)
        # Alice can support and can oppose
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        expected_actions = [
            'seeworkinggroups', 'duplicate',
            'comment', 'present', 'associate',
            'see', 'support', 'oppose']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 8)
        self.assertTrue(all(a in expected_actions
                            for a in actions_ids))
        # oppose
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement',
            node_id='oppose')
        oppose_action = actions[0]
        oppose_action.execute(
            idea_result, self.request, {})
        self.assertEqual(idea_result.len_support, 0)
        self.assertEqual(idea_result.len_opposition, 1)
        self.assertEqual(len(alice.supports), 1)
        self.assertEqual(len(idea_result._support_history), 3)
        self.assertIs(idea_result._support_history[2][0], alice_oid)
        # 0 == oppose
        self.assertEqual(idea_result._support_history[2][2], 0)
        # Alice can't support and cant oppose. Alice can withdraw the token
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement')
        expected_actions = [
            'seeworkinggroups', 'duplicate',
            'comment', 'present', 'associate',
            'see', 'withdraw_token']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 7)
        self.assertTrue(all(a in expected_actions
                            for a in actions_ids))

    def test_duplicate(self):
        # SetUp the 'moderation' Nova-Ideo configuration
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
        actions[0].execute(
            context, self.request, {'_object_data': idea})
        idea_result = context.ideas[0]
        # duplicate
        actions = getAllBusinessAction(
            idea_result, self.request,
            process_id='ideamanagement',
            node_id='duplicate')
        actions[0].execute(
            idea_result, self.request, {
                'title': 'Duplicated idea',
                'text': 'Idea text',
                'keywords': ['dup 1'],
                'attached_files': []
            })
        self.assertTrue(len(context.ideas), 2)
        new_idea = context.ideas[1]
        self.assertIn('to work', new_idea.state)
        self.assertEqual('Duplicated idea', new_idea.title)
        self.assertEqual('Idea text', new_idea.text)
        keywords = ['dup 1']
        self.assertTrue(all(a in keywords
                            for a in new_idea.keywords))
        self.assertIs(idea_result, new_idea.originalentity)
        self.assertIn(new_idea, idea_result.duplicates)
        # new idea actions: can't publish ==> the same text
        actions = getAllBusinessAction(
            new_idea, self.request,
            process_id='ideamanagement')
        expected_actions = ['duplicate', 'edit', 'abandon', 'associate', 'see']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 5)
        self.assertTrue(all(a in expected_actions
                            for a in actions_ids))
        # edit the text of the new idea
        new_idea.text = 'Duplicated text'
        # new idea actions: can publish
        actions = getAllBusinessAction(
            new_idea, self.request,
            process_id='ideamanagement')
        expected_actions = [
            'duplicate', 'edit',
            'abandon', 'associate',
            'see', 'publish']
        actions_ids = [a.node_id for a in actions]
        self.assertEqual(len(actions_ids), 6)
        self.assertTrue(all(a in expected_actions
                            for a in actions_ids))