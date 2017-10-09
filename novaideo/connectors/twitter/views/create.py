# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.connectors.twitter.content.behaviors import CreateConnector
from novaideo.connectors.twitter import TwitterConnectorSchema, TwitterConnector
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


@view_config(
    name='createtwitterconnector',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CreateTwitterConnectorView(FormView):

    title = _('Add a Twitter connector')
    schema = select(TwitterConnectorSchema(factory=TwitterConnector, editable=True),
                    ['auth_conf'])
    behaviors = [CreateConnector, Cancel]
    formid = 'formcreatetwitterconnector'
    name = 'createtwitterconnector'


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CreateConnector: CreateTwitterConnectorView})
