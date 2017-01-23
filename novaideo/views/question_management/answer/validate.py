# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.default_behavior import Cancel

from novaideo.content.processes.question_management.behaviors import (
    ValidateAnswer)
from novaideo.content.question import Answer
from novaideo import _


class ValidateAnswerViewStudyReport(BasicView):
    title = _('Alert for archiving')
    name = 'alertforpublication'
    template = 'novaideo:views/question_management/answer/templates/alert_answer_validate.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class ValidateAnswerView(FormView):
    title = _('Validate')
    name = 'validateanswerform'
    formid = 'formvalidateanswer'
    behaviors = [ValidateAnswer, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': ValidateAnswer.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='material-form deform novaideo-ajax-form')


@view_config(
    name='validateanswer',
    context=Answer,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ValidateAnswerViewMultipleView(MultipleView):
    title = _('Validate the answer')
    name = 'validateanswer'
    viewid = 'validateanswer'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (ValidateAnswerViewStudyReport, ValidateAnswerView)
    validators = [ValidateAnswer.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {ValidateAnswer: ValidateAnswerViewMultipleView})
