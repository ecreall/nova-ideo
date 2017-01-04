# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.reports_management.behaviors import Ignore
from novaideo.core import SignalableEntity
from novaideo import _


class IgnoreViewStudyIgnore(BasicView):
    title = _('Alert for ignoreing')
    name = 'alertforpublication'
    template = 'novaideo:views/reports_management/templates/alert_ignore.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class IgnoreFormView(FormView):

    title = _('Ignore')
    behaviors = [Ignore, Cancel]
    formid = 'formignore'
    name = 'formignore'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Ignore.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='ignore',
    context=SignalableEntity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class IgnoreView(MultipleView):
    title = _('Ignore')
    name = 'ignore'
    behaviors = [Ignore]
    viewid = 'ignoreentity'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (IgnoreViewStudyIgnore, IgnoreFormView)
    validators = [Ignore.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Ignore: IgnoreView})
