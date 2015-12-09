# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.idea_management.behaviors import (
    SupportIdea)
from novaideo.content.idea import Idea
from novaideo import _


@view_config(
    name='supportidea',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SupportIdeaView(BasicView):
    title = _('Support')
    name = 'supportidea'
    behaviors = [SupportIdea]
    viewid = 'supportidea'

    def update(self):
        results = self.execute(None)
        return results[0]

DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SupportIdea: SupportIdeaView})
