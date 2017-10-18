# -*- coding: utf8 -*-
# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode

from velruse import login_url
from pontus.schema import omit, Schema
from pontus.file import ObjectData as ObjectDataOrigine
from pontus.widget import Select2Widget

from novaideo.widget import SimpleMappingtWidget
from novaideo import _
from novaideo.connectors import IConnector, ConnectorSchema, Connector
from novaideo.utilities.data_manager import interface
from novaideo.connectors.core import GOOGLE_CONNECTOR_ID


_default_user_name = 'Anonymous Anonymous'


@interface()
class IGoogleConnector(IConnector):
    pass


class ObjectData(ObjectDataOrigine):

    def clean_cstruct(self, node, cstruct):
        result, appstruct, hasevalue = super(ObjectData, self)\
            .clean_cstruct(node, cstruct)

        if 'auth_conf' in result:
            auth_conf = result.pop('auth_conf')
            result.update(auth_conf)

        return result, appstruct, hasevalue


def context_is_a_google(context, request):
    return request.registry.content.istype(context, 'google')


class AuthSchema(Schema):

    log_in = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Login with a Google account'),
        description=_('Users can login with their Google account.'),
        title='',
        missing=False
    )


class GoogleConnectorSchema(ConnectorSchema):
    """Schema for idea"""

    typ_factory = ObjectData

    name = NameSchemaNode(
        editing=context_is_a_google,
        )

    auth_conf = omit(
        AuthSchema(
            widget=SimpleMappingtWidget(
                mapping_css_class='controled-form object-well',
                ajax=True,
                activator_icon="glyphicon glyphicon-log-in",
                activator_title=_('Configure the autentication policy'))),
        ["_csrf_token_"])


@content(
    'google',
    icon='icon novaideo-icon icon-idea',
    )
@implementer(IGoogleConnector)
class GoogleConnector(Connector):
    """GoogleConnector class"""

    type_title = _('Google')
    connector_id = GOOGLE_CONNECTOR_ID
    templates = {'default': 'novaideo:connectors/google/views/templates/google_bloc.pt',
                 'bloc': 'novaideo:connectors/google/views/templates/google_bloc.pt',
                 'small': 'novaideo:connectors/google/views/templates/google_bloc.pt',
                 'popover': 'novaideo:connectors/google/views/templates/google_bloc.pt'}

    def __init__(self, **kwargs):
        super(GoogleConnector, self).__init__(**kwargs)
        self.consumer_key = kwargs.get('consumer_key', None)
        self.consumer_secret = kwargs.get('consumer_secret', None)

    @property
    def auth_conf(self):
        return self.get_data(omit(AuthSchema(),
                                  '_csrf_token_'))

    def set_client_data(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def get_login_url(self, request):
        return login_url(request, self.connector_id)

    def get_access_tokens(self, user):
        source_data = user.get_source_data(GOOGLE_CONNECTOR_ID) if hasattr(user, 'get_source_data') else {}
        access_tokens = source_data.get(
            'access_token', {})
        access_token = access_tokens.get('oauthAccessToken', None)
        return {'access_token': access_token}

    def extract_data(self, sources):
        account = sources.profile.get('accounts')[0]
        source_data = {
            'app_name': sources.provider_name,
            'id': account['userid'],
            'access_token': sources.credentials
        }
        user_name = sources.profile.get(
            'preferredUsername', '')
        user_name = user_name or _default_user_name
        name_parts = user_name.split(' ')
        first_name, *last_name = name_parts
        last_name = ' '.join(last_name)
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'password': None,
            'email': account.get('email', None)
        }
        return source_data, user_data
