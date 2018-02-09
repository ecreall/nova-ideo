# -*- coding: utf-8 -*-
import graphene
from pyramid.threadlocal import get_current_request
from graphql_relay.connection.arrayconnection import cursor_to_offset
from hypatia.interfaces import STABLE

from dace.util import get_obj, find_catalog, getSite, getAllBusinessAction
from dace.objectofcollaboration.entity import ActionCall

from novaideo.views.filter import find_entities
from novaideo.content.interface import IPerson
from novaideo.views.filter import get_comments


def get_user_by_token(token):
    current_user = None
    novaideo_catalog = find_catalog('novaideo')
    dace_catalog = find_catalog('dace')
    identifier_index = novaideo_catalog['api_token']
    object_provides_index = dace_catalog['object_provides']
    query = object_provides_index.any([IPerson.__identifier__]) &\
        identifier_index.eq(token)
    users = list(query.execute().all())
    return users[0] if users else None


def get_entities(interfaces, states, args, info, user=None, intersect=None):  #pylint: disable=W0613
    try:
        after = cursor_to_offset(args.get('after'))
        first = args.get('first')
        if after is None:
            limit = first
        else:
            limit = after + 1 + first

        limit = limit + 1  # retrieve one more so the hasNextPage works
    except Exception:  # FIXME:
        limit = None

    # For the scrolling of the results, it's important that the sort is stable.
    # release_date is set to datetime.datetime.now(tz=pytz.UTC) when the event
    # is published, so we have microsecond resolution and so have a stable sort
    # even with not stable sort algorithms like nbest (because it's unlikely
    # we have several events with the same date).
    # When we specify limit in the query, the sort algorithm chosen will
    # most likely be nbest instead of stable timsort (python sorted).
    # The sort is ascending, meaning we will get new events published during
    # the scroll, it's ok.
    # The only issue we can found here is if x events are removed or unpublished
    # during the scroll, we will skip x new events during the scroll.
    # A naive solution is to implement our own graphql arrayconnection to slice
    # from the last known oid + 1, but the last known oid may not be in the
    # array anymore, so it doesn't work. It's not too bad we skip x events, in
    # reality it should rarely happen.
    rs = find_entities(
        sort_on=None,
        user=user,
        interfaces=interfaces,
        metadata_filter={'states': states},
        text_filter={'text_to_search': args.get('filter', '')},
        intersect=intersect
    )
    catalog = find_catalog('novaideo')
    release_date_index = catalog['release_date']
    return len(rs), list(release_date_index.sort(
        list(rs.ids), limit=limit, sort_type=STABLE, reverse=True))  #pylint: disable=E1101


def get_all_comments(container, args):
    try:
        after = cursor_to_offset(args.get('after'))
        first = args.get('first')
        if after is None:
            limit = first
        else:
            limit = after + 1 + first

        limit = limit + 1  # retrieve one more so the hasNextPage works
    except Exception:  # FIXME:
        limit = None

    filter_ = args.get('filter', '')
    comments = get_comments(
        container, [], filter_, filter_)
    catalog = find_catalog('novaideo')
    release_date_index = catalog['release_date']
    return list(release_date_index.sort(
        list(comments.ids), limit=limit, sort_type=STABLE, reverse=True))


def get_actions(context, request, args):
    process_id = args.get('process_id', '')
    node_ids = args.get('node_ids', '')
    if not node_ids:
        return [ActionCall(a, context) for a in getAllBusinessAction(
                context, request,
                process_id=process_id,
                process_discriminator='Application')]

    result = []
    for node_id in node_ids:
        result.extend(
            [ActionCall(a, context) for a in getAllBusinessAction(
             context, request,
             process_id=process_id, node_id=node_id,
             process_discriminator='Application')])

    return result


def get_context(oid, default=None):
    try:
        return get_obj(int(oid))
    except:
        return default or getSite()


def get_action(action_id, context, request):
    node_process = action_id.split('.')
    if len(node_process) == 2:
        process_id, node_id = node_process
        node_actions = getAllBusinessAction(
            context, request,
            process_id=process_id, node_id=node_id,
            process_discriminator='Application')
        if node_actions:
            return node_actions[0]

    return None


def get_execution_data(action_id, args):
    data = dict(args)
    context = get_context(
        data.pop('context') if 'context' in data else None)
    request = get_current_request()
    action = get_action(action_id, context, request)
    return context, request, action, data


def connection_for_type(_type):
    class Connection(graphene.Connection):
        total_count = graphene.Int()

        class Meta:
            name = _type._meta.name + 'Connection'
            node = _type

        def resolve_total_count(self, args, context, info):
            return getattr(self.iterable, 'total_count', len(self.iterable))

    return Connection