# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.default_behavior import Cancel
from pontus.schema import Schema

from novaideo.views.widget import LimitedTextAreaWidget
from novaideo.content.processes.challenge_management.behaviors import (
    ArchiveChallenge)
from novaideo.content.challenge import Challenge
from novaideo import _


class ArchiveChallengeViewStudyReport(BasicView):
    title = _('Alert for archiving')
    name = 'alertforpublication'
    template = 'novaideo:views/challenge_management/templates/alert_challenge_archive.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class ArchiveChallengeSchema(Schema):

    explanation = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=300),
        widget=LimitedTextAreaWidget(rows=5,
                                     cols=30,
                                     limit=300),
        title=_("Explanation")
        )


class ArchiveChallengeView(FormView):
    title = _('Archive')
    name = 'archivechallengeform'
    formid = 'formarchivechallenge'
    schema = ArchiveChallengeSchema()
    behaviors = [ArchiveChallenge, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': ArchiveChallenge.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='material-form deform novaideo-ajax-form')


@view_config(
    name='archivechallenge',
    context=Challenge,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ArchiveChallengeViewMultipleView(MultipleView):
    title = _('Archive the challenge')
    name = 'archivechallenge'
    viewid = 'archivechallenge'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (ArchiveChallengeViewStudyReport, ArchiveChallengeView)
    validators = [ArchiveChallenge.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {ArchiveChallenge: ArchiveChallengeViewMultipleView})
