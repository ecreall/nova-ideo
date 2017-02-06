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

from novaideo.content.processes.question_management.behaviors import EditAnswer
from novaideo.content.question import Answer
from ..answer_question import AnswerSchema, options_choice
from novaideo import _


class EditAnswerFormView(FormView):

    title = _('Edit the answer')
    schema = select(AnswerSchema(factory=Answer,
                                 editable=True,
                                 omit=('associated_contents',)),
                    ['files', 'associated_contents', 'option', 'comment'])
    behaviors = [EditAnswer, Cancel]
    formid = 'formeditanswer'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    name = 'editAnswer'

    def before_update(self):
        options = getattr(self.context.question, 'options', [])
        if options:
            self.schema.get('option').widget = options_choice(options)
        else:
            self.schema.children.remove(
                self.schema.get('option'))

        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': EditAnswer.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='commentform comment-inline-form answerform novaideo-ajax-form deform')

    def default_data(self):
        return self.context


@view_config(
    name='editanswer',
    context=Answer,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditAnswerView(MultipleView):
    title = _('Edit the answer')
    name = 'editanswer'
    wrapper_template = 'novaideo:views/templates/view_wrapper.pt'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (EditAnswerFormView, )
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/comment.js']}

DEFAULTMAPPING_ACTIONS_VIEWS.update({EditAnswer: EditAnswerView})
