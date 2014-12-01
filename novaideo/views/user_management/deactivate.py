# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.user_management.behaviors import  Deactivate
from novaideo.content.person import Person
from novaideo import _


@view_config(
    name='deactivate',
    context=Person,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DeactivateView(BasicView):
    title = _('Deactivate the member')
    name = 'deactivate'
    behaviors = [Deactivate]
    viewid = 'deactivateview'


    def update(self):
        self.execute(None)        
        return list(self.behaviorinstances.values())[0].redirect(
                                       self.context, self.request)


DEFAULTMAPPING_ACTIONS_VIEWS.update({Deactivate:DeactivateView})