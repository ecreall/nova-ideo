from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.idea_management.behaviors import  CreatIdea
from novaideo.content.idea import IdeaSchema, Idea
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


@view_config(
    name='creatidea',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class CreatIdeaView(FormView):

    title = _('Edit invitations')
    schema = select(IdeaSchema(factory=Idea, editable=True),['title',
                                                             'description',
                                                              ('keywords', ['title']),
                                                              'text'])
    behaviors = [CreatIdea]
    formid = 'formcreatidea'
    name='creatidea'


DEFAULTMAPPING_ACTIONS_VIEWS.update({CreatIdea:CreatIdeaView})
