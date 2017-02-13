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

from novaideo.content.processes.challenge_management.behaviors import DelChallenge
from novaideo.content.challenge import Challenge
from novaideo import _


class RemoveViewStudyReport(BasicView):
    title = _('Alert for deletion')
    name = 'alertfordeletion'
    template = 'novaideo:views/organization_management/templates/alert_remove.pt'

    def update(self):
        result = {}
        values = {'challenge': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class RemoveForm(FormView):
    title = _('Remove the challenge')
    name = 'delchallengeform'
    behaviors = [DelChallenge, Cancel]
    viewid = 'delchallengeform'
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': DelChallenge.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='delchallenge',
    context=Challenge,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DelChallengeView(MultipleView):
    title = _('Challenge deletion')
    name = 'delchallenge'
    behaviors = [DelChallenge]
    viewid = 'delchallenge'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (RemoveViewStudyReport, RemoveForm)
    validators = [DelChallenge.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {DelChallenge: DelChallengeView})
