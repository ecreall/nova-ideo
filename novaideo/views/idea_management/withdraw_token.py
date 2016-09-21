# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.idea_management.behaviors import (
    WithdrawToken)
from novaideo.content.idea import Idea
from novaideo import _


@view_config(
    name='withdrawtokenidea',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class WithdrawTokenView(BasicView):
    title = _('Withdraw my token')
    name = 'withdrawtokenidea'
    behaviors = [WithdrawToken]
    viewid = 'withdrawtokenidea'

    def update(self):
        results = self.execute(None)
        return results[0]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {WithdrawToken: WithdrawTokenView})
