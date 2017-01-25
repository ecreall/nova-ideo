# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS

from novaideo.content.processes.proposal_management.behaviors import (
    CommentProposal, CommentProposalAnonymous)
from novaideo.views.idea_management.comment_idea import (
    CommentIdeaView,
    CommentIdeaFormView,
    CommentsView as CommentsIdeaView)
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.views.core import ActionAnonymousView


class CommentsView(CommentsIdeaView):
    validators = [CommentProposal.get_validator()]


class CommentProposalFormView(CommentIdeaFormView):
    title = _('Discuss the proposal')
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    behaviors = [CommentProposal]
    formid = 'formcommentproposal'
    name = 'commentproposalform'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': CommentProposal.node_definition.id})
        formwidget = deform.widget.FormWidget(css_class='commentform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='comment',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CommentProposalView(CommentIdeaView):
    title = _('Discuss the proposal')
    description = _('Discuss the proposal')
    name = 'comment'
    views = (CommentsView, CommentProposalFormView)

    def _init_views(self, views, **kwargs):
        if kwargs.get('only_form', False):
            views = (CommentProposalFormView, )

        super(CommentIdeaView, self)._init_views(views, **kwargs)


@view_config(
    name='commentanonymous',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CommentProposalAnonymousView(ActionAnonymousView):
    behaviors = [CommentProposalAnonymous]
    name = 'commentanonymous'


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CommentProposalAnonymous: CommentProposalAnonymousView})


DEFAULTMAPPING_ACTIONS_VIEWS.update({CommentProposal: CommentProposalView})
