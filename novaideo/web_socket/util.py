# Copyright (c) 2017 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.threadlocal import get_current_request, get_current_registry
from pyramid.traversal import ResourceTreeTraverser, find_resource
from pyramid.i18n import make_localizer
from pyramid.interfaces import ITranslationDirectories


from twisted.internet import reactor

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
    content_to_manage,
    accessible_to_anonymous,
    searchable_contents,
    analytics_default_content_types,
    )
from novaideo.layout import GlobalLayout

  
def get_localizer_for_locale_name(locale_name):
    registry = get_current_registry()
    tdirs = registry.queryUtility(ITranslationDirectories, default=[])
    return make_localizer(locale_name, tdirs)


def add_request_method(callable, request):
    name = callable.__name__
    setattr(request, name, callable(request))


def get_request(client, **kwargs):
    request = get_current_request()
    cookie = client.http_headers.get('cookie', None)
    host = client.http_headers.get('host', None)
    if cookie:
        request.environ['AUTH_TYPE'] = 'cookie'
        request.environ['HTTP_COOKIE'] = cookie

    request.environ['HTTP_HOST'] = host
    request.environ['SERVER_NAME'] = client.http_request_host
    url = client.http_headers.get('origin')
    view_name = ''
    source_path = kwargs.get('source', {}).get('source_path', None)
    if not source_path:
        source_path = client.http_request_params.get('source_path', None)
        source_path = source_path[0] if source_path else None

    resources = ResourceTreeTraverser(request.root)(request)
    if source_path:
        url += source_path
        try:
            source_path_parts = source_path.split('/')
            view_name = source_path_parts[-1]
            source_path = '/'.join(source_path_parts[:-1])
            context = find_resource(request.root, source_path)
        except Exception:
            context = resources.get('context', None)
    else:
        context = resources.get('context', None)

    request.context_url = url
    request.view_name = view_name
    request.context = context
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
    add_request_method(content_to_manage, request)
    add_request_method(accessible_to_anonymous, request)
    add_request_method(searchable_contents, request)
    add_request_method(analytics_default_content_types, request)
    request.user = get_user(request)
    return request


def get_user(request):
    authenticated_userid = request.authenticated_userid
    if authenticated_userid:
        return get_obj(authenticated_userid)

    return None


def get_ws_factory():
    return reactor.ws_factory


def get_connected_users():
    return reactor.ws_factory.users
