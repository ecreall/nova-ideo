from pyramid.view import view_config

from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.view_operation import CallSelectedContextsViews
from pontus.schema import select
from pontus.view import BasicView, View, merge_dicts, ViewError

from novaideo.content.processes.proposal_management.behaviors import  DuplicateProposal
from novaideo.content.proposal import Proposal, ProposalSchema
from novaideo import _


@view_config(
    name='duplicateproposal',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class DuplicateProposalView(FormView):
    title = _('Duplicate')
    name = 'duplicateproposal'
    schema = select(ProposalSchema(),['title',
                                  'description',
                                  'keywords',
                                  'text'])

    behaviors = [DuplicateProposal, Cancel]
    formid = 'formduplicateproposal'


    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update({DuplicateProposal:DuplicateProposalView})
