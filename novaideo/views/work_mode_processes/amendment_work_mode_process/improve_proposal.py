# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select
from pontus.default_behavior import Cancel
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.work_mode_processes.amendment_work_mode_process.behaviors import (
    ImproveProposal, ImproveProposalAndExplain)
from novaideo.content.proposal import Proposal
from novaideo.content.amendment import AmendmentSchema
from novaideo import _


class ImproveProposalStudyReport(BasicView):
    title = _('Alert improvement')
    name = 'alertforimprovement'
    template = 'novaideo:views/work_mode_processes/amendment_work_mode_process/templates/alert_improve.pt'

    def update(self):
        result = {}
        values = {'context': self.context,
                  'draft_owner': getattr(self.parent, 'is_draft_owner', False)}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class ImproveProposalForm(FormView):
    title = _('Improve the proposal')
    name = 'improveproposalform'
    viewid = 'improveproposalform'
    formid = 'formimproveproposal'
    behaviors = [ImproveProposalAndExplain, ImproveProposal, Cancel]
    schema = select(AmendmentSchema(),
                    ['text'])
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/proposal_management.js']}
    css_class = 'panel-transparent'

    def default_data(self):
        return self.context


@view_config(
    name='improveproposal',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ImproveProposalView(MultipleView):
    title = _('Improve the proposal')
    name = 'improveproposal'
    behaviors = [ImproveProposal]
    viewid = 'improveproposal'
    template = 'daceui:templates/mergedmultipleview.pt'
    css_class = 'panel-transparent'
    views = (ImproveProposalStudyReport, ImproveProposalForm)
    validators = [ImproveProposal.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({ImproveProposal:ImproveProposalView})
