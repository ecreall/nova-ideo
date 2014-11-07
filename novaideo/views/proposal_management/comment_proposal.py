
import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS

from novaideo.content.processes.proposal_management.behaviors import (
    CommentProposal)
from novaideo.views.idea_management.comment_idea import (
    CommentIdeaView, 
    CommentIdeaFormView, 
    CommentsView as CommentsIdeaView)
from novaideo.content.proposal import Proposal
from novaideo import _



class CommentsView(CommentsIdeaView):
    validators = [CommentProposal.get_validator()]


class CommentProposalFormView(CommentIdeaFormView):
    title = _('Discuss the proposal')
    behaviors = [CommentProposal]
    formid = 'formcommentproposal'
    name = 'commentproposalform'

    def before_update(self):
        formwidget = deform.widget.FormWidget(css_class='commentform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        view_name = self.request.view_name
        if self.request.view_name == 'dace-ui-api-view':
            view_name = 'commentproposal'

        formwidget.ajax_url = self.request.resource_url(self.context,
                                                       '@@'+view_name)
        self.schema.widget = formwidget


@view_config(
    name='commentproposal',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class CommentProposalView(CommentIdeaView):
    title = _('Discuss the proposal')
    description = _('Discuss the proposal')
    name = 'commentidea'
    views = (CommentProposalFormView, CommentsView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({CommentProposal:CommentProposalView})
