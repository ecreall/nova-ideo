# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
# TODO: finish to clean, use our own templates, ... ?

import datetime
import pytz
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound
    )
from pyramid.renderers import get_renderer
from pyramid.session import check_csrf_token
from pyramid.security import remember

from substanced.util import get_oid
from substanced.event import LoggedIn

from dace.util import find_catalog
from dace.objectofcollaboration.principal.util import has_role
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView, ViewError

from novaideo.content.interface import IPerson
from novaideo import _
from novaideo.content.processes.user_management.behaviors import LogIn
from novaideo.content.novaideo_application import NovaIdeoApplication


@view_config(
    name='login',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class LoginView(BasicView):
    title = _('Log in')
    name = 'login'
    behaviors = [LogIn]
    template = 'novaideo:views/user_management/templates/login.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    viewid = 'login'

    def update(self):
        request = self.request
        context = self.context
        login_url = request.resource_url(request.context, 'login')
        login_url2 = request.resource_url(request.context, '@@login')
        referrer = self.params('came_from')
        if not referrer:
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
                login = request.params['email'].strip()
                password = request.params['password']
                novaideo_catalog = find_catalog('novaideo')
                dace_catalog = find_catalog('dace')
                identifier_index = novaideo_catalog['identifier']
                object_provides_index = dace_catalog['object_provides']
                query = object_provides_index.any([IPerson.__identifier__]) &\
                        identifier_index.any([login])
                users = list(query.execute().all())
                user = users[0] if users else None
                valid_check = user and user.check_password(password)
                if valid_check and \
                   (has_role(user=user, role=('SiteAdmin', )) or \
                   'active' in getattr(user, 'state', [])):
                    request.session.pop('novaideo.came_from', None)
                    headers = remember(request, get_oid(user))
                    request.registry.notify(LoggedIn(login, user,
                                               context, request))
                    user.last_connection = datetime.datetime.now(tz=pytz.UTC)
                    if hasattr(user, 'reindex'):
                        user.reindex()

                    return HTTPFound(location=came_from, headers=headers)
                elif valid_check and 'deactivated' in getattr(user, 'state', []):
                    error = ViewError()
                    error.principalmessage = _("Disabled account! Contact the site administrator to activate your account.")
                    message = error.render_message(request)
                    messages.update({error.type: [message]})
                else:
                    error = ViewError()
                    error.principalmessage = _("Failed login")
                    message = error.render_message(request)
                    messages.update({error.type: [message]})

        # Pass this through FBO views (e.g., forbidden) which use its macros.
        template = get_renderer('novaideo:views/user_management/templates/login.pt').implementation()
        values = dict(
            url=request.resource_url(request.virtual_root, 'login'),
            came_from=came_from,
            login=login,
            password=password,
            login_template=template,
            )
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        result = {}
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {LogIn: LoginView})
