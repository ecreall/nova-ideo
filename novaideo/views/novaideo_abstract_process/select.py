# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.novaideo_abstract_process.behaviors import (
    SelectEntity, SelectEntityAnonymous)
from novaideo import _
from novaideo.core import SearchableEntity
from novaideo.views.core import ActionAnonymousView


@view_config(
    name='selectentity',
    context=SearchableEntity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SelectEntityView(BasicView):
    title = _('Add to my favourites')
    name = 'selectentity'
    behaviors = [SelectEntity]
    viewid = 'selectentity'

    def update(self):
        results = self.execute(None)
        return results[0]


@view_config(
    name='selectentityanonymous',
    context=SearchableEntity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SelectEntityAnonymousView(ActionAnonymousView):
    behaviors = [SelectEntityAnonymous]
    name = 'selectentityanonymous'


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SelectEntityAnonymous: SelectEntityAnonymousView})


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SelectEntity: SelectEntityView})
