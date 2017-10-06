# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.connectors.facebook.content.behaviors import CreateConnector
from novaideo.connectors.facebook import FacebookConnectorSchema, FacebookConnector
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


@view_config(
    name='createfacebookconnector',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CreateFacebookConnectorView(FormView):

    title = _('Add a Facebook connector')
    schema = select(FacebookConnectorSchema(factory=FacebookConnector, editable=True),
                    ['auth_conf'])
    behaviors = [CreateConnector, Cancel]
    formid = 'formcreatefacebookconnector'
    name = 'createfacebookconnector'


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CreateConnector: CreateFacebookConnectorView})
