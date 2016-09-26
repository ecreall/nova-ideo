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
    AttachFiles)
from novaideo.content.proposal import AddFilesSchemaSchema, Proposal
from novaideo import _


@view_config(
    name='attachfiles',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AttachFilesView(FormView):
    title = _('Attach files to the proposal')
    schema = select(AddFilesSchemaSchema(),
                    ['ws_files', 'attached_files'])
    behaviors = [AttachFiles, Cancel]
    formid = 'formattachfiles'
    name = 'attachfiles'

    def default_data(self):
        return {'ws_files': self.context.attached_files}

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': AttachFiles.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {AttachFiles: AttachFilesView})
