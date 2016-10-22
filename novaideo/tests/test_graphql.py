# -*- coding: utf-8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Vincent Fretin

"""Tests for GraphQL endpoint
"""
from webtest import TestApp
from novaideo.testing import FunctionalTests


class ListIdeas(FunctionalTests):
    """Tests list ideas"""

    def setUp(self):
        super().setUp()
        self.app = TestApp(self.app)

    def test_no_idea(self):
        resp = self.app.get('/graphql', {'query': """{
            ideas {
                edges {
                    node { title }
                }
             }
        }"""})
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(resp.content_type, 'application/json')
        self.assertEqual(resp.body, b'{"data":{"ideas":{"edges":[]}}}')
