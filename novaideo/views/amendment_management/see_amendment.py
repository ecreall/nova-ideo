# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import html_diff_wrapper
from dace.util import getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current, has_role
from pontus.view import BasicView
from pontus.util import merge_dicts

from novaideo.content.processes.amendment_management.behaviors import (
    SeeAmendment)
from novaideo.content.amendment import Amendment
from novaideo.content.processes import get_states_mapping
from novaideo.utilities.util import generate_navbars, ObjectRemovedException
# from .present_amendment import PresentAmendmentView
# from .comment_amendment import CommentAmendmentView
from .explanation_amendment import IntentionFormView


@view_config(
    name='seeamendment',
    context=Amendment,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DetailAmendmentView(BasicView):
    title = ''
    name = 'seeamendment'
    behaviors = [SeeAmendment]
    template = 'novaideo:views/amendment_management/templates/see_amendment.pt'
    # wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    viewid = 'seeamendment'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/comment.js',
                                 'novaideo:static/js/explanation_amendment.js']}

    def _add_requirements(self, user):
        is_owner = has_role(user=user, role=('Owner', self.context))
        if is_owner and ('explanation' in self.context.state):
            self.requirements = {'js_links': [], 'css_links': []}
            intentionform = IntentionFormView(self.context, self.request)
            intentionformresult = intentionform()
            self.requirements['js_links'] = intentionformresult['js_links']
            self.requirements['css_links'] = intentionformresult['css_links']
            self.requirements['js_links'].append(
                'novaideo:static/js/explanation_amendment.js')

    def _end_explanation(self, actions):
        if 'explanation' in self.context.state:
            return any(a.behavior_id == 'submit'
                       for a in actions.get('global-action', []))

        return False

    def update(self):
        self.execute(None)
        try:
            navbars = generate_navbars(self.request, self.context)
        except ObjectRemovedException:
            return HTTPFound(self.request.resource_url(getSite(), ''))

        user = get_current()
        result = {}
        textdiff = ''
        # descriptiondiff = ''
        # keywordsdiff = []
        # proposal = self.context.proposal
        textdiff = self.context.text_diff
        # soup, descriptiondiff = html_diff_wrapper.render_html_diff(
        #     '<div>'+getattr(proposal, 'description', '')+'</div>',
        #     '<div>'+getattr(self.context, 'description', '')+'</div>')
        # for k in proposal.keywords:
        #     if k in self.context.keywords:
        #         keywordsdiff.append({'title': k, 'state': 'nothing'})
        #     else:
        #         keywordsdiff.append({'title': k, 'state': 'del'})

        # [keywordsdiff.append({'title': k, 'state': 'ins'})
        #  for k in self.context.keywords if k not in proposal.keywords]

        related_ideas = list(self.context.get_used_ideas())
        not_published_ideas = [i for i in related_ideas
                               if 'published' not in i.state]
        not_favorable_ideas = []
        idea_to_examine = 'idea' in self.request.content_to_examine
        if idea_to_examine:
            not_favorable_ideas = [i for i in related_ideas
                                   if 'favorable' not in i.state and
                                   'published' in i.state]
            if not self.request.moderate_ideas:
                not_favorable_ideas.extend(not_published_ideas)

        values = {
            'amendment': self.context,
            'state': get_states_mapping(
                user, self.context, self.context.state[0]),
            'textdiff': textdiff,
            # 'descriptiondiff': descriptiondiff,
            # 'keywordsdiff': keywordsdiff,
            'current_user': user,
            'navbar_body': navbars['navbar_body'],
            'actions_bodies': navbars['body_actions'],
            'footer_body': navbars['footer_body'],
            'to_submit': self._end_explanation(navbars['all_actions']),
            'idea_to_examine': idea_to_examine,
            'not_published_ideas': not_published_ideas,
            'not_favorable_ideas': not_favorable_ideas
        }
        self._add_requirements(user)
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = navbars['messages']
        item['isactive'] = navbars['isactive']
        result.update(navbars['resources'])
        result['coordinates'] = {self.coordinates: [item]}
        result = merge_dicts(self.requirements_copy, result)
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeAmendment: DetailAmendmentView})
