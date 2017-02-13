# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS

from novaideo.content.processes.challenge_management.behaviors import (
    CommentChallenge, CommentChallengeAnonymous)
from novaideo.views.idea_management.comment_idea import (
    CommentIdeaView,
    CommentIdeaFormView,
    CommentsView as CommentsIdeaView)
from novaideo.content.challenge import Challenge
from novaideo import _
from novaideo.views.core import ActionAnonymousView


class CommentsView(CommentsIdeaView):
    validators = [CommentChallenge.get_validator()]


class CommentChallengeFormView(CommentIdeaFormView):
    title = _('Discuss the challenge')
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    behaviors = [CommentChallenge]
    formid = 'formcommentchallenge'
    name = 'commentchallengeform'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': CommentChallenge.node_definition.id})
        formwidget = deform.widget.FormWidget(css_class='commentform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='comment',
    context=Challenge,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CommentChallengeView(CommentIdeaView):
    title = _('Discuss the challenge')
    description = _('Discuss the challenge')
    name = 'comment'
    views = (CommentsView, CommentChallengeFormView)

    def _init_views(self, views, **kwargs):
        if kwargs.get('only_form', False):
            views = (CommentChallengeFormView, )

        super(CommentIdeaView, self)._init_views(views, **kwargs)


@view_config(
    name='commentanonymous',
    context=Challenge,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CommentChallengeAnonymousView(ActionAnonymousView):
    behaviors = [CommentChallengeAnonymous]
    name = 'commentanonymous'


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CommentChallengeAnonymous: CommentChallengeAnonymousView})


DEFAULTMAPPING_ACTIONS_VIEWS.update({CommentChallenge: CommentChallengeView})
