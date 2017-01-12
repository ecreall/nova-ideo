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

from novaideo.content.processes.reports_management.behaviors import Restor
from novaideo.core import SignalableEntity
from novaideo import _


class RestorViewStudyRestor(BasicView):
    title = _('Alert for restoring')
    name = 'alertforpublication'
    template = 'novaideo:views/reports_management/templates/alert_restor.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class RestorFormView(FormView):

    title = _('Restore')
    behaviors = [Restor, Cancel]
    formid = 'formrestor'
    name = 'formrestor'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Restor.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='restor',
    context=SignalableEntity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class RestorView(MultipleView):
    title = _('Restore')
    name = 'restor'
    behaviors = [Restor]
    viewid = 'restorentity'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (RestorViewStudyRestor, RestorFormView)
    validators = [Restor.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Restor: RestorView})
