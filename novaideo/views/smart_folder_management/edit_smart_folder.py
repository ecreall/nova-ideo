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

from novaideo.content.processes.smart_folder_management.behaviors import (
    EditSmartFolder)
from novaideo.content.smart_folder import (
    SmartFolderSchema, SmartFolder)
from novaideo import _


@view_config(
    name='editsmartfolder',
    context=SmartFolder,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditSmartFolderView(FormView):

    title = _('Edit the topic of interest')
    schema = select(SmartFolderSchema(factory=SmartFolder, editable=True),
                    ['title',
                     'description',
                     'locale',
                     'view_type',
                     'icon_data',
                     # 'style',
                     'filters',
                     'contents'])
    behaviors = [EditSmartFolder, Cancel]
    formid = 'formeditsmartfolder'
    name = 'editsmartfolder'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': EditSmartFolder.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {EditSmartFolder: EditSmartFolderView})
