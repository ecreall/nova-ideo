# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.smart_folder_management.behaviors import (
    RemoveSmartFolder)
from novaideo.content.smart_folder import SmartFolder
from novaideo import _


class RemoveSmartFolderViewStudyReport(BasicView):
    title = 'Alert for remove'
    name = 'alertforremove'
    template = 'novaideo:views/smart_folder_management/templates/alert_smartfolder_remove.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class RemoveSmartFolderView(FormView):
    title = _('Remove')
    name = 'removesmartfolderform'
    formid = 'formremovesmartfolder'
    behaviors = [RemoveSmartFolder, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': RemoveSmartFolder.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='removesmartfolder',
    context=SmartFolder,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class RemoveSmartFolderViewMultipleView(MultipleView):
    title = _('Remove the topic of interest')
    name = 'removesmartfolder'
    viewid = 'removesmartfolder'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (RemoveSmartFolderViewStudyReport, RemoveSmartFolderView)
    validators = [RemoveSmartFolder.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {RemoveSmartFolder: RemoveSmartFolderViewMultipleView})
