from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view import BasicView
from pontus.view_operation import CallSelectedContextsViews
from pontus.schema import select

from novaideo.content.processes.invitation_management.behaviors import  SeeInvitation
from novaideo.content.invitation import Invitation


@view_config(
    name='seeinvitation',
    context=Invitation,
    renderer='pontus:templates/view.pt',
    )
class SeeInvitationView(BasicView):
    title = 'Details'
    name = 'seeinvitation'
    behaviors = [SeeInvitation]
    template = 'novaideo:views/invitation_management/templates/see_invitation.pt'
    viewid = 'seeinvitation'


    def update(self):
        self.execute(None)
        result = {}
        values = {
                'first_name': getattr(self.context, 'first_name',''),
                'last_name': getattr(self.context, 'last_name',''),
                'user_title': getattr(self.context, 'user_title', ''),
                'roles':getattr(self.context, 'roles', ''),
                'url': ''#self.request.resource_url(self.context, '@@index')
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result

DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeInvitation:SeeInvitationView})
