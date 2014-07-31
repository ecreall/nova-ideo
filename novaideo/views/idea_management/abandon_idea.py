from pyramid.view import view_config

from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import CallSelectedContextsViews
from pontus.schema import select
from pontus.view import BasicView, View, merge_dicts, ViewError

from novaideo.content.processes.idea_management.behaviors import  AbandonIdea
from novaideo.content.idea import Idea
from novaideo import _


@view_config(
    name='abandonidea',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class AbandonIdeaView(BasicView):
    title = _('Abandon')
    name = 'abandonidea'
    behaviors = [AbandonIdea]
    viewid = 'abandonidea'


    def update(self):
        self.execute(None)        
        return self.behaviorinstances.values()[0].redirect(self.context, self.request)

DEFAULTMAPPING_ACTIONS_VIEWS.update({AbandonIdea:AbandonIdeaView})
