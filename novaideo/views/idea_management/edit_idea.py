from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.idea_management.behaviors import  EditIdea
from novaideo.content.idea import IdeaSchema, Idea
from novaideo import _


@view_config(
    name='editidea',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class EditIdeaView(FormView):

    title = _('Edit idea')
    schema = select(IdeaSchema(factory=Idea, editable=True),['title',
                                                             'description',
                                                             ('keywords', ['title']),
                                                             'text'])
    behaviors = [EditIdea, Cancel]
    formid = 'formeditidea'
    name='editidea'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update({EditIdea:EditIdeaView})
