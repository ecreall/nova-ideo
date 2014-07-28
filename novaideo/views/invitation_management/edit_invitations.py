from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.invitation_management.behaviors import  EditInvitations
from novaideo.content.novaideo_application import NovaIdeoApplicationSchema, NovaIdeoApplication



@view_config(
    name='editinvitations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class EditInvitationsView(FormView):

    title = 'Edit invitations'
    schema = select(NovaIdeoApplicationSchema(editable=True),[(u'invitations',[ 'title',
                                                                                'user_title',
                                                                                'roles',
                                                                                'first_name', 
                                                                                'last_name',
                                                                                'email',
                                                                                'organization'])])
    behaviors = [EditInvitations]
    formid = 'formeditinvitations'
    name='editinvitations'

    def default_data(self):
        return self.context

DEFAULTMAPPING_ACTIONS_VIEWS.update({EditInvitations:EditInvitationsView})
