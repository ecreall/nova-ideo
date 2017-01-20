# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view import BasicView
from pontus.view_operation import MultipleView
from pontus.default_behavior import Cancel

from novaideo.content.processes.question_management.behaviors import DelQuestion
from novaideo.content.question import Question
from novaideo import _


class RemoveViewStudyReport(BasicView):
    title = _('Alert for deletion')
    name = 'alertfordeletion'
    template = 'novaideo:views/question_management/templates/alert_remove.pt'

    def update(self):
        result = {}
        values = {'question': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class RemoveForm(FormView):
    title = _('Remove the question')
    name = 'delquestionform'
    behaviors = [DelQuestion, Cancel]
    viewid = 'delquestionform'
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': DelQuestion.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='delquestion',
    context=Question,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DelQuestionView(MultipleView):
    title = _('Question deletion')
    name = 'delquestion'
    behaviors = [DelQuestion]
    viewid = 'delquestion'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (RemoveViewStudyReport, RemoveForm)
    validators = [DelQuestion.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {DelQuestion: DelQuestionView})
