from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.proposal_management.behaviors import  CreateProposal
from novaideo.content.proposal import ProposalSchema, Proposal
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


@view_config(
    name='createproposal',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class CreateProposalView(FormView):

    title = _('Create a proposal')
    schema = select(ProposalSchema(factory=Proposal, editable=True,
                               omit=['keywords', 'related_ideas']),
                    ['title',
                     'description',
                     'keywords',
                     'related_ideas'])
    behaviors = [CreateProposal, Cancel]
    formid = 'formcreateproposal'
    name='createproposal'


DEFAULTMAPPING_ACTIONS_VIEWS.update({CreateProposal: CreateProposalView})
