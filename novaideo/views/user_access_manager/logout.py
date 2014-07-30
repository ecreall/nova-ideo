from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget

from substanced.interfaces import IUserLocator
from substanced.principal import DefaultUserLocator
from substanced.event import LoggedIn

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView, ViewError

from novaideo.content.processes.user_access_manager.behaviors import  LogOut
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _



@view_config(
    name='logout',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class LogoutView(BasicView):
    title = _('Log out')
    name = 'logout'
    behaviors = [LogOut]
    viewid = 'logout'

    def update(self):
        self.execute(None)
        headers = forget(self.request)
        return HTTPFound(location = self.request.resource_url(self.request.context, '@@index'),
                     headers = headers)


DEFAULTMAPPING_ACTIONS_VIEWS.update({LogOut:LogoutView})
