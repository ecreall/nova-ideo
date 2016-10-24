# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
import deform
import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.user_management.behaviors import (
    ConfirmRegistration)
from novaideo.content.person import Preregistration, PersonSchema
from novaideo import _


class ConfirmRegistrationSchema(PersonSchema):

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
        title=_("Password"),
        description=_('Please choose a password to confirm your subscription')
        )


@view_config(
    name='',
    context=Preregistration,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ConfirmRegistrationView(FormView):

    title = _('Registration confirmation')
    schema = select(ConfirmRegistrationSchema(),
                    ['email', 'password'])
    behaviors = [ConfirmRegistration, Cancel]
    formid = 'formregistration'
    name = ''
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/user_management.js']}

    def default_data(self):
        return {'email': getattr(self.context, 'email')}

    def before_update(self):
        if self.request.POST:
            self.request.POST.update(self.default_data())

        return super(ConfirmRegistrationView, self).before_update()


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {ConfirmRegistration: ConfirmRegistrationView})
