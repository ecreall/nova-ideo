from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.proposal_management.behaviors import  EditProposal
from novaideo.content.proposal import ProposalSchema, Proposal
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


@view_config(
    name='editproposal',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class EditProposalView(FormView):

    title = _('Edit')
    schema = select(ProposalSchema(factory=Proposal, editable=True,
                               omit=['keywords']),
                    ['title',
                     'description',
                     'keywords',
                     'text'])
    behaviors = [EditProposal, Cancel]
    formid = 'formeditproposal'
    name='editproposal'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update({EditProposal: EditProposalView})
