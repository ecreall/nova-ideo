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

from novaideo.content.processes.organization_management.behaviors import (
    WithdrawUser)
from novaideo.content.person import Person
from novaideo import _


class WithdrawViewStudyReport(BasicView):
    title = _('Alert for deletion')
    name = 'alertWithdraw'
    template = 'novaideo:views/organization_management/templates/alert_withdraw.pt'

    def update(self):
        result = {}
        values = {'user': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class WithdrawForm(FormView):
    title = _('Withdraw user from the organization')
    name = 'withdrawuserform'
    behaviors = [WithdrawUser, Cancel]
    viewid = 'withdrawuserform'
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': WithdrawUser.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


@view_config(
    name='withdrawuser',
    context=Person,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class WithdrawView(MultipleView):
    title = _('Withdraw user from the organization')
    name = 'withdrawuser'
    behaviors = [WithdrawUser]
    viewid = 'withdrawuser'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (WithdrawViewStudyReport, WithdrawForm)
    validators = [WithdrawUser.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {WithdrawUser: WithdrawView})
