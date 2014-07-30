from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.invitation_management.behaviors import  EditInvitation
from novaideo.content.invitation import InvitationSchema, Invitation
from novaideo import _


@view_config(
    name='editinvitation',
    context=Invitation,
    renderer='pontus:templates/view.pt',
    )
class EditInvitationView(FormView):

    title = _('Edit invitation')
    schema = select(InvitationSchema(editable=True),['title',
                                                     'user_title',
                                                     'roles',
                                                     'first_name', 
                                                     'last_name',
                                                     'email',
                                                     'organization'])
    behaviors = [EditInvitation]
    formid = 'formeditinvitation'
    name='editinvitation'

    def default_data(self):
        return self.context

DEFAULTMAPPING_ACTIONS_VIEWS.update({EditInvitation:EditInvitationView})
