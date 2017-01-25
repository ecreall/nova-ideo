# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS

from novaideo.content.processes.question_management.behaviors import (
    CommentAnswer, CommentAnswerAnonymous)
from novaideo.content.question import Answer
from novaideo import _

from novaideo.views.idea_management.comment_idea import (
    CommentIdeaView,
    CommentIdeaFormView,
    CommentsView as CommentsIdeaView)
from novaideo.views.core import ActionAnonymousView


class CommentsView(CommentsIdeaView):
    validators = [CommentAnswer.get_validator()]


class CommentAnswerFormView(CommentIdeaFormView):
    title = _('Discuss the answer')
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    behaviors = [CommentAnswer]
    formid = 'formcommentanswer'
    name = 'commentanswerform'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': CommentAnswer.node_definition.id})
        formwidget = deform.widget.FormWidget(css_class='commentform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='comment',
    context=Answer,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CommentAnswerView(CommentIdeaView):
    title = _('Discuss the answer')
    description = _('Discuss the answer')
    name = 'comment'
    views = (CommentsView, CommentAnswerFormView)

    def _init_views(self, views, **kwargs):
        if kwargs.get('only_form', False):
            views = (CommentAnswerFormView, )

        super(CommentIdeaView, self)._init_views(views, **kwargs)


@view_config(
    name='commentanonymous',
    context=Answer,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CommentAnswerAnonymousView(ActionAnonymousView):
    behaviors = [CommentAnswerAnonymous]
    name = 'commentanonymous'


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CommentAnswerAnonymous: CommentAnswerAnonymousView})


DEFAULTMAPPING_ACTIONS_VIEWS.update({CommentAnswer: CommentAnswerView})
