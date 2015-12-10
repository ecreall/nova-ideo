# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import Schema
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.admin_process.behaviors import (
    ManageKeywords)
from novaideo.content.novaideo_application import (
    NovaIdeoApplication)
from novaideo.content.site_configuration import keywords_choice
from novaideo import _


class ManageKeywordsViewStudyReport(BasicView):
    title = 'Alert for keywords'
    name = 'alertforkeywordsmanagement'
    template = 'novaideo:views/admin_process/templates/alert_event_keywords.pt'

    def update(self):
        result = {}
        values = {}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class ManageKeywordsSchema(Schema):

    targets = colander.SchemaNode(
        colander.Set(),
        widget=keywords_choice,
        title=_("Keywords")
        )

    source = colander.SchemaNode(
        colander.String(),
        title=_("New keyword")
        )


class ManageKeywordsFormView(FormView):

    title = _('Manage keywords')
    schema = ManageKeywordsSchema()
    behaviors = [ManageKeywords, Cancel]
    formid = 'formmanagekeywords'
    name = 'formmanagekeywords'


@view_config(
    name='managekeywords',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ManageKeywordsView(MultipleView):
    title = _('Manage keywords')
    name = 'managekeywords'
    viewid = 'managekeywords'
    template = 'daceui:templates/mergedmultipleview.pt'
    views = (ManageKeywordsViewStudyReport, ManageKeywordsFormView)
    validators = [ManageKeywords.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({ManageKeywords: ManageKeywordsView})
