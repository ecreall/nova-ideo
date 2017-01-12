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
    WithdrawSmartFolder)
from novaideo.content.smart_folder import SmartFolder
from novaideo import _


class WithdrawSmartFolderViewStudyReport(BasicView):
    title = 'Alert for withdraw'
    name = 'alertforwithdraw'
    template = 'novaideo:views/smart_folder_management/templates/alert_smartfolder_withdraw.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class WithdrawSmartFolderView(FormView):
    title = _('Withdraw')
    name = 'withdrawsmartfolderform'
    formid = 'formwithdrawsmartfolder'
    behaviors = [WithdrawSmartFolder, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': WithdrawSmartFolder.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='withdrawsmartfolder',
    context=SmartFolder,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class WithdrawSmartFolderViewMultipleView(MultipleView):
    title = _('Withdraw the topic of interest')
    name = 'withdrawsmartfolder'
    viewid = 'withdrawsmartfolder'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (WithdrawSmartFolderViewStudyReport, WithdrawSmartFolderView)
    validators = [WithdrawSmartFolder.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {WithdrawSmartFolder: WithdrawSmartFolderViewMultipleView})
