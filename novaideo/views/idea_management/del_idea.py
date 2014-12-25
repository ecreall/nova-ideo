# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.idea_management.behaviors import  DelIdea
from novaideo.content.idea import Idea
from novaideo import _


@view_config(
    name='delidea',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DelIdeaView(BasicView):
    title = _('Delete')
    name = 'delidea'
    behaviors = [DelIdea]
    viewid = 'delidea'

    def update(self):
        results = self.execute(None)
        return results[0]


DEFAULTMAPPING_ACTIONS_VIEWS.update({DelIdea:DelIdeaView})
