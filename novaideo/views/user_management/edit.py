# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, Schema

from novaideo.content.processes.user_management.behaviors import Edit
from novaideo.content.person import PersonSchema, Person
from novaideo.views.widget import SimpleMappingtWidget
from novaideo import _


class Password_validator(object):
    def __call__(self, node, value):
        """ Returns a ``colander.Function`` validator that uses the context (user)
        to validate the password."""
        user = get_current()
        if value['changepassword'] and \
           not user.check_password(value['currentuserpassword']):
            raise colander.Invalid(
                node.get('currentuserpassword'),
                _(' Invalid current password'))

        if value['changepassword']:
            colander.Length(min=3, max=100)(node.get('password'),
                                            value['password'])


class UserPasswordSchema(Schema):
    """ The schema for validating password change requests."""
    currentuserpassword = colander.SchemaNode(
        colander.String(),
        title=_('Your Current Password'),
        widget=deform.widget.PasswordWidget(redisplay=True),
        missing=''
        )
    password = colander.SchemaNode(
        colander.String(),
        title=_('New Password'),
        widget=deform.widget.CheckedPasswordWidget(redisplay=False),
        missing=''
        )

    changepassword = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(css_class="hide-bloc"),
        label='',
        title='',
        default=False,
        missing=False
        )


class EditPersonSchema(PersonSchema):

    change_password = UserPasswordSchema(
        widget=SimpleMappingtWidget(
            mapping_css_class="controled-form change-password-form hide-bloc",
            ajax=True,
            activator_icon="glyphicon glyphicon-asterisk",
            activator_title=_('Change Password')),
        validator=Password_validator())


@view_config(
    name='edit',
    context=Person,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditView(FormView):

    title = _('Edit the profile')
    schema = select(EditPersonSchema(factory=Person,
                                     editable=True,
                                     omit=('change_password', )),
                    ['user_title',
                     'first_name',
                     'last_name',
                     'function',
                     'description',
                     'keywords',
                     'picture',
                     'email',
                     'locale',
                     'change_password'])
    behaviors = [Edit, Cancel]
    formid = 'formedit'
    name = 'edit'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/user_management.js']}

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update({Edit: EditView})
