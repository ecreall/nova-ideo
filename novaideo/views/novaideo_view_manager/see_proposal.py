import re
import colander
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.util import find_catalog
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite, allSubobjectsOfType
from dace.objectofcollaboration.principal.util import get_current, has_any_roles
from pontus.view import BasicView, ViewError, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI
from pontus.widget import CheckboxChoiceWidget, RichTextWidget
from pontus.schema import Schema
from pontus.form import FormView
from pontus.view_operation import MultipleView

from novaideo.content.processes.novaideo_view_manager.behaviors import  SeeProposal
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.views.proposal_management.present_proposal import PresentProposalView
from novaideo.views.proposal_management.comment_proposal import CommentProposalView
from novaideo.views.proposal_management.associate import AssociateView
from novaideo.views.proposal_management.edit_amendments import EditAmendmentsView
from novaideo.views.proposal_management.add_ideas import AddIdeasView


class DetailProposalView(BasicView):
    title = _('Details')
    name = 'seeProposal'
    behaviors = [SeeProposal]
    template = 'novaideo:views/novaideo_view_manager/templates/see_proposal.pt'
    item_template = 'pontus:templates/subview_sample.pt'
    viewid = 'seeproposal'
    filigrane_template = 'novaideo:views/novaideo_view_manager/templates/filigrane.pt'

    def _vote_action(self):
        isactive = False
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,'dace_ui_api')
        action_updated, messages, resources, actions = dace_ui_api._actions(self.request, self.context, process_discriminator='Vote process')
        for action in actions:
            action['body'] = dace_ui_api.get_action_body(self.context, self.request, action['action'], True)
           
        return actions, resources, messages, action_updated

    def _get_adapted_text(self, user):
        is_participant = has_any_roles(user=user, roles=(('Participant', self.context),))
        text = getattr(self.context, 'text', '')
        add_filigrane = False
        corrections = [c for c in self.context.corrections if 'in process' in c.state]
        if corrections and is_participant:
            text = corrections[-1].get_adapted_text(user)
        elif not is_participant and not ('published' in self.context.state):
            add_filigrane = True

        return text, add_filigrane

    def update(self):
        self.execute(None)
        user = get_current()
        actions = self.context.actions
        vote_actions, resources, messages, isactive = self._vote_action()
        actions = [a for a in actions if getattr(a.action, 'style', '') == 'button']
        global_actions = [a for a in actions if getattr(a.action, 'style_descriminator','') == 'global-action']
        wg_actions = [a for a in actions if getattr(a.action, 'style_descriminator','') == 'wg-action']
        text_actions = [a for a in  actions if getattr(a.action, 'style_descriminator','') == 'text-action']
        global_actions = sorted(global_actions, key=lambda e: getattr(e.action, 'style_order',0))
        wg_actions = sorted(wg_actions, key=lambda e: getattr(e.action, 'style_order',0))
        text_actions = sorted(text_actions, key=lambda e: getattr(e.action, 'style_order',0))
        text, add_filigrane = self._get_adapted_text(user)
        result = {}
        values = {
                'proposal': self.context,
                'text': text,
                'current_user': user,
                'global_actions': global_actions,
                'wg_actions': wg_actions,
                'text_actions': text_actions,
                'voteactions': vote_actions,
                'filigrane': add_filigrane
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
    views = (EditAmendmentsView, AssociateView, AddIdeasView, PresentProposalView, CommentProposalView)


@view_config(
    name='seeproposal',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class SeeProposalView(MultipleView):
    title = _('Details')
    name = 'seeproposal'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    requirements = {'css_links':['novaideo:static/css/steps/steps.css'],
                    'js_links':['novaideo:static/js/correct_proposal.js',
                                'novaideo:static/js/comment.js']}
    views = (DetailProposalView, SeeProposalActionsView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeProposal:SeeProposalView})

