# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.default_behavior import Cancel

from novaideo.content.processes.proposal_management.behaviors import (
    PublishProposalModeration)
from novaideo.content.proposal import Proposal
from novaideo import _


class PublishProposalViewStudyReport(BasicView):
    title = _('Alert for publication')
    name = 'alertforpublication'
    template = 'novaideo:views/proposal_management/templates/alert_proposal_publish.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class PublishProposalView(FormView):
    title = _('Publish')
    name = 'publishproposalmoderationform'
    formid = 'formpublishproposalmoderation'
    behaviors = [PublishProposalModeration, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': PublishProposalModeration.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='publishproposalmoderation',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PublishProposalViewMultipleView(MultipleView):
    title = _('Publish the proposal')
    name = 'publishproposalmoderation'
    behaviors = [PublishProposalModeration]
    viewid = 'publishproposalmoderation'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (PublishProposalViewStudyReport, PublishProposalView)
    validators = [PublishProposalModeration.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {PublishProposalModeration: PublishProposalViewMultipleView})
