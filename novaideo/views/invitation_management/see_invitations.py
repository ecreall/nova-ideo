
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
        all_messages = {}
        isactive = False
        all_resources = {}
        all_resources['js_links'] = []
        all_resources['css_links'] = []
        all_invitation_data = {'invitations':[]}
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,
                                                        'dace_ui_api')
        for invitation in self.context.invitations:
            action_updated, messages, resources, actions = dace_ui_api._actions(self.request, invitation)
            if action_updated and not isactive:
                isactive = True

            all_messages.update(messages)
            if resources is not None:
                if 'js_links' in resources:
                    all_resources['js_links'].extend(resources['js_links'])
                    all_resources['js_links'] = list(set(all_resources['js_links']))

                if 'css_links' in resources:
                    all_resources['css_links'].extend(resources['css_links'])
                    all_resources['css_links'] =list(set(all_resources['css_links']))

            state = None
            if invitation.state:
                state = invitation.state[0]

            invitation_dic = { 
                'actions': actions,
                'url':self.request.resource_url(invitation, '@@index'), 
                'first_name': getattr(invitation, 'first_name',''),
                'last_name': getattr(invitation, 'last_name', ''),
                'user_title': getattr(invitation, 'user_title', ''),
                'roles':getattr(invitation, 'roles', ''),
                'organization':getattr(invitation, 'organization', None),
                'state': get_states_mapping(user, invitation, state)}
            all_invitation_data['invitations'].append(invitation_dic)
         
        all_invitation_data['tabid'] = self.__class__.__name__ + 'InvitationActions'
        body = self.content(result=all_invitation_data, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = all_messages
        item['isactive'] = isactive
        result['coordinates'] = {self.coordinates:[item]}
        result.update(all_resources)
        result  = merge_dicts(self.requirements_copy, result)
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeInvitations:SeeInvitationsView})
