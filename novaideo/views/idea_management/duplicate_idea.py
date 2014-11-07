
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.idea_management.behaviors import  DuplicateIdea
from novaideo.content.idea import Idea, IdeaSchema
from novaideo import _


@view_config(
    name='duplicateidea',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class DuplicateIdeaView(FormView):
    title = _('Duplicate')
    name = 'duplicateidea'
    schema = select(IdeaSchema(), ['intention',
                                  'title',
                                  'description',
                                  'keywords',
                                  'text',
                                  'attached_files'])
    behaviors = [DuplicateIdea, Cancel]
    formid = 'formduplicateidea'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update({DuplicateIdea:DuplicateIdeaView})
