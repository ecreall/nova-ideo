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
    Remind)
from novaideo.content.person import Preregistration
from novaideo import _


class RemindViewStudyReport(BasicView):
    title = 'Alert for remove'
    name = 'alertforremove'
    template = 'novaideo:views/user_management/templates/alert_remind_registration.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class RemindView(FormView):
    title = _('Remove')
    name = 'remindform'
    formid = 'formremind'
    behaviors = [Remind, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Remind.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='remind',
    context=Preregistration,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class RemindViewMultipleView(MultipleView):
    title = _('Remind the user')
    name = 'remind'
    viewid = 'remind'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (RemindViewStudyReport, RemindView)
    validators = [Remind.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Remind: RemindViewMultipleView})
