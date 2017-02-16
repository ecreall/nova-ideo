# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, omit

from novaideo.content.processes.comment_management.behaviors import (
    TransformToQuestion)
from novaideo.content.question import QuestionSchema, Question
from novaideo.views.proposal_management.create_proposal import add_file_data
from novaideo import _
from novaideo.content.comment import Comment
from ..filter import get_pending_challenges


@view_config(
    name='askquestion',
    context=Comment,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AskQuestionView(FormView):

    title = _('Transform the comment into an idea')
    schema = select(QuestionSchema(factory=Question, editable=True),
                    ['challenge',
                     'title',
                     'text',
                     'options',
                     'keywords',
                     'attached_files'])
    behaviors = [TransformToQuestion, Cancel]
    formid = 'formaskquestion'
    name = 'askquestion'

    def default_data(self):
        data = {'text': self.context.comment}
        attached_files = self.context.files
        data['attached_files'] = []
        files = []
        for file_ in attached_files:
            file_data = add_file_data(file_)
            if file_data:
                files.append(file_data)

        if files:
            data['attached_files'] = files

        challenge = self.context.challenge
        if challenge and challenge.can_add_content:
            data['challenge'] = challenge

        return data

    def before_update(self):
        user = get_current(self.request)
        has_challenges = len(get_pending_challenges(user)) > 0
        if not has_challenges:
            self.schema = omit(
                self.schema, ['challenge'])

        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': TransformToQuestion.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {TransformToQuestion: AskQuestionView})
