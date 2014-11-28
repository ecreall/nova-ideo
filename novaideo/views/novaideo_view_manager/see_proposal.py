# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    get_current, has_role, Anonymous)
from pontus.view import BasicView
from pontus.dace_ui_extension.interfaces import IDaceUIAPI
from pontus.view_operation import MultipleView

from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeProposal)
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
    template = 'novaideo:views/novaideo_view_manager/templates/see_proposal.pt'
    item_template = 'pontus:templates/subview_sample.pt'
    viewid = 'seeproposal'
    filigrane_template = 'novaideo:views/novaideo_view_manager/templates/filigrane.pt'
    validate_behaviors = False

    def _vote_actions(self):
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,
                                                       'dace_ui_api')
        vote_actions = dace_ui_api.get_actions([self.context],
                                           self.request,
                                           process_discriminator='Vote process',
                                            )
        action_updated, messages, \
        resources, actions = dace_ui_api.update_actions(
                                        self.request, 
                                        vote_actions,
                                        True,
                                        )
        for action in list(actions):
            action['body'] = dace_ui_api.get_action_body(self.context, 
                                                         self.request, 
                                                         action['action'], 
                                                         True)
            if not action['body']:
                actions.remove(action)

        return actions, resources, messages, action_updated

    def _get_adapted_text(self, user):
        is_participant = has_role(user=user, role=('Participant', self.context))
        text = getattr(self.context, 'text', '')
        description = getattr(self.context, 'description', '')
        add_filigrane = False
        corrections = [c for c in self.context.corrections \
                       if 'in process' in c.state]
        if corrections and is_participant:
            text = corrections[-1].get_adapted_text(user)
            description = corrections[-1].get_adapted_description(user)
        elif not is_participant and not ('published' in self.context.state):
            add_filigrane = True

        return description, text, add_filigrane

    def _cant_submit_alert(self, actions):
        if 'draft' in self.context.state:
            return not any(a.title == 'Publish' for a in actions)

        return False

    def update(self):
        self.execute(None)
        user = get_current()
        root = getSite()
        wg = self.context.working_group
        actions = self.context.actions
        vote_actions, resources, messages, isactive = self._vote_actions()
        actions = [a for a in actions \
                   if getattr(a.action, 'style', '') == 'button']
        global_actions = [a for a in actions \
                          if getattr(a.action, 'style_descriminator', '') == \
                             'global-action']
        wg_actions = [a for a in actions \
                      if getattr(a.action, 'style_descriminator', '') == \
                         'wg-action']
        text_actions = [a for a in  actions \
                        if getattr(a.action, 'style_descriminator', '') == \
                           'text-action']
        global_actions = sorted(global_actions, 
                                key=lambda e: getattr(e.action, 
                                                      'style_order', 0))
        wg_actions = sorted(wg_actions, 
                            key=lambda e: getattr(e.action, 'style_order', 0))
        text_actions = sorted(text_actions, 
                              key=lambda e: getattr(e.action, 'style_order', 0))

        ct_participate_max = False
        ct_participate_closed = False
        ct_participate = False
        if wg:
            ct_participate_max = len(wg.members) == root.participants_maxi
            ct_participate_closed = 'closed' in wg.state
            ct_participate = 'archived' not in wg.state and \
                         not isinstance(user, Anonymous) and \
                         user not in wg.members and \
                         (ct_participate_max or ct_participate_closed)
        
        
        description, text, add_filigrane = self._get_adapted_text(user)
        result = {}
        values = {
                'proposal': self.context,
                'state': get_states_mapping(user, self.context, 
                                            self.context.state[0]),
                'text': text,
                'description': description,
                'current_user': user,
                'global_actions': global_actions,
                'wg_actions': wg_actions,
                'text_actions': text_actions,
                'voteactions': vote_actions,
                'filigrane': add_filigrane,
                'cant_submit': self._cant_submit_alert(global_actions),
                'ct_participate': ct_participate,
                'ct_participate_closed': ct_participate_closed,
                'ct_participate_max': ct_participate_max
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = isactive
        result.update(resources)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class SeeProposalActionsView(MultipleView):
    title = _('actions')
    name = 'seeiactionsdea'
    template = 'novaideo:views/idea_management/templates/panel_group.pt'
    views = (SeeAmendmentsView, 
             SeeRelatedIdeasView, 
             PresentProposalView, 
             CompareProposalView, 
             CommentProposalView)

    def _activate(self, items):
        pass


@view_config(
    name='seeproposal',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class SeeProposalView(MultipleView):
    title = ''
    name = 'seeproposal'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/correct_proposal.js',
                                'novaideo:static/js/comment.js',
                                'novaideo:static/js/compare_idea.js']}
    views = (DetailProposalView, SeeProposalActionsView)
    validators = [SeeProposal.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeProposal:SeeProposalView})