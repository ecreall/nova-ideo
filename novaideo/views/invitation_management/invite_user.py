import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.widget import TableWidget, LineWidget
from pontus.schema import Schema, omit, select

from novaideo.content.processes.invitation_management.behaviors import  InviteUsers
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.content.invitation import InvitationSchema, Invitation


class InviteUsersSchema(Schema):

    invitations = colander.SchemaNode(
                colander.Sequence(),
                select(omit(InvitationSchema(factory=Invitation,
                                         editable=True,
                                         name='Invitation'),['_csrf_token_']), ['user_title',
                                                                                'roles',
                                                                                'first_name', 
                                                                                'last_name',
                                                                                'email',
                                                                                'organization']),
                title='Invitations'
                )


@view_config(
    name='inviteusers',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class InviteUserView(FormView):

    title = 'Invite users'
    schema = InviteUsersSchema()
    behaviors = [InviteUsers]
    formid = 'forminviteusers'
    name ='inviteusers'


DEFAULTMAPPING_ACTIONS_VIEWS.update({InviteUsers:InviteUserView})
