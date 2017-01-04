# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.user_management.behaviors import (
    Deactivate)
from novaideo.content.person import Person
from novaideo import _


class DeactivateViewStudyReport(BasicView):
    title = 'Alert: disactivate the profile'
    name = 'alertfordisactivate'
    template = 'novaideo:views/user_management/templates/alert_deactivate_profile.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class DeactivateView(FormView):
    title = _('Disactivate the profile')
    name = 'disactivateform'
    formid = 'formdisactivate'
    behaviors = [Deactivate, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Deactivate.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='disactivate',
    context=Person,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DeactivateViewMultipleView(MultipleView):
    title = _('Disactivate the profile')
    name = 'disactivate'
    viewid = 'disactivate'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (DeactivateViewStudyReport, DeactivateView)
    validators = [Deactivate.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Deactivate: DeactivateViewMultipleView})
