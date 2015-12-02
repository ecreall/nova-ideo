# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_registry
from pyramid.security import remember

from substanced.util import get_oid
from substanced.event import LoggedIn

from dace.util import getSite
from dace.processinstance.activity import ActionType
from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from daceui.interfaces import IDaceUIAPI
from pontus.view import BasicView
from pontus.util import merge_dicts

from novaideo.content.processes.invitation_management.behaviors import (
    SeeInvitation)
from novaideo.content.processes import get_states_mapping
from novaideo.content.invitation import Invitation
from novaideo import _


@view_config(
    name='',
    context=Invitation,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeInvitationView(BasicView):
    title = ''
    name = ''
    behaviors = [SeeInvitation]
    template = 'novaideo:views/invitation_management/templates/see_invitation.pt'
    viewid = 'seeinvitation'


    def update(self):
        user = get_current()
        invitation = self.context
        self.execute(None)   
        dace_ui_api = get_current_registry().getUtility(
                                                IDaceUIAPI,
                                                'dace_ui_api')     
        invitation_actions = dace_ui_api.get_actions([invitation], self.request,
                                           process_or_id='invitationmanagement')
        invitation_actions = [a for a in invitation_actions \
                              if a[1].actionType != ActionType.automatic]
        action_updated, messages, \
        resources, actions = dace_ui_api.update_actions(
                                          self.request, invitation_actions)
        if hasattr(invitation, 'person'):
            person = invitation.person
            headers = remember(self.request, get_oid(person))
            self.request.registry.notify(LoggedIn(person.email, person, 
                                      invitation, self.request))
            root = getSite()
            return HTTPFound(location = self.request.resource_url(root), 
                             headers = headers)

        result = {}
        state = None
        if invitation.state:
            state = invitation.state[0]

        localizer = self.request.localizer
        values = {
                'actions':actions,
                'first_name': getattr(invitation, 'first_name',''),
                'last_name': getattr(invitation, 'last_name',''),
                'user_title': localizer.translate(_(getattr(invitation, 'user_title', ''))),
                'roles': getattr(invitation, 'roles', ''),
                'organization': getattr(invitation, 'organization', None),
                'state': get_states_mapping(user, invitation, state)
               }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = action_updated
        result['coordinates'] = {self.coordinates:[item]}
        result.update(resources)
        result  = merge_dicts(self.requirements_copy, result)
        return result

DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeInvitation:SeeInvitationView})
