# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
# TODO: finish to clean, use our own templates, ... ?

from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound
    )
from pyramid.renderers import get_renderer
from pyramid.session import check_csrf_token
from pyramid.security import remember

from substanced.util import get_oid

from substanced.interfaces import IUserLocator
from substanced.principal import DefaultUserLocator
from substanced.event import LoggedIn

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView, ViewError

from novaideo import _
from novaideo.content.processes.user_access_manager.behaviors import  LogIn
from novaideo.content.novaideo_application import NovaIdeoApplication


@view_config(
    name='login',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class LoginView(BasicView):
    title = _('Log in')
    name = 'login'
    behaviors = [LogIn]
    template = 'novaideo:views/user_access_manager/templates/login.pt'
    item_template = 'pontus:templates/subview_sample.pt'
    viewid = 'login'


    def update(self):
        request = self.request
        context = self.context
        login_url = request.resource_url(request.context, 'login')
        login_url2 = request.resource_url(request.context, '@@login')
        referrer = request.path_url
        if '/auditstream-sse' in referrer:
            # If we're being invoked as the result of a failed request to the
            # auditstream sse view, bail.  Otherwise the came_from will be set to
            # the auditstream URL, and the user who this happens to will eventually
            # be redirected to it and they'll be left scratching their head when
            # they see e.g. "id: 0-10\ndata: " when they log in successfully.
            return HTTPForbidden()

        if login_url in referrer or login_url2 in referrer:
            # never use the login form itself as came_from
            referrer = request.resource_url(request.virtual_root)
        came_from = request.session.setdefault('novaideo.came_from', referrer)
        login = ''
        password = ''
        message = None
        messages = {}
        if 'form.submitted' in request.params:

            try:
                check_csrf_token(request)
            except:
                request.sdiapi.flash(_('Failed login (CSRF)'), 'danger')
            else:
                self.execute(None)
                login = request.params['email']
                password = request.params['password']
                adapter = request.registry.queryMultiAdapter(
                    (context, request),
                    IUserLocator
                    )
                if adapter is None:
                    adapter = DefaultUserLocator(context, request)
                user = adapter.get_user_by_email(login)
                if user is not None and user.check_password(password):
                    request.session.pop('novaideo.came_from', None)
                    headers = remember(request, get_oid(user))
                    request.registry.notify(LoggedIn(login, user, 
                                               context, request))
                    return HTTPFound(location = came_from, headers = headers)
                error = ViewError()
                error.principalmessage = u"Failed login"
                message = self._get_message(error)
                messages.update({error.type: [message]})

        # Pass this through FBO views (e.g., forbidden) which use its macros.
        template = get_renderer('novaideo:views/user_access_manager/templates/login.pt').implementation()
        values = dict(
            url = request.resource_url(request.virtual_root, 'login'),
            came_from = came_from,
            login = login,
            password = password,
            login_template = template,
            )
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        result = {}
        result['coordinates'] = {self.coordinates:[item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({LogIn:LoginView})
