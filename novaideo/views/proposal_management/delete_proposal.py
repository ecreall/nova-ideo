# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import Schema

from novaideo.content.processes.proposal_management.behaviors import (
    DeleteProposal)
from novaideo.content.proposal import Proposal
from novaideo.views.widget import LimitedTextAreaWidget
from novaideo import _



class ExplanationSchema(Schema):

    explanation = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=600),
        widget=LimitedTextAreaWidget(rows=5, 
                                     cols=30, 
                                     limit=600),
        title=_("Explanation")
        )


@view_config(
    name='deleteproposal',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DeleteProposalFormView(FormView):
    title = _('Proposal deletion')
    schema = ExplanationSchema()
    behaviors = [DeleteProposal, Cancel]
    formid = 'formdeleteproposal'
    name = 'deleteproposal'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update({DeleteProposal: DeleteProposalFormView})
