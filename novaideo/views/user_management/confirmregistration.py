# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.user_management.behaviors import (
    ConfirmRegistration)
from novaideo.content.person import Preregistration, PersonSchema
from novaideo import _


@view_config(
    name='',
    context=Preregistration,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ConfirmRegistrationView(FormView):

    title = _('Registration confirmation')
    schema = select(PersonSchema(),
                    ['password'])
    behaviors = [ConfirmRegistration, Cancel]
    formid = 'formregistration'
    name = ''
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/user_management.js']}


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {ConfirmRegistration: ConfirmRegistrationView})
