# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS

from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.working_group_management.behaviors import (
    EditAction)
from novaideo.content.working_group import WorkingGroup, WorkingGroupSchema
from novaideo import _


@view_config(
    name='edit_wg',
    context=WorkingGroup,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditView(FormView):

    title = _('Edit')
    schema = select(WorkingGroupSchema(factory=WorkingGroup, 
                                       editable=True), [u'title'])
    behaviors = [EditAction]
    formid = 'formeditaction'
    name = 'edit_wg'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update({EditAction:EditView})