# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPInternalServerError

from pontus.view import BasicView

from novaideo import _


@view_config(
    context=HTTPNotFound,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class NotFoundView(BasicView):
    title = _('Document not found!')
    name = 'notfound'
    template = 'novaideo:views/http_views/templates/404.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'
    wrapper_template = 'novaideo:views/http_views/templates/simple_wrapper.pt'

    def update(self):
        self.title = self.request.localizer.translate(self.title)
        result = {}
        body = self.content(args={}, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        self.request.response.status = 404
        return result


@view_config(
    context=HTTPInternalServerError,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class InternalServerError(BasicView):
    title = _('An error has occurred!')
    name = 'internalservererror'
    template = 'novaideo:views/http_views/templates/500.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'
    wrapper_template = 'novaideo:views/http_views/templates/simple_wrapper.pt'

    def update(self):
        self.title = self.request.localizer.translate(self.title)
        result = {}
        body = self.content(args={}, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        self.request.response.status = 500
        return result
