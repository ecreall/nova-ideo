# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.reports_management.behaviors import Report
from novaideo.content.report import ReportSchema, Report as ReportClass
from novaideo.core import SignalableEntity
from novaideo import _


class ReportViewStudyReport(BasicView):
    title = _('Alert for restoring')
    name = 'alertforpublication'
    template = 'novaideo:views/reports_management/templates/alert_report.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class ReportFormView(FormView):

    title = _('Report')
    schema = select(ReportSchema(
                        factory=ReportClass, editable=True),
                    ['reporting_reasons',
                     'details'])
    behaviors = [Report, Cancel]
    formid = 'formreport'
    name = 'formreport'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Report.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='report',
    context=SignalableEntity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ReportView(MultipleView):
    title = _('Report')
    name = 'report'
    behaviors = [Report]
    viewid = 'reportentity'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (ReportViewStudyReport, ReportFormView)
    validators = [Report.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Report: ReportView})
