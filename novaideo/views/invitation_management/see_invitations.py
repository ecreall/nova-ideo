
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI

from novaideo.content.processes.invitation_management.behaviors import (
    SeeInvitations)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.content.processes import get_states_mapping
from novaideo import _


@view_config(
    name='seeinvitations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class SeeInvitationsView(BasicView):
    title = _('Invitations')
    name = 'seeinvitations'
    behaviors = [SeeInvitations]
    template = 'novaideo:views/invitation_management/templates/see_invitations.pt'
    viewid = 'seeinvitations'


    def update(self):
        self.execute(None)
        user = get_current()
        result = {}
        all_invitation_data = {'invitations':[]}
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,
                                                        'dace_ui_api')
        invitations_actions = dace_ui_api.get_actions(
                            self.context.invitations, self.request)
        action_updated, messages, \
        resources, actions = dace_ui_api.update_actions(self.request,
                                                            invitations_actions)
        for invitation in self.context.invitations:
            invitation_actions = [a for a in actions \
                                  if a['context'] is invitation]
            state = None
            if invitation.state:
                state = invitation.state[0]

            invitation_dic = { 
                'actions': invitation_actions,
                'url':self.request.resource_url(invitation, '@@index'), 
                'first_name': getattr(invitation, 'first_name',''),
                'last_name': getattr(invitation, 'last_name', ''),
                'user_title': getattr(invitation, 'user_title', ''),
                'roles':getattr(invitation, 'roles', ''),
                'organization':getattr(invitation, 'organization', None),
                'state': get_states_mapping(user, invitation, state)}
            all_invitation_data['invitations'].append(invitation_dic)
         
        all_invitation_data['tabid'] = self.__class__.__name__ + \
                                       'InvitationActions'
        body = self.content(result=all_invitation_data, 
                            template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = action_updated
        result['coordinates'] = {self.coordinates:[item]}
        result.update(resources)
        result  = merge_dicts(self.requirements_copy, result)
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeInvitations:SeeInvitationsView})
