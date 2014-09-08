from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.proposal_management.behaviors import  Amendable
from novaideo.content.proposal import Proposal
from novaideo import _


@view_config(
    name='amendable',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class AmendableView(BasicView):
    title = _('Amendable')
    name = 'amendable'
    behaviors = [Amendable]
    viewid = 'amendable'


    def update(self):
        self.execute(None)        
        return list(self.behaviorinstances.values())[0].redirect(self.context, self.request)

DEFAULTMAPPING_ACTIONS_VIEWS.update({Amendable:AmendableView})
