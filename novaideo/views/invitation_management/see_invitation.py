from pyramid.view import view_config

from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import CallSelectedContextsViews
from pontus.schema import select
from pontus.view import BasicView, View, merge_dicts, ViewError

from novaideo.content.processes.invitation_management.behaviors import  SeeInvitation
from novaideo.content.novaideo_application import NovaIdeoApplication
from .see_invitations import SeeInvitationsView
from novaideo import _


@view_config(
    name='seeinvitation',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class SeeInvitationView(BasicView):
    title = _('Details')
    name = 'seeinvitation'
    behaviors = [SeeInvitation]
    template = 'novaideo:views/invitation_management/templates/see_invitation.pt'
    viewid = 'seeinvitation'


    def update(self):
        invitation_id = self.params('invitation_id')
        try:
            invitation = get_obj(int(invitation_id)) 
        except Exception:
            e = ViewError()
            e.principalmessage = _("Invitation is not valid")
            raise e

        self.execute(None)        
        invitationsview = SeeInvitationsView(self.context, self.request)
        action_updated, messages, resources, actions = invitationsview._actions(invitation)
        result = {}
        state = None
        if invitation.state:
            state = invitation.state[0]

        values = {
                'actions':actions,
                'first_name': getattr(invitation, 'first_name',''),
                'last_name': getattr(invitation, 'last_name',''),
                'user_title': getattr(invitation, 'user_title', ''),
                'roles':getattr(invitation, 'roles', ''),
                'organization':getattr(invitation, 'organization', None),
                'state': state
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = action_updated
        result['coordinates'] = {self.coordinates:[item]}
        result.update(resources)
        result  = merge_dicts(self.requirements_copy, result)
        return result

DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeInvitation:SeeInvitationView})
