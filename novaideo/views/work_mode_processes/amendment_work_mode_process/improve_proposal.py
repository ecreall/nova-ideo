# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select
from pontus.default_behavior import Cancel

from novaideo.content.processes.work_mode_processes.amendment_work_mode_process.behaviors import (
    ImproveProposal)
from novaideo.content.proposal import Proposal
from novaideo.content.amendment import AmendmentSchema
from novaideo import _


@view_config(
    name='improveproposal',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ImproveProposalView(FormView):
    title = _('Improve the proposal')
    name = 'improveproposal'
    viewid = 'improveproposal'
    formid = 'formimproveproposal'
    behaviors = [ImproveProposal, Cancel]
    schema = select(AmendmentSchema(),
                    ['text'])
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/proposal_management.js']}

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update({ImproveProposal:ImproveProposalView})
