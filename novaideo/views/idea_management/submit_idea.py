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

from novaideo.content.processes.idea_management.behaviors import SubmitIdea
from novaideo.content.idea import Idea
from novaideo import _


class SubmitIdeaViewStudyReport(BasicView):
    title = _('Alert for submission')
    name = 'alertforsubmission'
    template = 'novaideo:views/idea_management/templates/alert_idea_submission.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class SubmitIdeaView(FormView):
    title = _('Submit for publication')
    name = 'submitideaform'
    formid = 'formsubmitidea'
    behaviors = [SubmitIdea, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': SubmitIdea.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='submitidea',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PublishIdeaViewMultipleView(MultipleView):
    title = _('Submit for publication')
    name = 'submitidea'
    viewid = 'submitidea'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (SubmitIdeaViewStudyReport, SubmitIdeaView)
    validators = [SubmitIdea.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SubmitIdea: PublishIdeaViewMultipleView})
