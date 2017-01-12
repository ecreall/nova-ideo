# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view import BasicView
from pontus.view_operation import MultipleView
from pontus.default_behavior import Cancel
from pontus.file import File

from novaideo.content.processes.proposal_management.behaviors import (
    RemoveFile)
from novaideo import _


class RemoveViewStudyReport(BasicView):
    title = _('Alert for deletion')
    name = 'alertfordeletion'
    template = 'novaideo:views/proposal_management/templates/alert_remove_file.pt'

    def update(self):
        result = {}
        values = {'file': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class RemoveForm(FormView):
    title = _('Delete file')
    name = 'delfileform'
    behaviors = [RemoveFile, Cancel]
    viewid = 'delfileform'
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': RemoveFile.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='removefile',
    context=File,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DelFileView(MultipleView):
    title = _('Delete file')
    name = 'removefile'
    behaviors = [RemoveFile]
    viewid = 'removefile'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (RemoveViewStudyReport, RemoveForm)
    validators = [RemoveFile.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {RemoveFile: DelFileView})
