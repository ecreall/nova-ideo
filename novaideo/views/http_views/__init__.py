# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPInternalServerError


@view_config(context=HTTPNotFound, 
	         renderer='novaideo:views/http_views/templates/404.pt')
def not_found(self, request):
    request.response.status = 404
    return {'request': request}


@view_config(context=HTTPInternalServerError, 
	         renderer='novaideo:views/http_views/templates/500.pt')
def internal_server_error(self, request):
    request.response.status = 500
    return {'request': request}
