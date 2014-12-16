# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.novaideo_abstract_process.behaviors import  (
    EditDeadLine)
from novaideo.content.novaideo_application import (
    NovaIdeoApplication, NovaIdeoApplicationSchema)
from novaideo import _


@view_config(
    name='editdeadline',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditDeadLineView(FormView):

    title = _('Edit the current deadline')
    schema = select(NovaIdeoApplicationSchema(), ['deadline'])
    behaviors = [EditDeadLine, Cancel]
    formid = 'formeditdeadline'
    name = 'editdeadline'

    def default_data(self):
        return {'deadline': self.context.deadlines[-1]}

DEFAULTMAPPING_ACTIONS_VIEWS.update({EditDeadLine: EditDeadLineView})