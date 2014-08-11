from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.idea_management.behaviors import  CreateIdea
from novaideo.content.idea import IdeaSchema, Idea
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


@view_config(
    name='createidea',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class CreateIdeaView(FormView):

    title = _('Create an idea')
    schema = select(IdeaSchema(factory=Idea, editable=True,
                               omit=['keywords']),
                    ['title',
                     'description',
                     'keywords',
                     'text'])
    behaviors = [CreateIdea, Cancel]
    formid = 'formcreateidea'
    name='createidea'


DEFAULTMAPPING_ACTIONS_VIEWS.update({CreateIdea: CreateIdeaView})
