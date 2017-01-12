# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from substanced.util import Batch, get_oid

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from dace.util import find_catalog, getSite
from pontus.view import BasicView
from pontus.util import merge_dicts
from pontus.view_operation import MultipleView

from novaideo.utilities.util import render_listing_objs
from novaideo.content.processes.reports_management.behaviors import SeeReports
from novaideo import _
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.views.filter import find_entities
from novaideo.core import SignalableEntity
from novaideo.content.interface import ISReport
from novaideo.utilities.util import generate_navbars, ObjectRemovedException


CONTENTS_MESSAGES = {
    '0': _(u"""No element found"""),
    '1': _(u"""One element found"""),
    '*': _(u"""${nember} elements found""")
}


class ReportView(BasicView):
    template = 'novaideo:views/novaideo_view_manager/templates/home.pt'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    report_state = 'pending'

    def update(self):
        user = get_current()
        context_oid = get_oid(self.context)
        dace_index = find_catalog('dace')
        dace_container_oid = dace_index['container_oid']
        query = dace_container_oid.eq(context_oid)
        objects = find_entities(
            user=user,
            interfaces=[ISReport],
            metadata_filter={
                'states': [self.report_state]
            },
            add_query=query)
        url = self.request.resource_url(
            self.context, '',
            query={'view_report_state': self.report_state})
        batch = Batch(objects,
                      self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        self.title = _(self.title, mapping={'nb': batch.seqlen})
        batch.target = "#results"+"-report-" + self.report_state.replace(' ', '')
        result_body, result = render_listing_objs(
            self.request, batch, user)
        values = {'bodies': result_body,
                  'batch': batch,
                  'empty_message': self.empty_message,
                  'empty_icon': self.empty_icon}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class OldReportView(ReportView):
    title = _('Previous reports (${nb})')
    report_state = 'processed'
    viewid = 'old-reporst'
    view_icon = 'icon glyphicon glyphicon-time'
    empty_message = _("No previous report")
    empty_icon = 'icon glyphicon glyphicon-time'


class NewReportsView(ReportView):
    title = _('New reports (${nb})')
    report_state = 'pending'
    viewid = 'new-reporst'
    view_icon = 'icon md md-sms-failed'
    empty_message = _("No new report")
    empty_icon = 'icon md md-sms-failed'


class SeeReportsPartsView(MultipleView):
    name = 'seereportsparts'
    template = 'novaideo:views/templates/multipleview.pt'
    viewid = 'seereportsparts'
    css_class = 'reports-parts-view media-body'
    views = (NewReportsView, OldReportView)

    def _init_views(self, views, **kwargs):
        if self.params('view_report_state') == 'pending':
            views = (NewReportsView, )

        if self.params('view_report_state') == 'processed':
            views = (OldReportView, )

        super(SeeReportsPartsView, self)._init_views(views, **kwargs)


class DetailSubjectView(BasicView):
    title = _('Details')
    name = 'detailssubject'
    template = 'novaideo:views/reports_management/templates/see_reports.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    viewid = 'detailssubject'

    def update(self):
        self.execute(None)
        try:
            navbars = generate_navbars(
                self.request, self.context,
                process_id='reportsmanagement',
                descriminators=['plus-action'],
                flatten=True)
        except ObjectRemovedException:
            return HTTPFound(self.request.resource_url(getSite(), ''))

        result = {}
        values = {
            'navbar_body': navbars['navbar_body'],
            'object': self.context
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = navbars['messages']
        item['isactive'] = navbars['isactive']
        result.update(navbars['resources'])
        result['coordinates'] = {self.coordinates: [item]}
        return result


@view_config(
    name='seereports',
    context=SignalableEntity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeReportsView(MultipleView):
    name = 'seereports'
    behaviors = [SeeReports]
    template = 'novaideo:views/reports_management/templates/reports_multiple_view.pt'
    viewid = 'seereports'
    views = (DetailSubjectView, SeeReportsPartsView)


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeReports: SeeReportsView})
