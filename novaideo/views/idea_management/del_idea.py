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

from novaideo.content.processes.idea_management.behaviors import DelIdea
from novaideo.content.idea import Idea
from novaideo import _


class RemoveViewStudyReport(BasicView):
    title = _('Alert for deletion')
    name = 'alertfordeletion'
    template = 'novaideo:views/organization_management/templates/alert_remove.pt'

    def update(self):
        result = {}
        values = {'idea': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class RemoveForm(FormView):
    title = _('Remove the idea')
    name = 'delideaform'
    behaviors = [DelIdea, Cancel]
    viewid = 'delideaform'
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': DelIdea.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='delidea',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DelIdeaView(MultipleView):
    title = _('Idea deletion')
    name = 'delidea'
    behaviors = [DelIdea]
    viewid = 'delidea'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (RemoveViewStudyReport, RemoveForm)
    validators = [DelIdea.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {DelIdea: DelIdeaView})
