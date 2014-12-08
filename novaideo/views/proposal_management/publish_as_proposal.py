# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView
from pontus.default_behavior import Cancel
from pontus.view_operation import MultipleView
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.proposal_management.behaviors import (
    PublishAsProposal)
from novaideo.content.idea import Idea
from novaideo.content.proposal import ProposalSchema
from novaideo import _



class PublishAsProposalStudyReport(BasicView):
    title = _('Alert for transformation')
    name = 'alertfortransformation'
    template ='novaideo:views/proposal_management/templates/alert_proposal_transformation.pt'

    def update(self):
        result = {}
        body = self.content(result={}, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class PublishAsProposalFormView(FormView):

    title = _('Transform the idea into a proposal')
    schema = select(ProposalSchema(), ['title', 'description'])
    formid = 'formpublishasproposal'
    behaviors = [PublishAsProposal, Cancel]
    name = 'publishasproposal'

    def default_data(self):
        localizer = self.request.localizer
        title = self.context.title + \
                    localizer.translate(_(" (the proposal)"))
        return {'title': title}


@view_config(
    name='publishasproposal',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PublishAsProposalView(MultipleView):
    title = _('Transform the idea into a proposal')
    name = 'publishasproposal'
    viewid = 'publishasproposal'
    template = 'daceui:templates/mergedmultipleview.pt'
    views = (PublishAsProposalStudyReport, PublishAsProposalFormView)
    validators = [PublishAsProposal.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({PublishAsProposal:PublishAsProposalView})
