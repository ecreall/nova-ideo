# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view_operation import MultipleView
from pontus.default_behavior import Cancel

from novaideo.content.processes.proposal_management.behaviors import (
    SubmitProposalModeration)
from novaideo.content.proposal import Proposal
from .publish_proposal import (
    PublishProposalStudyReport, PublishProposalFormView)
from novaideo import _


class SubmitProposalViewStudyReport(PublishProposalStudyReport):
    title = _('Alert for submission')
    name = 'alertforsubmission'
    template = 'novaideo:views/proposal_management/templates/alert_proposal_submission.pt'


class SubmitProposalView(PublishProposalFormView):
    title = _('Submit for publication')
    name = 'submitproposalform'
    formid = 'formsubmitproposal'
    behaviors = [SubmitProposalModeration, Cancel]
    validate_behaviors = False
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/proposal_management.js']}

    def before_update(self):
        super(SubmitProposalView, self).before_update()
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': SubmitProposalModeration.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form  publish-proposal-form')


@view_config(
    name='submitproposalmoderation',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PublishProposalViewMultipleView(MultipleView):
    title = _('Submit for publication')
    name = 'submitproposal'
    viewid = 'submitproposal'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (SubmitProposalViewStudyReport, SubmitProposalView)
    validators = [SubmitProposalModeration.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SubmitProposalModeration: PublishProposalViewMultipleView})
