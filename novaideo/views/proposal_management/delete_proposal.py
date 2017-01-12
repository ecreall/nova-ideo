# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
import colander
from pyramid.view import view_config

from dace.objectofcollaboration.principal.util import has_role
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import Schema, omit
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.proposal_management.behaviors import (
    DeleteProposal)
from novaideo.content.proposal import Proposal
from novaideo.views.widget import LimitedTextAreaWidget
from novaideo import _


class DeleteProposalViewStudyReport(BasicView):
    title = _('Alert for deletion')
    name = 'alertfordeletion'
    template = 'novaideo:views/proposal_management/templates/alert_proposal_deletion.pt'

    def update(self):
        result = {}
        values = {'context': self.context,
                  'draft_owner': getattr(self.parent, 'is_draft_owner', False)}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class ExplanationSchema(Schema):

    explanation = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=600),
        widget=LimitedTextAreaWidget(rows=5,
                                     cols=30,
                                     limit=600),
        title=_("Explanation")
        )


class DeleteProposalFormView(FormView):
    title = _('Delete the proposal')
    schema = ExplanationSchema()
    behaviors = [DeleteProposal, Cancel]
    formid = 'formdeleteproposal'
    name = 'deleteproposalform'

    def default_data(self):
        return self.context

    def before_update(self):
        if getattr(self.parent, 'is_draft_owner', False):
            self.schema = omit(self.schema, ['explanation'])

        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': DeleteProposal.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='deleteproposal',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DeleteProposalView(MultipleView):
    title = _('Delete the proposal')
    name = 'deleteproposal'
    behaviors = [DeleteProposal]
    viewid = 'deleteproposal'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (DeleteProposalViewStudyReport, DeleteProposalFormView)
    validators = [DeleteProposal.get_validator()]

    def before_update(self):
        self.is_draft_owner = False
        if 'draft' in self.context.state and \
            has_role(role=('Owner', self.context)):
            self.is_draft_owner = True

        super(DeleteProposalView, self).before_update()

DEFAULTMAPPING_ACTIONS_VIEWS.update({DeleteProposal: DeleteProposalView})
