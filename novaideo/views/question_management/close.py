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
    Close)
from novaideo.content.question import Question
from novaideo import _


class CloseQuestionViewStudyReport(BasicView):
    title = _('Alert for archiving')
    name = 'alertforpublication'
    template = 'novaideo:views/question_management/templates/alert_question_close.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class CloseQuestionView(FormView):
    title = _('Close')
    name = 'closequestionform'
    formid = 'formclosequestion'
    behaviors = [Close, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Close.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='material-form deform novaideo-ajax-form')


@view_config(
    name='closequestion',
    context=Question,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CloseQuestionViewMultipleView(MultipleView):
    title = _('Close the question')
    name = 'closequestion'
    viewid = 'closequestion'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (CloseQuestionViewStudyReport, CloseQuestionView)
    validators = [Close.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Close: CloseQuestionViewMultipleView})
