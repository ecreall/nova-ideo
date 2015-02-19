# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

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
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DuplicateIdeaView(FormView):
    title = _('Duplicate the idea')
    name = 'duplicateidea'
    schema = select(IdeaSchema(), ['title',
                                  'text',
                                  'keywords',
                                  'attached_files',
                                  'note'])
    behaviors = [DuplicateIdea, Cancel]
    formid = 'formduplicateidea'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update({DuplicateIdea:DuplicateIdeaView})
