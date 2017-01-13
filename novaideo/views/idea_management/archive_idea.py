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
from novaideo.content.processes.idea_management.behaviors import (
    ArchiveIdea, ModerationArchiveIdea)
from novaideo.content.idea import Idea
from novaideo import _


class ArchiveIdeaViewStudyReport(BasicView):
    title = _('Alert for archiving')
    name = 'alertforpublication'
    template = 'novaideo:views/idea_management/templates/alert_idea_archive.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class ArchiveIdeaSchema(Schema):

    explanation = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=300),
        widget=LimitedTextAreaWidget(rows=5,
                                     cols=30,
                                     limit=300),
        title=_("Explanation")
        )


class ArchiveIdeaView(FormView):
    title = _('Archive')
    name = 'archiveideaform'
    formid = 'formarchiveidea'
    schema = ArchiveIdeaSchema()
    behaviors = [ArchiveIdea, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': ArchiveIdea.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='material-form deform novaideo-ajax-form')


@view_config(
    name='archiveidea',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ArchiveIdeaViewMultipleView(MultipleView):
    title = _('Archive the idea')
    name = 'archiveidea'
    viewid = 'archiveidea'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (ArchiveIdeaViewStudyReport, ArchiveIdeaView)
    validators = [ArchiveIdea.get_validator()]


class ModerationArchiveIdeaView(FormView):
    title = _('Archive')
    name = 'moderationarchiveideaform'
    formid = 'formmoderationarchiveidea'
    schema = ArchiveIdeaSchema()
    behaviors = [ModerationArchiveIdea, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': ModerationArchiveIdea.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='moderationarchiveidea',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ModerationArchiveIdeaViewMultipleView(MultipleView):
    title = _('Archive the idea')
    name = 'moderationarchiveidea'
    viewid = 'moderationarchiveidea'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (ArchiveIdeaViewStudyReport, ModerationArchiveIdeaView)
    validators = [ModerationArchiveIdea.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {ModerationArchiveIdea: ModerationArchiveIdeaViewMultipleView})


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {ArchiveIdea: ArchiveIdeaViewMultipleView})
