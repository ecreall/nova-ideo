from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.user_management.behaviors import  Registration
from novaideo.content.person import PersonSchema, Person
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


@view_config(
    name='registration',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class RegistrationView(FormView):

    title = _('Registration')
    schema = select(PersonSchema(factory=Person, editable=True),['user_title',
                                                     'first_name', 
                                                     'last_name',
                                                     'email',
                                                     'password'])
    behaviors = [Registration, Cancel]
    formid = 'formregistration'
    name='registration'


DEFAULTMAPPING_ACTIONS_VIEWS.update({Registration:RegistrationView})
