# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, Schema
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.user_management.behaviors import GetAPIToken
from novaideo.content.person import PersonSchema, Person
from novaideo.widget import SimpleMappingtWidget
from novaideo import _


class DisplayAPITokenStudyReport(BasicView):

    title = _('API token')
    name = 'display_api_token'
    template = 'novaideo:views/user_management/templates/display_api_token.pt'

    def update(self):
        result = {}
        if 'invalid_password' in self.request.GET:
            self.request.sdiapi.flash(
                _('Your password is incorrect. Please try again'), 'danger')

        values = {
            'api_token': getattr(self.context, 'api_token', None)
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class GetAPITokenSchema(Schema):

    password = colander.SchemaNode(
        colander.String(),
        title=_('Please enter your password to generate a new API token'),
        widget=deform.widget.PasswordWidget(redisplay=True),
        missing=''
        )


class EditAPITokenView(FormView):

    title = _('Edit the API token')
    schema = GetAPITokenSchema()
    behaviors = [GetAPIToken]
    formid = 'formgetapitoken'
    name = 'get_api_token'


@view_config(
    name='get_api_token',
    context=Person,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class GetAPITokenView(MultipleView):
    title = _('Get API token')
    name = 'get_api_token'
    behaviors = [GetAPIToken]
    viewid = 'get_api_token'
    template = 'daceui:templates/mergedmultipleview.pt'
    views = (DisplayAPITokenStudyReport, EditAPITokenView)
    validators = [GetAPIToken.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({
    GetAPIToken: GetAPITokenView
})
