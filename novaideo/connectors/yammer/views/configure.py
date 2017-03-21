# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.connectors.yammer.content.behaviors import Configure
from novaideo.connectors.yammer import YammerConnectorSchema, YammerConnector
from novaideo import _


@view_config(
    name='configureyammerconnector',
    context=YammerConnector,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ConfigureYammerConnectorView(FormView):

    title = _('Configure the Yammer connector')
    schema = select(YammerConnectorSchema(editable=True),
                    ['auth_conf',
                     'notif_conf'])
    behaviors = [Configure, Cancel]
    formid = 'formconfigureyammerconnector'
    name = 'configureyammerconnector'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Configure: ConfigureYammerConnectorView})
