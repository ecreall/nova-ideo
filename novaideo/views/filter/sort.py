
import venusian
from hypatia.util import ResultSet
from pyramid import renderers
from pyramid.threadlocal import get_current_request

from dace.objectofcollaboration.principal.util import has_role
from dace.util import find_catalog

from novaideo import core
from novaideo import _, log


SORTS = {}


SORT_TEMPLATE = 'novaideo:views/filter/templates/sort.pt'


DEFAULT_SORT = 'release_date'


def sort_on(name, objects, reverse=False, **kwargs):
    sort = SORTS.get(name, None)
    if not sort:
        log.warning('Sort not valid')
        sort = SORTS.get(DEFAULT_SORT)

    return sort['sort'](objects, reverse, **kwargs)


def get_adapted_sort(content_types, user, intersect=None, **kwargs):
    result = []
    sorts = SORTS.items()
    if intersect:
        sorts = [s for s in sorts if s[0] in intersect]

    for (name, sort) in sorts:
        if sort['sort'].is_adapted(content_types, user, **kwargs):
            result.append((name, sort))

    result = sorted(result, key=lambda e: SORTS[e[0]]['order'])
    return result


def sort_view_objects(
    view, objects, content_types,
    user, default_sort='release_date', intersect=[],
    sort_url=None):
    current_sort = default_sort
    sort = view.params('sort')
    reverse = view.params('reverse_sort')
    reverse = reverse == 'on' if reverse else False
    adapted_sorts = get_adapted_sort(
        content_types, user, intersect=intersect, request=view.request)
    adapted_sorts_ids = [s[0] for s in adapted_sorts]
    if sort and sort in adapted_sorts_ids:
        objects = sort_on(sort, objects, reverse)
        current_sort = sort
    elif current_sort in adapted_sorts_ids:
        objects = sort_on(current_sort, objects, reverse)

    sort_body = render_adapted_sort(
        view.request, content_types, user,
        sorts=adapted_sorts,
        current_sort=current_sort,
        reverse=reverse,
        sort_url=sort_url)

    return objects, sort_body


def render_adapted_sort(
    request, content_types, user,
    template=SORT_TEMPLATE, sorts=None,
    current_sort=None, reverse=False,
    sort_url=None):
    if not sorts:
        sorts = get_adapted_sort(content_types, user, request=request)

    return renderers.render(
        template,
        {'options': sorts,
         'current': current_sort,
         'reverse': reverse,
         'sort_url': sort_url},
        request)


class sort_config(object):
    """ A function, class or method decorator which allows a
    developer to create sort registrations.
    """
    def __init__(self, name, title, order=0, description='', contents=['all'],):
        self.name = name
        self.contents = contents
        self.title = title
        self.description = description
        self.order = order

    def __call__(self, wrapped):
        def callback(context, name, ob):
            SORTS[self.name] = {
                'title': self.title,
                'description': self.description,
                'contents': self.contents,
                'order': self.order,
                'sort': ob()
            }

        venusian.attach(wrapped, callback, category='sort')
        return wrapped


def sort_by_tokens(objects, reverse=False, is_oppose=False):
    tokens_source = 'len_support'
    tokens_target = 'len_opposition'
    if is_oppose:
        tokens_source = 'len_opposition'
        tokens_target = 'len_support'

    ordered_objects = [(obj,
                        (getattr(obj, tokens_source, []) -
                         getattr(obj, tokens_target, [])))
                       for obj in objects]
    groups = {}
    for obj in ordered_objects:
        if groups.get(obj[1], None):
            groups[obj[1]].append(obj)
        else:
            groups[obj[1]] = [obj]

    for group_key in list(groups.keys()):
        sub_objects = list(groups[group_key])
        groups[group_key] = sorted(
            sub_objects,
            key=lambda obj: getattr(obj[0], tokens_source, []),
            reverse=reverse)
    groups = sorted(
        groups.items(),
        key=lambda value: value[0], reverse=reverse)
    return [obj[0] for sublist in groups
            for obj in sublist[1]]


@sort_config(
    name='nbsupport',
    title=_('Number of support tokens'),
    contents=['proposal', 'idea', 'question', 'answer'],
    order=3
)
class NumberSupport(object):
    def __call__(self, objects, reverse=False, **kwargs):
        default_reverse = not reverse
        if isinstance(objects, ResultSet):
            novaideo_catalog = kwargs.get('novaideo_catalog', None)
            if not novaideo_catalog:
                novaideo_catalog = find_catalog('novaideo')

            return objects.sort(
                novaideo_catalog['support'],
                reverse=default_reverse)

        return sort_by_tokens(objects, reverse=default_reverse)

    def is_adapted(self, content_types, user, **kwargs):
        request = kwargs.get('request', None)
        if not request:
            request = get_current_request()
        content_to_support = list(getattr(request, 'content_to_support', []))
        content_to_support.extend(list(core.SUSTAINABLE_CONTENTS.keys()))
        return ('all' in content_types and content_to_support) or\
            any(t in content_to_support for t in content_types)


@sort_config(
    name='nboppose',
    title=_('Number of opposition tokens'),
    contents=['proposal', 'idea', 'question', 'answer'],
    order=4
)
class NumberOppose(object):
    def __call__(self, objects, reverse=False, **kwargs):
        default_reverse = not reverse
        if isinstance(objects, ResultSet):
            novaideo_catalog = kwargs.get('novaideo_catalog', None)
            if not novaideo_catalog:
                novaideo_catalog = find_catalog('novaideo')

            return objects.sort(
                novaideo_catalog['oppose'],
                reverse=default_reverse)

        return sort_by_tokens(objects, reverse=default_reverse, is_oppose=True)

    def is_adapted(self, content_types, user, **kwargs):
        request = kwargs.get('request', None)
        if not request:
            request = get_current_request()

        content_to_support = list(getattr(request, 'content_to_support', []))
        content_to_support.extend(list(core.SUSTAINABLE_CONTENTS.keys()))
        return ('all' in content_types and content_to_support) or\
            any(t in content_to_support for t in content_types)


@sort_config(
    name='release_date',
    title=_('Modification date'),
    order=0
)
class ModificationDate(object):
    def __call__(self, objects, reverse=False, **kwargs):
        default_reverse = not reverse
        if isinstance(objects, ResultSet):
            novaideo_catalog = kwargs.get('novaideo_catalog', None)
            if not novaideo_catalog:
                novaideo_catalog = find_catalog('novaideo')

            return objects.sort(
                novaideo_catalog['release_date'], reverse=default_reverse)

        return sorted(
            objects,
            key=lambda e: getattr(e, 'release_date', e.modified_at),
            reverse=default_reverse)

    def is_adapted(self, content_types, user, **kwargs):
        return True


@sort_config(
    name='created_at',
    title=_('Creation date'),
    order=1
)
class CreationDate(object):
    def __call__(self, objects, reverse=False, **kwargs):
        default_reverse = not reverse
        if isinstance(objects, ResultSet):
            novaideo_catalog = kwargs.get('novaideo_catalog', None)
            if not novaideo_catalog:
                novaideo_catalog = find_catalog('novaideo')

            return objects.sort(
                novaideo_catalog['created_at'], reverse=default_reverse)

        return sorted(
            objects,
            key=lambda e: e.created_at,
            reverse=default_reverse)

    def is_adapted(self, content_types, user, **kwargs):
        return True


@sort_config(
    name='last_connection',
    description=_('Only for users'),
    title=_('Connection date'),
    order=2
)
class ConnectionDate(object):
    def __call__(self, objects, reverse=False, **kwargs):
        default_reverse = not reverse
        if isinstance(objects, ResultSet):
            novaideo_catalog = kwargs.get('novaideo_catalog', None)
            if not novaideo_catalog:
                novaideo_catalog = find_catalog('novaideo')

            return objects.sort(
                novaideo_catalog['last_connection'], reverse=default_reverse)

        return sorted(
            objects,
            key=lambda e:  getattr(e, 'last_connection', e.modified_at),
            reverse=default_reverse)

    def is_adapted(self, content_types, user, **kwargs):
        return ('all' in content_types or 'person' in content_types) and \
            has_role(user=user, role=('SiteAdmin', ))
