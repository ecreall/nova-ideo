# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.default_behavior import Cancel

from novaideo.content.processes.novaideo_file_management.behaviors import (
    Private)
from novaideo.content.file import FileEntity
from novaideo import _


class PrivateFileViewStudyReport(BasicView):
    title = _('Alert: content privatised')
    name = 'alertforprivate'
    template = 'novaideo:views/novaideo_file_management/templates/alert_private.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class PrivateFileView(FormView):
    title = _('Privatize')
    name = 'privatefileform'
    formid = 'formprivatefile'
    behaviors = [Private, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Private.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='privatefile',
    context=FileEntity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PrivateFileMultipleView(MultipleView):
    title = _('Privatize the document')
    name = 'privatefile'
    behaviors = [Private]
    viewid = 'privatefile'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (PrivateFileViewStudyReport, PrivateFileView)
    validators = [Private.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Private: PrivateFileMultipleView})
