from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.proposal_management.behaviors import  AmendmentsResult
from novaideo.content.proposal import Proposal
from novaideo import _


@view_config(
    name='amendmentsresult',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class AmendmentsResultView(BasicView):
    title = _('Amendments result')
    name = 'amendmentsresult'
    behaviors = [AmendmentsResult]
    viewid = 'amendmentsresult'


    def update(self):
        self.execute(None)        
        return self.behaviorinstances.values()[0].redirect(self.context, self.request)

DEFAULTMAPPING_ACTIONS_VIEWS.update({AmendmentsResult:AmendmentsResultView})
