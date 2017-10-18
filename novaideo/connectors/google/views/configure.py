# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.connectors.google.content.behaviors import Configure
from novaideo.connectors.google import GoogleConnectorSchema, GoogleConnector
from novaideo import _


@view_config(
    name='configuregoogleconnector',
    context=GoogleConnector,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ConfigureGoogleConnectorView(FormView):

    title = _('Configure the Google connector')
    schema = select(GoogleConnectorSchema(editable=True),
                    ['auth_conf'])
    behaviors = [Configure, Cancel]
    formid = 'formconfiguregoogleconnector'
    name = 'configuregoogleconnector'
    css_class = 'panel-transparent'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Configure: ConfigureGoogleConnectorView})
