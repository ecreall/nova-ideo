# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember

from substanced.util import get_oid
from substanced.event import LoggedIn

from dace.objectofcollaboration.principal.util import get_current
from dace.util import getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.invitation_management.behaviors import (
    SeeInvitation)
from novaideo.content.invitation import Invitation
from novaideo.utilities.util import (
    generate_listing_menu,
    ObjectRemovedException,
    DEFAUL_LISTING_ACTIONS_TEMPLATE)
from novaideo.content.processes import get_states_mapping


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
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'

    def update(self):
        self.execute(None)
        try:
            navbars = generate_listing_menu(
                self.request, self.context,
                template=DEFAUL_LISTING_ACTIONS_TEMPLATE)
        except ObjectRemovedException:
            #Log in if the invitation is accepted
            if hasattr(self.context, 'person'):
                person = self.context.person
                headers = remember(self.request, get_oid(person))
                self.request.registry.notify(
                    LoggedIn(person.email, person,
                             self.context, self.request))
                root = getSite()
                return HTTPFound(
                    location=self.request.resource_url(root),
                    headers=headers)

            return HTTPFound(self.request.resource_url(getSite(), ''))

        user = get_current()
        values = {
            'invitation': self.context,
            'menu_body': navbars['menu_body'],
            'state': get_states_mapping(
                user, self.context, self.context.state[0]),}
        result = {}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = navbars['messages']
        item['isactive'] = navbars['isactive']
        result.update(navbars['resources'])
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeInvitation: SeeInvitationView})
