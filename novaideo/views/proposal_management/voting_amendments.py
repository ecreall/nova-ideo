from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.proposal_management.behaviors import  VotingAmendments
from novaideo.content.proposal import Proposal
from novaideo import _


@view_config(
    name='votingamendments',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class VotingAmendmentsView(BasicView):
    title = _('Voting amendments')
    name = 'votingamendments'
    behaviors = [VotingAmendments]
    viewid = 'votingamendments'


    def update(self):
        self.execute(None)        
        return list(self.behaviorinstances.values())[0].redirect(self.context, self.request)

DEFAULTMAPPING_ACTIONS_VIEWS.update({VotingAmendments:VotingAmendmentsView})
