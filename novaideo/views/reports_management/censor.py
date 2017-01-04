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
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.reports_management.behaviors import Censor
from novaideo.content.report import (
    ReportSchema, reporting_reasons_choice, Report)
from novaideo.core import SignalableEntity
from novaideo import _


class CensorViewStudyCensor(BasicView):
    title = _('Alert for censoring')
    name = 'alertforpublication'
    template = 'novaideo:views/reports_management/templates/alert_censor.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class CensorSchema(ReportSchema):
    """Schema for censoring"""

    reporting_reasons = colander.SchemaNode(
        colander.Set(),
        widget=reporting_reasons_choice,
        title=_("Censoring reasons")
        )


class CensorFormView(FormView):

    title = _('Censor')
    schema = select(CensorSchema(factory=Report, editable=True),
                    ['reporting_reasons',
                     'details'])
    behaviors = [Censor, Cancel]
    formid = 'formcensor'
    name = 'formcensor'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Censor.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='censor',
    context=SignalableEntity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CensorView(MultipleView):
    title = _('Censor')
    name = 'censor'
    behaviors = [Censor]
    viewid = 'censorentity'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (CensorViewStudyCensor, CensorFormView)
    validators = [Censor.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Censor: CensorView})
