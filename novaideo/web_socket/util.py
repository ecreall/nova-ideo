# Copyright (c) 2017 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.threadlocal import get_current_request
from pyramid.traversal import ResourceTreeTraverser

from dace.util import get_obj

from novaideo import (
    ajax_api,
    get_time_zone,
    moderate_ideas,
    moderate_proposals,
    examine_ideas,
    examine_proposals,
    support_ideas,
    support_proposals,
    content_to_examine,
    content_to_support,
    is_idea_box,
    accessible_to_anonymous,
    searchable_contents,
    analytics_default_content_types,
    )
from novaideo.layout import GlobalLayout


def add_request_method(callable, request):
    name = callable.__name__
    setattr(request, name, callable(request))


def get_request(client):
    request = get_current_request()
    cookie = client.http_headers.get('cookie', None)
    host = client.http_headers.get('host', None)
    if cookie:
        request.environ['AUTH_TYPE'] = 'cookie'
        request.environ['HTTP_COOKIE'] = cookie

    request.environ['HTTP_HOST'] = host
    request.environ['SERVER_NAME'] = client.http_request_host
    resources = ResourceTreeTraverser(request.root)(request)
    request.context = resources.get('context', None)
    request.layout = GlobalLayout(request.context, request)
    add_request_method(ajax_api, request)
    add_request_method(get_time_zone, request)
    add_request_method(moderate_ideas, request)
    add_request_method(moderate_proposals, request)
    add_request_method(examine_ideas, request)
    add_request_method(examine_proposals, request)
    add_request_method(support_ideas, request)
    add_request_method(support_proposals, request)
    add_request_method(content_to_examine, request)
    add_request_method(content_to_support, request)
    add_request_method(is_idea_box, request)
    add_request_method(accessible_to_anonymous, request)
    add_request_method(searchable_contents, request)
    add_request_method(analytics_default_content_types, request)
    return request


def get_user(request):
    authenticated_userid = request.authenticated_userid
    if authenticated_userid:
        return get_obj(authenticated_userid)

    return None
