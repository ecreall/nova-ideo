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

from novaideo.content.processes.channel_management.behaviors import Subscribe
from novaideo.core import Channel
from novaideo import _


class SubscribeViewStudyReport(BasicView):
    title = _('Alert for subscription')
    name = 'alertfordeletion'
    template = 'novaideo:views/channel_management/templates/alert_subscribe.pt'

    def update(self):
        result = {}
        values = {'channel': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class SubscribeForm(FormView):
    title = _('Subscribe to the discussion')
    name = 'subscribechannelform'
    behaviors = [Subscribe, Cancel]
    viewid = 'subscribechannelform'
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Subscribe.node_definition.id})
        formwidget = deform.widget.FormWidget(css_class='channel-subscribe-form deform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='subscribechannel',
    context=Channel,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SubscribeView(MultipleView):
    title = _('Subscribe to the discussion')
    name = 'subscribechannel'
    behaviors = [Subscribe]
    viewid = 'subscribechannel'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (SubscribeViewStudyReport, SubscribeForm)
    validators = [Subscribe.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Subscribe: SubscribeView})
