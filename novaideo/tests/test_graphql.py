# -*- coding: utf-8 -*-
from dace.util import getAllBusinessAction
import transaction

from novaideo.content.idea import Idea
from novaideo.graphql.schema import schema
from novaideo.testing import FunctionalTests


def create_idea(request, title, text, keywords):
    """Create an Idea."""
    container = request.root
    idea = Idea(
        title=title,
        text=text,
        keywords=keywords
    )
    actions = getAllBusinessAction(
        container, request, process_id='ideamanagement',
        node_id='creatandpublish')
    create_action = actions[0]
    create_action.execute(
        container, request, {'_object_data': idea})


class TestGraphQLSchema(FunctionalTests):

    def setUp(self):
        super(TestGraphQLSchema, self).setUp()
        self.default_novaideo_config()
        params = {
            'title': 'My great idea',
            'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit',
            'keywords': ['foo', 'bar']
        }
        create_idea(self.request, **params)
        params['title'] = 'My other idea'
        create_idea(self.request, **params)
        transaction.commit()

    def test_get_id_for_all_ideas(self):
        query = '{ ideas { edges { node { id, title } } } }'
        result = schema.execute(query)
        self.assertIsNone(result.errors)
        edges = result.data['ideas']['edges']
        self.assertEqual(len(edges), 2)
        self.assertEqual(edges[0]['node']['title'], 'My great idea')
        self.assertEqual(edges[1]['node']['title'], 'My other idea')
