from pyramid.view import view_config

from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import CallSelectedContextsViews
from pontus.schema import select
from pontus.view import BasicView, View, merge_dicts, ViewError

from novaideo.content.processes.idea_management.behaviors import  DelIdea
from novaideo.content.idea import Idea
from novaideo import _


@view_config(
    name='delidea',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class DelIdeaView(BasicView):
    title = _('Delete')
    name = 'delidea'
    behaviors = [DelIdea]
    viewid = 'delidea'


    def update(self):
        self.execute(None)        
        return list(self.behaviorinstances.values())[0].redirect(self.context, self.request)

DEFAULTMAPPING_ACTIONS_VIEWS.update({DelIdea:DelIdeaView})
