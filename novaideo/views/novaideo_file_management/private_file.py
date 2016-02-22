# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.default_behavior import Cancel

from novaideo.content.processes.novaideo_file_management.behaviors import (
    Private)
from novaideo.core import FileEntity
from novaideo import _


class PrivateFileViewStudyReport(BasicView):
    title = _('Alert for private')
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


@view_config(
    name='privatefile',
    context=FileEntity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PrivateFileMultipleView(MultipleView):
    title = _('Privatize the file')
    name = 'privatefile'
    behaviors = [Private]
    viewid = 'privatefile'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    views = (PrivateFileViewStudyReport, PrivateFileView)
    validators = [Private.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Private: PrivateFileMultipleView})
