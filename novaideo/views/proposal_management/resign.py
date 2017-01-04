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

from novaideo.content.processes.proposal_management.behaviors import Resign
from novaideo.content.proposal import Proposal
from novaideo import _


class ResignViewStudyReport(BasicView):
    title = 'Alert:  for publication'
    name = 'alertforresign'
    template = 'novaideo:views/proposal_management/templates/alert_resign.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class ResignView(FormView):
    title = _('Quit')
    name = 'resignform'
    formid = 'formresign'
    behaviors = [Resign, Cancel]
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Resign.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='resign',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ResignViewMultipleView(MultipleView):
    title = _('Quit')
    name = 'resign'
    behaviors = [Resign]
    viewid = 'resign'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (ResignViewStudyReport, ResignView)
    validators = [Resign.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({Resign: ResignViewMultipleView})
