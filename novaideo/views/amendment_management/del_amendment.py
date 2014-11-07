
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.amendment_management.behaviors import (
    DelAmendment)
from novaideo.content.amendment import Amendment
from novaideo import _


@view_config(
    name='delamendment',
    context=Amendment,
    renderer='pontus:templates/view.pt',
    )
class DelAmendmentView(BasicView):
    title = _('Delete')
    name = 'delamendment'
    behaviors = [DelAmendment]
    viewid = 'delamendment'


    def update(self):
        self.execute(None)        
        return list(self.behaviorinstances.values())[0].redirect(self.context,
                                                                  self.request)

DEFAULTMAPPING_ACTIONS_VIEWS.update({DelAmendment:DelAmendmentView})