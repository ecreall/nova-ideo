import datetime
import deform
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView
from pontus.view import BasicView, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI

from novaideo.content.processes.proposal_management.behaviors import  CommentProposal
from novaideo.views.idea_management.comment_idea import CommentIdeaView, CommentIdeaFormView, CommentsView as CommentsIdeaView
from novaideo.content.comment import CommentSchema, Comment
from novaideo.content.proposal import Proposal
from novaideo import _



class CommentsView(CommentsIdeaView):
    validators = [CommentProposal.get_validator()]


class CommentProposalFormView(CommentIdeaFormView):

    title = _('Comment')
    behaviors = [CommentProposal]
    formid = 'formcommentproposal'
    name='commentproposalform'

    def before_update(self):
        formwidget = deform.widget.FormWidget(css_class='commentform')
        formwidget.template = 'novaideo:views/templates/form.pt'
        view_name = self.request.view_name
        if self.request.view_name == 'dace-ui-api-view':
            view_name = 'commentproposal'

        formwidget.ajax_url = self.request.resource_url(self.context, '@@'+view_name)
        self.schema.widget = formwidget



@view_config(
    name='commentproposal',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class CommentProposalView(CommentIdeaView):
    name='commentidea'
    views = (CommentProposalFormView, CommentsView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({CommentProposal:CommentProposalView})
