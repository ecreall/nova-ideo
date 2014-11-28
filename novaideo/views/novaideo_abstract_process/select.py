# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.entity import Entity
from pontus.view import BasicView

from novaideo.content.processes.novaideo_abstract_process.behaviors import  (
    SelectEntity)
from novaideo import _


@view_config(
    name='selectentity',
    context=Entity,
    renderer='pontus:templates/view.pt',
    )
class SelectEntityView(BasicView):
    title = _('Add to my selections')
    name = 'selectentity'
    behaviors = [SelectEntity]
    viewid = 'selectentity'


    def update(self):
        self.execute(None)        
        return list(self.behaviorinstances.values())[0].redirect(
                                       self.context, self.request)


DEFAULTMAPPING_ACTIONS_VIEWS.update({SelectEntity:SelectEntityView})
