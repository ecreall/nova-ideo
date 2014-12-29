# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from substanced.interfaces import IUserLocator, IPasswordReset
from substanced.principal import DefaultUserLocator

from dace.processinstance.core import  Behavior
from pontus.form import FormView
from pontus.schema import Schema

from novaideo import _
from novaideo.content.novaideo_application import NovaIdeoApplication


class Send(Behavior):

    behavior_id = "send"
    title = _("Send")
    description = ""

    def start(self, context, request, appstruct, **kw):
        login = appstruct['email']
        adapter = request.registry.queryMultiAdapter(
                    (context, request),
                    IUserLocator
                    )
        if adapter is None:
            adapter = DefaultUserLocator(context, request)

        user = adapter.get_user_by_email(login)
        if user is not None:
            user.email_password_reset(request)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, ""))


@colander.deferred
def login_validator(node, kw):
    context = kw['context']
    request = kw['request']
    def _login_validator(node, value):
        adapter = request.registry.queryMultiAdapter(
                    (context, request),
                    IUserLocator
                    )
        if adapter is None:
            adapter = DefaultUserLocator(context, request)

        user = adapter.get_user_by_email(value)
        if user is None:
            raise colander.Invalid(node, 'No such user %s' % value)

    return _login_validator


class ResetRequestSchema(Schema):
    """ The schema for validating password reset requests."""
    email = colander.SchemaNode(
        colander.String(),
        validator = login_validator,
        )


@view_config(
    name='resetpassword',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ResetRequestView(FormView):
    title = _('Request Password Reset')
    schema = ResetRequestSchema()
    behaviors = [Send]



class Reset(Behavior):
    behavior_id = "send"
    title = _("Send")
    description = ""

    def start(self, context, request, appstruct, **kw):
        context.reset_password(appstruct['new_password'])
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(request.virtual_root, "@@login"))


class ResetSchema(Schema):
    """ The schema for validating password reset requests."""
    new_password = colander.SchemaNode(
        colander.String(),
        validator = colander.Length(min=3, max=100),
        widget = deform.widget.CheckedPasswordWidget(),
        )


@view_config(
    name='',
    context=IPasswordReset,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ResetView(FormView):
    title = _('Reset Password')
    schema = ResetSchema()
    behaviors = [Reset]


