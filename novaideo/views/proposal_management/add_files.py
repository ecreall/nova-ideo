# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.proposal_management.behaviors import (
    AddFiles)
from novaideo.content.workspace import Workspace, WorkspaceSchema
from novaideo import _


@view_config(
    name='addfilesws',
    context=Workspace,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AddFilesView(FormView):

    title = _('Add files')
    schema = select(WorkspaceSchema(),
                    ['files'])
    behaviors = [AddFiles, Cancel]
    formid = 'formaddfilesws'
    name = 'addfilesws'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': AddFiles.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {AddFiles: AddFilesView})
