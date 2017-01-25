# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS

from novaideo.content.processes.question_management.behaviors import (
    CommentQuestion, CommentQuestionAnonymous)
from novaideo.content.question import Question
from novaideo import _

from novaideo.views.idea_management.comment_idea import (
    CommentIdeaView,
    CommentIdeaFormView,
    CommentsView as CommentsIdeaView)
from novaideo.views.core import ActionAnonymousView


class CommentsView(CommentsIdeaView):
    validators = [CommentQuestion.get_validator()]


class CommentQuestionFormView(CommentIdeaFormView):
    title = _('Discuss the question')
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    behaviors = [CommentQuestion]
    formid = 'formcommentquestion'
    name = 'commentquestionform'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': CommentQuestion.node_definition.id})
        formwidget = deform.widget.FormWidget(css_class='commentform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='comment',
    context=Question,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CommentQuestionView(CommentIdeaView):
    title = _('Discuss the question')
    description = _('Discuss the question')
    name = 'comment'
    views = (CommentsView, CommentQuestionFormView)

    def _init_views(self, views, **kwargs):
        if kwargs.get('only_form', False):
            views = (CommentQuestionFormView, )

        super(CommentIdeaView, self)._init_views(views, **kwargs)


@view_config(
    name='commentanonymous',
    context=Question,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CommentQuestionAnonymousView(ActionAnonymousView):
    behaviors = [CommentQuestionAnonymous]
    name = 'commentanonymous'


DEFAULTMAPPING_ACTIONS_VIEWS.update({CommentQuestion: CommentQuestionView})

DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CommentQuestionAnonymous: CommentQuestionAnonymousView})
