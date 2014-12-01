# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.proposal_management.behaviors import (
    PublishProposal)
from novaideo.content.proposal import Proposal
from novaideo import _


@view_config(
    name='publishproposal',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PublishProposalView(BasicView):
    title = _('Submit the proposal')
    name = 'publishproposal'
    behaviors = [PublishProposal]
    viewid = 'publishproposal'


    def update(self):
        self.execute(None)        
        return list(self.behaviorinstances.values())[0].redirect(
                                       self.context, self.request)


DEFAULTMAPPING_ACTIONS_VIEWS.update({PublishProposal:PublishProposalView})