
# -*- coding: utf8 -*-
# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi


from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from pontus.view import BasicView

from novaideo import _
from novaideo.connectors.core.content import (
    validate_user)


@view_config(
    context='velruse.AuthenticationComplete',
    renderer='pontus:templates/views_templates/grid.pt',
    )
class LoginCompleteView(BasicView):
    title = _('Login complete')
    template = 'novaideo:connectors/core/views/templates/result.pt'
    wrapper_template = 'daceui:templates/simple_view_wrapper.pt'
    viewid = 'login_complete'

    def update(self):
        app_name = self.context.provider_name
        root = self.request.sdiapi.get_connection(
            self.request).root().get('app_root')
        connectors = list(root.get_connectors(app_name))
        app_connector = connectors[0] if connectors else None
        if app_connector:
            source_data, user_data = app_connector.extract_data(self.context)
            values = {
                'user_data': user_data,
                'source_data': source_data
            }
            self.request.root = root
            self.request.virtual_root = root
            self.request.context = root
            self.context = root
            person, valid, headers = validate_user(self.context, self.request, values)
            if person and valid and headers:
                return HTTPFound(location=self.request.resource_url(self.context),
                                 headers=headers)

        return HTTPFound(self.request.resource_url(root, '@@login'))


@view_config(
    context='velruse.AuthenticationDenied',
    renderer='pontus:templates/views_templates/grid.pt',
    )
class LoginDeniedView(BasicView):
    title = _('Login denied')
    name = 'login_denied'
    template = 'novaideo:connectors/core/views/templates/result.pt'
    wrapper_template = 'daceui:templates/simple_view_wrapper.pt'
    viewid = 'login_denied'

    def update(self):
        self.request.root = self.request.sdiapi.get_connection(
            self.request).root().get('app_root')
        self.request.virtual_root = self.request.root
        self.request.context = self.request.root
        self.context = self.request.root
        values = {
            'result': 'denied',
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result = {}
        result['coordinates'] = {self.coordinates: [item]}
        return result
