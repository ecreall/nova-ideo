
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.proposal_management.behaviors import (
    PublishAsProposal)
from novaideo.content.idea import Idea
from novaideo import _


@view_config(
    name='publishasproposal',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class PublishAsProposalView(BasicView):
    title = _('Publish as a proposal')
    name = 'publishasproposal'
    behaviors = [PublishAsProposal]
    viewid = 'publishasproposal'

    def update(self):
        self.execute(None)
        return list(self.behaviorinstances.values())[0].redirect(
                                       self.context, self.request)


DEFAULTMAPPING_ACTIONS_VIEWS.update({PublishAsProposal:PublishAsProposalView})
