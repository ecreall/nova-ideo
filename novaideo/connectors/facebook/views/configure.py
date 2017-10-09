# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.connectors.facebook.content.behaviors import Configure
from novaideo.connectors.facebook import FacebookConnectorSchema, FacebookConnector
from novaideo import _


@view_config(
    name='configurefacebookconnector',
    context=FacebookConnector,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ConfigureFacebookConnectorView(FormView):

    title = _('Configure the Facebook connector')
    schema = select(FacebookConnectorSchema(editable=True),
                    ['auth_conf'])
    behaviors = [Configure, Cancel]
    formid = 'formconfigurefacebookconnector'
    name = 'configurefacebookconnector'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Configure: ConfigureFacebookConnectorView})
