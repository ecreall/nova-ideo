# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform.widget
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite
from pontus.form import FormView
from pontus.schema import Schema

from novaideo.content.processes.invitation_management.behaviors import (
    AcceptInvitation)
from novaideo.content.invitation import Invitation
from novaideo.views.widget import TOUCheckboxWidget
from novaideo import _


@colander.deferred
def conditions_widget(node, kw):
    root = getSite()
    terms_of_use = root['terms_of_use']
    return TOUCheckboxWidget(tou_file=terms_of_use)


class AcceptInvitationSchema(Schema):

    email = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextInputWidget(
            template='novaideo:views/templates/disabled_text_input.pt'),
        title=_('Login (email)'),
        missing=''
        )

    password = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.CheckedPasswordWidget(),
        validator=colander.Length(min=3, max=100),
        description=_('Please choose a password to confirm your subscription'),
        title=_('Password')
        )

    accept_conditions = colander.SchemaNode(
        colander.Boolean(),
        widget=conditions_widget,
        label=_('I have read and accept the terms and conditions'),
        title='',
        missing=False
    )


@view_config(
    name='accept_invitation',
    context=Invitation,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AcceptInvitationView(FormView):
    title = _('Validate the invitation')
    schema = AcceptInvitationSchema()
    behaviors = [AcceptInvitation]
    formid = 'formacceptinvitation'
    name = 'accept_invitation'

    def default_data(self):
        return {'email': getattr(self.context, 'email')}

    def before_update(self):
        if self.request.POST:
            self.request.POST.update(self.default_data())

        return super(AcceptInvitationView, self).before_update()


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {AcceptInvitation: AcceptInvitationView})
