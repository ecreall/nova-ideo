# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry
from pyramid.httpexceptions import HTTPFound

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    get_current, has_role, Anonymous)
from pontus.view import BasicView
from daceui.interfaces import IDaceUIAPI
from pontus.view_operation import MultipleView
from pontus.util import merge_dicts

from novaideo.content.processes.proposal_management.behaviors import (
    SeeProposal)
from novaideo.utilities.util import (
    generate_navbars, ObjectRemovedException)
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.content.processes import get_states_mapping
from novaideo.views.proposal_management.present_proposal import (
    PresentProposalView)
from novaideo.views.proposal_management.comment_proposal import (
    CommentProposalView)
from novaideo.views.proposal_management.see_amendments import (
    SeeAmendmentsView)
from novaideo.views.proposal_management.see_related_ideas import (
    SeeRelatedIdeasView)
from novaideo.views.proposal_management.compare_proposal import (
    CompareProposalView)


class DetailProposalView(BasicView):
    title = _('Details')
    name = 'seeProposal'
    behaviors = [SeeProposal]
    template = 'novaideo:views/proposal_management/templates/see_proposal.pt'
    wrapper_template = 'daceui:templates/simple_view_wrapper.pt'
    viewid = 'seeproposal'
    filigrane_template = 'novaideo:views/proposal_management/templates/filigrane.pt'
    validate_behaviors = False

    def _vote_actions(self):
        dace_ui_api = get_current_registry().getUtility(
            IDaceUIAPI, 'dace_ui_api')
        vote_actions = dace_ui_api.get_actions(
            [self.context], self.request,
            process_discriminator='Vote process')
        action_updated, messages, \
            resources, actions = dace_ui_api.update_actions(
                self.request, vote_actions, True)
        for action in list(actions):
            action['body'] = dace_ui_api.get_action_body(
                self.context, self.request, action['action'],
                True, False)
            if not action['body']:
                actions.remove(action)

        return actions, resources, messages, action_updated

    def _get_adapted_text(self, user, is_participant, corrections):
        text = getattr(self.context, 'text', '')
        description = getattr(self.context, 'description', '')
        title = getattr(self.context, 'title', '')
        add_filigrane = False
        if corrections and is_participant:
            text = corrections[-1].get_adapted_text(user)
            description = corrections[-1].get_adapted_description(user)
            title = corrections[-1].get_adapted_title(user)
        elif not is_participant and \
            not any(s in self.context.state
                    for s in ['published', 'examined']):
            add_filigrane = True

        return title, description, text, add_filigrane

    def _cant_publish_alert(self, actions):
        if 'draft' in self.context.state:
            return not any(a.behavior_id == 'publish'
                           for a in actions.get('global-action', []))

        return False

    def update(self):
        self.execute(None)
        vote_actions, resources, messages, isactive = self._vote_actions()
        try:
            text_action = [{'title': _('Vote'),
                            'class_css': 'vote-action',
                            'style_picto': 'glyphicon glyphicon-stats'}] \
                if vote_actions else []

            navbars = generate_navbars(
                self.request, self.context,
                text_action=text_action)
        except ObjectRemovedException:
            return HTTPFound(self.request.resource_url(getSite(), ''))

        ct_participate_max = False
        ct_participate_closed = False
        ct_participate = False
        user = get_current()
        is_participant = has_role(user=user, role=('Participant', self.context))
        root = getSite()
        working_group = self.context.working_group
        wg_actions = [a for a in navbars['all_actions']['wg-action']
                      if a.node_id != "seemembers"]
        resources = merge_dicts(navbars['resources'], resources,
                                ('js_links', 'css_links'))
        resources['js_links'] = list(set(resources['js_links']))
        resources['css_links'] = list(set(resources['css_links']))
        if not messages:
            messages = navbars['messages']

        if working_group:
            participants_maxi = root.participants_maxi
            work_mode = getattr(working_group, 'work_mode', None)
            if work_mode:
                participants_maxi = work_mode.participants_maxi

            ct_participate_max = len(working_group.members) == participants_maxi
            ct_participate_closed = 'closed' in working_group.state
            ct_participate = 'archived' not in working_group.state and \
                not isinstance(user, Anonymous) and \
                user not in working_group.members and \
                (ct_participate_max or ct_participate_closed)

        corrections = [c for c in self.context.corrections
                       if 'in process' in c.state]
        title, description, text, add_filigrane = self._get_adapted_text(
            user, is_participant, corrections)
        related_ideas = list(self.context.related_ideas.keys())
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

        result = {}
        values = {
            'proposal': self.context,
            'state': get_states_mapping(user, self.context,
                                        self.context.state[0]),
            'title': title,
            'description': description,
            'text': text,
            'corrections': corrections,
            'current_user': user,
            'is_participant': is_participant,
            'wg_actions': wg_actions,
            'voteactions': vote_actions,
            'filigrane': add_filigrane,
            'cant_publish': self._cant_publish_alert(navbars['all_actions']),
            'idea_to_examine': idea_to_examine,
            'not_published_ideas': not_published_ideas,
            'not_favorable_ideas': not_favorable_ideas,
            'ct_participate': ct_participate,
            'ct_participate_closed': ct_participate_closed,
            'ct_participate_max': ct_participate_max,
            'navbar_body': navbars['navbar_body'],
            'actions_bodies': navbars['body_actions'],
            'footer_body': navbars['footer_body']
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = isactive or navbars['isactive']
        result.update(resources)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class SeeProposalActionsView(MultipleView):
    title = _('actions')
    name = 'seeiactionsdea'
    template = 'novaideo:views/idea_management/templates/panel_group.pt'
    views = (SeeAmendmentsView,
             SeeRelatedIdeasView,
             CompareProposalView)

    def _activate(self, items):
        pass


@view_config(
    name='seeproposal',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeProposalView(MultipleView):
    title = ''
    name = 'seeproposal'
    template = 'novaideo:views/templates/simple_mergedmultipleview.pt'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/correct_proposal.js',
                                 'novaideo:static/js/comment.js',
                                 'novaideo:static/js/compare_idea.js',
                                 'novaideo:static/js/ballot_management.js']}
    views = (DetailProposalView, SeeProposalActionsView)
    validators = [SeeProposal.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeProposal: SeeProposalView})
