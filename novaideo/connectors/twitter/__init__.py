# -*- coding: utf8 -*-
# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
import deform
import urllib
import io
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode

from velruse import login_url
from pontus.schema import omit, Schema
from pontus.file import File, ObjectData as ObjectDataOrigine
from pontus.widget import Select2Widget

from novaideo.widget import SimpleMappingtWidget
from novaideo import _, log
from novaideo.connectors import IConnector, ConnectorSchema, Connector
from novaideo.utilities.data_manager import interface
from novaideo.connectors.core import TWITTER_CONNECTOR_ID


_default_user_name = 'Anonymous Anonymous'


def upload_file(url):
    try:
        buf = io.BytesIO(urllib.request.urlopen(url).read())
        buf.seek(0)
        filename = url.split('/')[-1]
        return File(
            fp=buf,
            filename=filename)
    except Exception as e:
        log.warning(e)
        return None


@interface()
class ITwitterConnector(IConnector):
    pass


class ObjectData(ObjectDataOrigine):

    def clean_cstruct(self, node, cstruct):
        result, appstruct, hasevalue = super(ObjectData, self)\
            .clean_cstruct(node, cstruct)

        if 'auth_conf' in result:
            auth_conf = result.pop('auth_conf')
            result.update(auth_conf)

        return result, appstruct, hasevalue


def context_is_a_twitter(context, request):
    return request.registry.content.istype(context, 'twitter')


class AuthSchema(Schema):

    log_in = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Login with a Twitter account'),
        description=_('Users can login with their Twitter account.'),
        title='',
        missing=False
    )


class TwitterConnectorSchema(ConnectorSchema):
    """Schema for idea"""

    typ_factory = ObjectData

    name = NameSchemaNode(
        editing=context_is_a_twitter,
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
    'twitter',
    icon='icon novaideo-icon icon-idea',
    )
@implementer(ITwitterConnector)
class TwitterConnector(Connector):
    """TwitterConnector class"""

    type_title = _('Twitter')
    connector_id = TWITTER_CONNECTOR_ID
    templates = {'default': 'novaideo:connectors/twitter/views/templates/twitter_bloc.pt',
                 'bloc': 'novaideo:connectors/twitter/views/templates/twitter_bloc.pt',
                 'small': 'novaideo:connectors/twitter/views/templates/twitter_bloc.pt',
                 'popover': 'novaideo:connectors/twitter/views/templates/twitter_bloc.pt'}

    def __init__(self, **kwargs):
        super(TwitterConnector, self).__init__(**kwargs)
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
        source_data = user.get_source_data(TWITTER_CONNECTOR_ID) if hasattr(user, 'get_source_data') else {}
        access_tokens = source_data.get(
            'access_token', {})
        access_token = access_tokens.get('oauthAccessToken', None)
        access_token_secret = access_tokens.get('oauthAccessTokenSecret', None)
        return {'access_token': access_token, 'access_token_secret': access_token_secret}

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
            'email': account.get('email', None),
        }
        photos = sources.profile.get('photos', [])
        if photos:
            image_url = photos[0]['value']
            user_data['picture'] = upload_file(image_url)

        return source_data, user_data
