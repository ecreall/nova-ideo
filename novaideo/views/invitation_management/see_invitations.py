# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.activity import ActionType
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView
from pontus.util import merge_dicts
from daceui.interfaces import IDaceUIAPI

from novaideo.content.processes.invitation_management.behaviors import (
    SeeInvitations)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.content.processes import get_states_mapping
from novaideo import _
from novaideo.core import can_access 



CONTENTS_MESSAGES = {
        '0': _(u"""No invitation found"""),
        '1': _(u"""One invitation found"""),
        '*': _(u"""${nember} invitations found""")
        }

@view_config(
    name='seeinvitations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeInvitationsView(BasicView):
    title = _('Invitations')
    name = 'seeinvitations'
    behaviors = [SeeInvitations]
    template = 'novaideo:views/invitation_management/templates/see_invitations.pt'
    viewid = 'seeinvitations'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'

    def update(self):
        self.execute(None)
        user = get_current()
        result = {}
        invitations = [i for i in self.context.invitations \
                       if can_access(user, i)]
        len_result = len(invitations)
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(CONTENTS_MESSAGES[index] , 
                       mapping={'nember': len_result})
        all_invitation_data = {'invitations':[]}
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,
                                                        'dace_ui_api')
        invitations_actions = dace_ui_api.get_actions(
                            invitations, self.request,
                            process_or_id='invitationmanagement')
        invitations_actions = [a for a in invitations_actions \
                              if a[1].actionType != ActionType.automatic]
        action_updated, messages, \
        resources, actions = dace_ui_api.update_actions(self.request,
                                                            invitations_actions)
        localizer = self.request.localizer
        for invitation in invitations:
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
                'user_title': localizer.translate(_(getattr(invitation, 'user_title', ''))),
                'roles':getattr(invitation, 'roles', ''),
                'organization':getattr(invitation, 'organization', None),
                'state': get_states_mapping(user, invitation, state)}
            all_invitation_data['invitations'].append(invitation_dic)
         
        all_invitation_data['tabid'] = self.__class__.__name__ + \
                                       'InvitationActions'
        body = self.content(args=all_invitation_data, 
                            template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = action_updated
        result['coordinates'] = {self.coordinates:[item]}
        result.update(resources)
        result  = merge_dicts(self.requirements_copy, result)
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeInvitations:SeeInvitationsView})
