# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from substanced.interfaces import IPasswordReset
from substanced.util import find_service

from dace.util import find_catalog
from dace.processinstance.core import Behavior
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.schema import Schema
from pontus.default_behavior import Cancel as DefaultCancel

from novaideo.content.interface import IPerson
from novaideo import _
from novaideo.utilities.alerts_utility import alert
from novaideo.content.novaideo_application import NovaIdeoApplication


class Cancel(DefaultCancel):

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(request.root, ""))


class Send(Behavior):

    behavior_id = "send"
    title = _("Send")
    description = ""

    def start(self, context, request, appstruct, **kw):
        login = appstruct['email']
        dace_catalog = find_catalog('dace')
        novaideo_catalog = find_catalog('novaideo')
        identifier_index = novaideo_catalog['identifier']
        object_provides_index = dace_catalog['object_provides']
        query = object_provides_index.any([IPerson.__identifier__]) &\
                identifier_index.any([login])
        users = list(query.execute().all())
        user = users[0] if users else None
        if user is not None:
            principals = find_service(user, 'principals')
            reset = principals.add_reset(user)
            reseturl = request.resource_url(reset)
            if not user.email:
                raise ValueError('User does not possess a valid email address.')

            root = request.root
            mail_template = root.get_mail_template('reset_password')
            subject = mail_template['subject'].format(
                novaideo_title=request.root.title)
            localizer = request.localizer
            message = mail_template['template'].format(
                recipient_title=localizer.translate(
                    _(getattr(user, 'user_title', ''))),
                recipient_first_name=getattr(user, 'first_name', user.name),
                recipient_last_name=getattr(user, 'last_name', ''),
                reseturl=reseturl,
                novaideo_title=request.root.title
            )
            alert('email', [root.get_site_sender()], [user.email],
                  subject=subject, body=message)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, ""))


@colander.deferred
def login_validator(node, kw):
    def _login_validator(node, value):
        dace_catalog = find_catalog('dace')
        novaideo_catalog = find_catalog('novaideo')
        identifier_index = novaideo_catalog['identifier']
        object_provides_index = dace_catalog['object_provides']
        query = object_provides_index.any([IPerson.__identifier__]) &\
                identifier_index.any([value])
        users = list(query.execute().all())
        user = users[0] if users else None
        if user is None:
            raise colander.Invalid(node, _('No such user ${member}',
                                            mapping={'member': value}))

    return _login_validator


class ResetRequestSchema(Schema):
    """ The schema for validating password reset requests."""
    email = colander.SchemaNode(
        colander.String(),
        validator=login_validator,
        title=_('Login (email)')
        )


class ResetRequestViewStudyReport(BasicView):
    title = _('Alert for reset')
    name = 'alertforreset'
    template = 'novaideo:views/user_management/templates/alert_reset.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class ResetRequestView(FormView):
    title = _('Request password reset')
    schema = ResetRequestSchema()
    behaviors = [Send, Cancel]


@view_config(
    name='resetpassword',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ResetRequestViewMultipleView(MultipleView):
    title = _('Request password reset')
    name = 'submitidea'
    viewid = 'submitidea'
    template = 'daceui:templates/mergedmultipleview.pt'
    views = (ResetRequestViewStudyReport, ResetRequestView)
    validators = [Send.get_validator()]


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
        validator=colander.Length(min=3, max=100),
        widget=deform.widget.CheckedPasswordWidget(),
        title=_("New Password")
        )


@view_config(
    name='',
    context=IPasswordReset,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ResetView(FormView):
    title = _('Reset Password')
    schema = ResetSchema()
    behaviors = [Reset, Cancel]
