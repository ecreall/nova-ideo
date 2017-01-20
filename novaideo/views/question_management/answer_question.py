# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView

from novaideo.content.processes.question_management.behaviors import (
    AnswerQuestion)
from novaideo.content.question import (
    AnswerSchema as AnswerSchemaBase, Question, Answer)
from novaideo import _
from novaideo.utilities.util import get_emoji_form


def options_choice(options):
    values = list(enumerate(options))
    return deform.widget.RadioChoiceWidget(values=values, inline=True,)


@colander.deferred
def comment_textarea(node, kw):
    request = node.bindings['request']
    emoji_form = get_emoji_form(
        request, emoji_class='comment-form-group')
    return deform.widget.TextAreaWidget(
        rows=2, cols=60, item_css_class="comment-form-group comment-textarea",
        emoji_form=emoji_form,
        template='novaideo:views/templates/textarea_answer.pt')


class AnswerSchema(AnswerSchemaBase):

    options = colander.SchemaNode(
        colander.Int(),
        default=0,
        title=_('Options'),
        )

    comment = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        widget=comment_textarea,
        title=_("Message")
        )


class AnswerQuestionFormView(FormView):

    title = _('Answer the question')
    schema = select(AnswerSchema(factory=Answer,
                                 editable=True,
                                 omit=('related_contents',)),
                    ['files', 'related_contents', 'options', 'comment'])
    behaviors = [AnswerQuestion, Cancel]
    formid = 'formanswerquestion'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    name = 'answerQuestion'

    def before_update(self):
        options = getattr(self.context, 'options', [])
        if options:
            self.schema.get('options').widget = options_choice(options)
        else:
            self.schema.children.remove(
                self.schema.get('options'))

        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': AnswerQuestion.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='commentform comment-inline-form answerform novaideo-ajax-form deform')


@view_config(
    name='answerquestion',
    context=Question,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AnswerQuestionView(MultipleView):
    title = _('Answer the question')
    name = 'answerquestion'
    wrapper_template = 'novaideo:views/templates/view_wrapper.pt'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (AnswerQuestionFormView, )
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/comment.js']}


DEFAULTMAPPING_ACTIONS_VIEWS.update({AnswerQuestion: AnswerQuestionView})
