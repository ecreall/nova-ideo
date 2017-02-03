# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
from zope.interface import invariant
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.view import BasicView
from pontus.schema import select

from novaideo.views.widget import TOUCheckboxWidget, ReCAPTCHAWidget
from novaideo.content.processes.user_management.behaviors import (
    Registration)
from novaideo.content.person import PersonSchema, Preregistration
from novaideo.content.novaideo_application import (
    NovaIdeoApplication)
from novaideo import _


@colander.deferred
def conditions_widget(node, kw):
    request = node.bindings['request']
    terms_of_use = request.root['terms_of_use']
    return TOUCheckboxWidget(tou_file=terms_of_use)


class RegistrationSchema(PersonSchema):

    accept_conditions = colander.SchemaNode(
        colander.Boolean(),
        widget=conditions_widget,
        label=_('I have read and accept the terms and conditions.'),
        title='',
        missing=False
    )

    captcha = colander.SchemaNode(
        colander.String(),
        widget=ReCAPTCHAWidget(),
        label=_('I have read and accept the terms and conditions.'),
        title='',
        missing=''
    )

    @invariant
    def captcha_invariant(self, appstruct):
        captcha = appstruct.get('captcha', '')
        if not captcha:
            raise colander.Invalid(
                self, _('Invalid captcha'))


@view_config(
    name='registration',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class RegistrationView(FormView):

    title = _('Your registration')
    schema = select(RegistrationSchema(factory=Preregistration,
                                       editable=True,
                                       omit=['captcha']),
                    ['user_title',
                     'first_name',
                     'last_name',
                     'email',
                     'accept_conditions',
                     'captcha'])
    behaviors = [Registration, Cancel]
    formid = 'formregistration'
    name = 'registration'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/user_management.js']}


@view_config(
    name='registrationsubmitted',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class RegistrationSubmittedView(BasicView):
    template = 'novaideo:views/user_management/templates/registrationsubmitted.pt'
    title = _('Please confirm your registration')
    name = 'registrationsubmitted'
    viewid = 'deactivateview'

    def before_update(self):
        moderate_registration = getattr(
            self.context, 'moderate_registration', False)
        if moderate_registration:
            self.title = _('Your registration is submitted to moderation')

    def update(self):
        result = {}
        body = self.content(args={}, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({Registration: RegistrationView})
