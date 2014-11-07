
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.idea_management.behaviors import  RecuperateIdea
from novaideo.content.idea import Idea
from novaideo import _


@view_config(
    name='recuperateidea',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class RecuperateIdeaView(BasicView):
    title = _('Recuperate')
    name = 'recuperateidea'
    behaviors = [RecuperateIdea]
    viewid = 'recuperateidea'

    def update(self):
        self.execute(None)        
        return list(self.behaviorinstances.values())[0].redirect(self.context, 
                                                                 self.request)


DEFAULTMAPPING_ACTIONS_VIEWS.update({RecuperateIdea:RecuperateIdeaView})
