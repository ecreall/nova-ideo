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
    Publish)
from novaideo.content.file import FileEntity
from novaideo import _


class PublishFileViewStudyReport(BasicView):
    title = _('Alert for publication')
    name = 'alertforpublication'
    template = 'novaideo:views/novaideo_file_management/templates/alert_publish.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class PublishFileView(FormView):
    title = _('Publish')
    name = 'publishfileform'
    formid = 'formpublishfile'
    behaviors = [Publish, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Publish.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='publishfile',
    context=FileEntity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PublishFileMultipleView(MultipleView):
    title = _('Publish the document')
    name = 'publishfile'
    behaviors = [Publish]
    viewid = 'publishfile'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (PublishFileViewStudyReport, PublishFileView)
    validators = [Publish.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Publish: PublishFileMultipleView})
