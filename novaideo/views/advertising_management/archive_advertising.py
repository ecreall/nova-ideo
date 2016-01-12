# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config


from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.advertising_management.behaviors import (
    ArchiveAdvertising)
from novaideo.content.web_advertising import Advertising
from novaideo import _


class ArchiveAdvertisingViewStudyReport(BasicView):
    title = 'Alert for archive'
    name = 'alertforarchive'
    template = 'novaideo:views/advertising_management/templates/alert_archive.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class ArchiveAdvertisingView(FormView):
    title = _('Archive')
    name = 'archiveadvertisingform'
    formid = 'formarchiveadvertising'
    behaviors = [ArchiveAdvertising, Cancel]
    validate_behaviors = False


@view_config(
    name='archiveadvertising',
    context=Advertising,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ArchiveAdvertisingViewMultipleView(MultipleView):
    title = _('Archive the announcement')
    name = 'archiveadvertising'
    viewid = 'archiveadvertising'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    views = (ArchiveAdvertisingViewStudyReport, ArchiveAdvertisingView)
    validators = [ArchiveAdvertising.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {ArchiveAdvertising: ArchiveAdvertisingViewMultipleView})
