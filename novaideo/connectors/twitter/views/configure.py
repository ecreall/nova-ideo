# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.connectors.twitter.content.behaviors import Configure
from novaideo.connectors.twitter import TwitterConnectorSchema, TwitterConnector
from novaideo import _


@view_config(
    name='configuretwitterconnector',
    context=TwitterConnector,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ConfigureTwitterConnectorView(FormView):

    title = _('Configure the Twitter connector')
    schema = select(TwitterConnectorSchema(editable=True),
                    ['auth_conf'])
    behaviors = [Configure, Cancel]
    formid = 'formconfiguretwitterconnector'
    name = 'configuretwitterconnector'
    css_class = 'panel-transparent'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Configure: ConfigureTwitterConnectorView})
