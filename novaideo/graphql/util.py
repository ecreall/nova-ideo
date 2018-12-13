# -*- coding: utf-8 -*-
import graphene
import json
import urllib
from pyramid.threadlocal import get_current_request
from graphql_relay.connection.arrayconnection import cursor_to_offset
from hypatia.interfaces import STABLE
from substanced.objectmap import find_objectmap

from dace.util import get_obj, find_catalog, getSite, getAllBusinessAction
from dace.objectofcollaboration.entity import ActionCall

from novaideo.views.filter import find_entities
from novaideo.content.interface import IPerson
from novaideo.views.filter import get_comments


class ResolverLazyList(object):

    def __init__(self, origin, object_type, state=None, total_count=None):
        self._origin = origin
        self._state = state or []
        self._origin_iter = None
        self._total_count = total_count
        self._finished = False
        objectmap = find_objectmap(get_current_request().root)
        self.resolver = objectmap.object_for
        self.object_type = object_type

    def __iter__(self):
        return self if not self._finished else iter(self._state)

    def iter(self):
        return self.__iter__()

    def __len__(self):
        return self._origin.__len__()

    def __next__(self):
        try:
            if not self._origin_iter:
                self._origin_iter = self._origin.__iter__()
            # n = next(self._origin_iter)
            oid = next(self._origin_iter)
            n = self.resolver(oid)
        except StopIteration as e:
            self._finished = True
            raise e
        else:
            self._state.append(n)
            return n

    def next(self):
        return self.__next__()

    def __getitem__(self, key):
        item = self._origin[key]
        if isinstance(key, slice):
            return self.__class__(item, object_type=self.object_type)

        return item

    def __getattr__(self, name):
        return getattr(self._origin, name)

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, repr(self._origin))

    @property
    def total_count(self):
        return self._total_count


def get_user_by_token(token):
    novaideo_catalog = find_catalog('novaideo')
    dace_catalog = find_catalog('dace')
    identifier_index = novaideo_catalog['api_token']
    object_provides_index = dace_catalog['object_provides']
    query = object_provides_index.any([IPerson.__identifier__]) &\
        identifier_index.eq(token)
    users = list(query.execute().all())
    return users[0] if users else None


def get_entities(
    interfaces, states, args, info, user=None,
    intersect=None, defined_search=False, generate_text_search=False):  #pylint: disable=W0613
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
    filter = args.get('filter', {'text': '', 'keywords': []})
    rs = find_entities(
        sort_on=None,
        user=user,
        interfaces=interfaces,
        metadata_filter={'states': states, 'keywords': filter.get('keywords', [])},
        text_filter={'text_to_search': filter.get('text', '')},
        intersect=intersect,
        defined_search=defined_search,
        generate_text_search=generate_text_search
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

    filter_ = args.get('filter', {'text': ''})
    text_to_search = filter_.get('text', '')
    pinned = args.get('pinned', False)
    file = args.get('file', False)
    filters = []
    if pinned: filters.append('pinned')

    if file: filters.append('file')

    comments = get_comments(
        container, filters, text_to_search, text_to_search or pinned or file)
    catalog = find_catalog('novaideo')
    release_date_index = catalog['release_date']

    return len(comments), list(release_date_index.sort(
        list(comments.ids), limit=limit, sort_type=STABLE, reverse=True))


def get_actions(context, request, args):
    process_ids = args.get('process_id', None)
    node_ids = args.get('node_ids', None)
    action_tags = args.get('action_tags', None)
    process_tags = args.get('process_tags', None)
    if not node_ids:
        return [ActionCall(a, context) for a in getAllBusinessAction(
                context, request,
                process_id=process_ids,
                process_discriminator='Application',
                action_tags=action_tags,
                process_tags=process_tags)]

    result = []
    for node_id in node_ids:
        result.extend(
            [ActionCall(a, context) for a in getAllBusinessAction(
             context, request,
             process_id=process_ids, node_id=node_id,
             process_discriminator='Application',
             action_tags=action_tags,
             process_tags=process_tags)])

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


def extract_files(key, request):
    """
    the Upload object type deserialization currently doesn't work,
    it fails silently, so we actually get a list of None.
    So if we uploaded 3 files, we get files = [None, None, None]
    We retrieve the files with the hard coded
    variables.attachedFiles.{0,1,2} below.
    This code will not work if batched mode is
    implemented in graphql-wsgi and batched mode is enabled on apollo.
    """
    results = []
    if request.POST:
        key_items = key.split('_')
        if len(key_items) == 1:
            cc_key = key
        else:
            cc_key = key_items[0]+"".join([e.capitalize() for e in key_items[1:]])

        files_map = request.POST.get('map')
        if files_map:
            map_values = list(json.loads(files_map).items())
            file_id = "variables.{key}.".format(key=cc_key)
            files_keys = [(index, file_key) for index, files in map_values for file_key in files]
            files_keys = [(index, f) for index, f in files_keys if f.startswith(file_id)]
            file_storages = [request.POST.get(index) for index, fk in files_keys]
            for file_storage in file_storages:
                fp = file_storage.file
                fp.seek(0)
                results.append({
                    'fp': fp,
                    'filename': urllib.parse.unquote(file_storage.filename)})

    return results
