# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView

from novaideo.content.processes.question_management.behaviors import EditQuestion
from novaideo.content.question import QuestionSchema, Question
from novaideo import _


class EditQuestionFormView(FormView):

    title = _('Edit the question')
    schema = select(QuestionSchema(),
                    ['title',
                     'text',
                     'options',
                     'keywords',
                     'attached_files'])
    behaviors = [EditQuestion, Cancel]
    formid = 'formeditquestion'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    name = 'editQuestion'

    def before_update(self):
        if self.context.answers:
            self.schema.children.remove(
                self.schema.get('options'))

        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': EditQuestion.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')

    def default_data(self):
        return self.context


@view_config(
    name='editquestion',
    context=Question,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditQuestionView(MultipleView):
    title = _('Edit the question')
    name = 'editquestion'
    wrapper_template = 'novaideo:views/templates/view_wrapper.pt'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (EditQuestionFormView, )


DEFAULTMAPPING_ACTIONS_VIEWS.update({EditQuestion: EditQuestionView})
