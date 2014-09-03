import re
import colander
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.util import find_catalog
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite, allSubobjectsOfType
from dace.objectofcollaboration.principal.util import get_current
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


class DetailProposalView(BasicView):
    title = _('Details')
    name = 'seeProposal'
    behaviors = [SeeProposal]
    template = 'novaideo:views/novaideo_view_manager/templates/see_proposal.pt'
    item_template = 'pontus:templates/subview_sample.pt'
    viewid = 'seeproposal'


    def _vote_action(self):
        isactive = False
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,'dace_ui_api')
        vote_data = {'subject':self.context}
        action_updated, messages, resources, actions = dace_ui_api._actions(self.request, self.context, 'referendumprocess', 'favour')
        if action_updated and not isactive:
            isactive = True

        if actions: 
            vote_data['voteaction'] = actions[0]

        return vote_data, resources, messages, isactive

    def update(self):
        self.execute(None)
        user = get_current()
        actions = self.context.actions
        firstvote_actions, resources, messages, isactive = self._vote_action()
        actions = [a for a in actions if getattr(a.action, 'style', '') == 'button']
        actions_urls = []
        for action in actions:
            actions_urls.append({'title':action.title, 'url':action.url})

        result = {}
        values = {
                'proposal': self.context,
                'current_user': user,
                'actions': actions_urls,
                'voteaction': firstvote_actions
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
    views = (EditAmendmentsView, AssociateView, PresentProposalView, CommentProposalView)


@view_config(
    name='seeproposal',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class SeeProposalView(MultipleView):
    title = _('Details')
    name = 'seeproposal'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    views = (DetailProposalView, SeeProposalActionsView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeProposal:SeeProposalView})

