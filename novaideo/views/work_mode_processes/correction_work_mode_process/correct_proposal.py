# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select
from pontus.default_behavior import Cancel

from novaideo.content.processes.work_mode_processes.correction_work_mode_process.behaviors import (
    CorrectProposal)
from novaideo.content.proposal import Proposal
from novaideo.content.correction import Correction, CorrectionSchema
from novaideo import _


@view_config(
    name='improveproposalcorrection',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CorrectProposalView(FormView):
    title = _('Improve the proposal')
    name = 'improveproposalcorrection'
    behaviors = [CorrectProposal, Cancel]
    viewid = 'improveproposalcorrection'
    formid = 'formcorrectproposal'
    schema = select(CorrectionSchema(factory=Correction,
                                     editable=True,
                                     widget=deform.widget.FormWidget(
                                                css_class='amendmentform')),
                    ['title', 'description', 'text'])
    requirements = {'css_links': [],
                    'js_links': []}

    def default_data(self):
        return {'title': self.context.title,
                'text': self.context.text,
                'description': self.context.description}


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CorrectProposal: CorrectProposalView})
