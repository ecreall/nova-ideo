# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import json
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    get_current, has_role, Anonymous, has_any_roles)
from pontus.view import BasicView
from pontus.view_operation import MultipleView
from pontus.util import merge_dicts

from novaideo.content.processes.proposal_management.behaviors import (
    SeeProposal)
from novaideo.utilities.util import (
    generate_navbars, ObjectRemovedException, get_vote_actions_body)
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.content.processes import get_states_mapping
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

    def _enable_corrections(self, is_participant, corrections):
        return 'active' in getattr(self.context.working_group, 'state', []) and\
               corrections and is_participant

    def _get_adapted_text(
        self, user, is_participant,
        corrections, enable_corrections):
        text = getattr(self.context, 'text', '')
        description = getattr(self.context, 'description', '')
        title = getattr(self.context, 'title', '')
        add_filigrane = False
        if enable_corrections:
            text = corrections[-1].get_adapted_text(user)
            description = corrections[-1].get_adapted_description(user)
            title = corrections[-1].get_adapted_title(user)
        elif not is_participant and \
            not any(s in self.context.state
                    for s in ['published', 'examined']):
            add_filigrane = True

        return title, description, text, add_filigrane

    def _cant_participate(self, actions, user, root):
        cant_participate = not any(a.behavior_id == 'participate'
                                   for a in actions.get('wg-action', []))
        if cant_participate:
            working_group = self.context.working_group
            if not working_group:
                return _("The working group is closed")

            is_active_user = 'active' in getattr(user, 'state', [])
            if not is_active_user:
                return None

            active_working_groups = getattr(user, 'active_working_groups', [])
            is_member = user in working_group.members
            in_wl = user in working_group.wating_list
            max_participation = len(active_working_groups) >= \
                root.participations_maxi
            is_closed = 'closed' in working_group.state or \
                not any(s in self.context.state for s in
                        ['amendable', 'open to a working group'])
            if not is_member:
                if in_wl:
                    return _("You are on the waiting list")

                if max_participation:
                    return _("You have reached the limit of the number "
                             "of working groups in which you can participate "
                             "simultaneously. In order to submit your proposal, "
                             "please quit one of your current working groups")

                if is_closed:
                    return _("The participation is closed")

                return _("You can't participate in the working group")

        return None

    def _cant_publish(self, actions):
        if 'draft' in self.context.state:
            return not any(a.behavior_id == 'publish' or
                           a.behavior_id == 'submit'
                           for a in actions.get('global-action', []))

        return False

    def update(self):
        self.execute(None)
        vote_actions = get_vote_actions_body(
            self.context, self.request)
        try:
            navbars = generate_navbars(
                self.request, self.context,
                text_action=vote_actions['activators'])
        except ObjectRemovedException:
            return HTTPFound(self.request.resource_url(getSite(), ''))

        resources = merge_dicts(navbars['resources'], vote_actions['resources'],
                                ('js_links', 'css_links'))
        resources['js_links'] = list(set(resources['js_links']))
        resources['css_links'] = list(set(resources['css_links']))
        messages = vote_actions['messages']
        if not messages:
            messages = navbars['messages']

        user = get_current()
        is_participant = has_role(
            user=user, role=('Participant', self.context))
        root = getSite()
        corrections = [c for c in self.context.corrections
                       if 'in process' in c.state]
        enable_corrections = self._enable_corrections(
            is_participant, corrections)
        title, description, text, add_filigrane = self._get_adapted_text(
            user, is_participant, corrections, enable_corrections)
        tinymce_js = 'deform:static/tinymce/tinymce.min.js'
        if enable_corrections and\
           tinymce_js not in resources['js_links']:
            resources['js_links'].append(tinymce_js)

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

        is_censored = 'censored' in self.context.state
        to_hide = is_censored and not has_any_roles(
            user=user, roles=(('Participant', self.context), 'Moderator'))
        result = {}
        values = {
            'proposal': self.context,
            'is_censored': is_censored,
            'to_hide': to_hide,
            'state': get_states_mapping(user, self.context,
                                        self.context.state[0]),
            'title': title,
            'description': description,
            'text': text,
            'corrections': corrections,
            'enable_corrections': enable_corrections,
            'current_user': user,
            'is_participant': is_participant,
            'vote_actions_body': vote_actions['body'],
            'filigrane': add_filigrane,
            'cant_publish': self._cant_publish(navbars['all_actions']),
            'idea_to_examine': idea_to_examine,
            'not_published_ideas': not_published_ideas,
            'not_favorable_ideas': not_favorable_ideas,
            'ct_participate': self._cant_participate(
                navbars['all_actions'], user, root),
            'wg_body': navbars['wg_body'],
            'navbar_body': navbars['navbar_body'],
            'actions_bodies': navbars['body_actions'],
            'footer_body': navbars['footer_body'],
            'json': json
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = vote_actions['isactive'] or navbars['isactive']
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
