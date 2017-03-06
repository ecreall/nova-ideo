# Copyright (c) 2017 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.threadlocal import get_current_request
from pyramid.traversal import ResourceTreeTraverser

from dace.util import get_obj


def get_request(client):
    request = get_current_request()
    cookie = client.http_headers.get('cookie', None)
    if cookie:
        request.environ['AUTH_TYPE'] = 'cookie'
        request.environ['HTTP_COOKIE'] = cookie

    resources = ResourceTreeTraverser(request.root)(request)
    request.context = resources.get('context', None)
    return request


def get_user(request):
    authenticated_userid = request.authenticated_userid
    if authenticated_userid:
        return get_obj(authenticated_userid)

    return None
