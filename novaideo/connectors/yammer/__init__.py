
import colander
import deform
from zope.interface import implementer
import yampy

from substanced.content import content
from substanced.schema import NameSchemaNode

from pontus.schema import omit, Schema
from pontus.file import ObjectData as ObjectDataOrigine
from pontus.widget import Select2Widget

from novaideo.widget import SimpleMappingtWidget
from novaideo.connectors.yammer.views.widget import YammerNotificationWidget
from novaideo import _
from novaideo.connectors import IConnector, ConnectorSchema, Connector
from novaideo.utilities.data_manager import interface


@interface()
class IYammerConnector(IConnector):
    pass


class ObjectData(ObjectDataOrigine):

    def clean_cstruct(self, node, cstruct):
        result, appstruct, hasevalue = super(ObjectData, self)\
            .clean_cstruct(node, cstruct)

        if 'auth_conf' in result:
            auth_conf = result.pop('auth_conf')
            result.update(auth_conf)

        if 'notif_conf' in result:
            notif_conf = result.pop('notif_conf')
            result.update(notif_conf)

        return result, appstruct, hasevalue


def context_is_a_yammer(context, request):
    return request.registry.content.istype(context, 'yammer')


class AuthSchema(Schema):

    log_in = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Login with a Yammer account'),
        description=_('Users can login with their Yammer account.'),
        title='',
        missing=False
    )

    networks = colander.SchemaNode(
        colander.Set(),
        widget=Select2Widget(
            values=[],
            create=True,
            multiple=True),
        title=_('Trusted networks'),
        description=_("To add trusted network, you need to tap the « Enter »"
                      " key after each network or to separate them with commas."),
        missing=[]
        )


@colander.deferred
def only_from_default_widget(node, kw):
    context = node.bindings['context']
    access_token = getattr(context, 'access_token', None)
    item_css_class = 'yammer-only-from-default'
    if not access_token:
        item_css_class += ' hide-bloc'

    return deform.widget.CheckboxWidget(
        item_css_class=item_css_class)


@colander.deferred
def access_token_widget(node, kw):
    request = node.bindings['request']
    context = node.bindings['context']
    client_id = request.registry.settings['yammer.client_id']
    client_id = getattr(context, 'client_id', client_id)
    return YammerNotificationWidget(app_id=client_id)


class NotificationSchema(Schema):

    enable_notifications = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Enable notifications on Yammer'),
        description=_('Send a notification to Yammer when new content is published.'),
        title='',
        missing=False
    )

    access_token = colander.SchemaNode(
        colander.String(),
        widget=access_token_widget,
        title=_('Default notification account'),
        missing=''
        )

    only_from_default = colander.SchemaNode(
        colander.Boolean(),
        widget=only_from_default_widget,
        label=_('Notify only from the default account'),
        title='',
        missing=False
    )


class YammerConnectorSchema(ConnectorSchema):
    """Schema for idea"""

    typ_factory = ObjectData

    name = NameSchemaNode(
        editing=context_is_a_yammer,
        )

    auth_conf = omit(
        AuthSchema(
            widget=SimpleMappingtWidget(
                mapping_css_class='controled-form object-well',
                ajax=True,
                activator_icon="glyphicon glyphicon-log-in",
                activator_title=_('Configure the autentication policy'))),
        ["_csrf_token_"])

    notif_conf = omit(
        NotificationSchema(
            widget=SimpleMappingtWidget(
                mapping_css_class='controled-form object-well',
                ajax=True,
                activator_icon="glyphicon glyphicon-bell",
                activator_title=_('Configure notifications'))),
        ["_csrf_token_"])


@content(
    'yammer',
    icon='icon novaideo-icon icon-idea',
    )
@implementer(IYammerConnector)
class YammerConnector(Connector):
    """YammerConnector class"""

    type_title = _('Yammer')
    connector_id = 'yammer'
    templates = {'default': 'novaideo:connectors/yammer/views/templates/yammer_bloc.pt',
                 'bloc': 'novaideo:connectors/yammer/views/templates/yammer_bloc.pt',
                 'small': 'novaideo:connectors/yammer/views/templates/yammer_bloc.pt',
                 'popover': 'novaideo:connectors/yammer/views/templates/yammer_bloc.pt'}

    def __init__(self, **kwargs):
        super(YammerConnector, self).__init__(**kwargs)
        self.client_id = kwargs.get('client_id', None)
        self.client_secret = kwargs.get('client_secret', None)
        self.authenticator = None
        if self.client_id and self.client_secret:
            self.set_client_data(self.client_id, self.client_secret)

    @property
    def auth_conf(self):
        return self.get_data(omit(AuthSchema(),
                                  '_csrf_token_'))

    @property
    def notif_conf(self):
        return self.get_data(omit(NotificationSchema(),
                                  '_csrf_token_'))

    def set_client_data(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authenticator = yampy.Authenticator(
            client_id=self.client_id, client_secret=self.client_secret)

    def get_auth_url(self, redirect_uri):
        return self.authenticator.authorization_url(redirect_uri=redirect_uri)

    def get_login_url(self, request):
        redirect_uri = request.resource_url(request.root, 'yammerlogin')
        return self.get_auth_url(redirect_uri)
