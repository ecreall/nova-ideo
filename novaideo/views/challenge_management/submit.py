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

from novaideo.content.processes.challenge_management.behaviors import SubmitChallenge
from novaideo.content.challenge import Challenge
from novaideo import _


class SubmitChallengeViewStudyReport(BasicView):
    title = _('Alert for submission')
    name = 'alertforsubmission'
    template = 'novaideo:views/challenge_management/templates/alert_challenge_submission.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class SubmitChallengeView(FormView):
    title = _('Submit for publication')
    name = 'submitchallengeform'
    formid = 'formsubmitchallenge'
    behaviors = [SubmitChallenge, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': SubmitChallenge.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='submitchallenge',
    context=Challenge,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PublishChallengeViewMultipleView(MultipleView):
    title = _('Submit for publication')
    name = 'submitchallenge'
    viewid = 'submitchallenge'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (SubmitChallengeViewStudyReport, SubmitChallengeView)
    validators = [SubmitChallenge.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SubmitChallenge: PublishChallengeViewMultipleView})
