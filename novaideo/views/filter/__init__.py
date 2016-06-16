# -*- coding: utf8 -*-
# Copyright (c) 2015 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import re
import colander
import datetime
import pytz
import types
import json
from hypatia.text.parsetree import ParseError
from hypatia.util import ResultSet
from hypatia.query import Not
from pyramid.view import view_config
from pyramid import renderers
from pyramid.threadlocal import (
    get_current_registry, get_current_request)

from substanced.util import get_oid

from dace.objectofcollaboration.principal.util import Anonymous
from dace.util import getSite, find_catalog, get_obj
from dace.objectofcollaboration.principal.util import (
    get_current, has_any_roles)
from pontus.widget import (
    Select2Widget, AjaxSelect2Widget, SimpleMappingWidget)
from pontus.schema import Schema, omit, select
from pontus.form import FormView

from novaideo import _
from novaideo import core
from novaideo.content.processes import (
    FLATTENED_STATES_MEMBER_MAPPING,
    get_content_types_states)
from novaideo.utilities.util import (
    normalize_title, combinaisons)
from novaideo.views.filter.util import (
    match_in, get_zipcodes, get_zipcodes_from_cities,
    deepcopy, get_node_query,
    get_filters_query, QUERY_OPERATORS, get_analyzed_data,
    merge_with_filter_view)
from novaideo.views.widget import SimpleMappingtWidget
from novaideo import log


#If updated: See data_manager utility FILTER_DEFAULT_DATA


FILTER_SOURCES = {}


INDEX_MAPPING = {
    ('publication', 'day'): 'published_at_str',
    ('publication', 'month'): 'published_at_month_str',
    ('publication', 'year'): 'published_at_year_str',
    ('examination', 'day'): 'examined_at_str',
    ('examination', 'month'): 'examined_at_month_str',
    ('examination', 'year'): 'examined_at_year_str',

}


FILTER_TEMPLATES = {
    'geographic_filter': {
        'default': 'novaideo:views/filter/templates/geographic_filter.pt',
        'extraction': 'novaideo:views/filter/templates/extraction/geographic_filter.pt'
    },
    'metadata_filter': {
        'default': 'novaideo:views/filter/templates/metadata_filter.pt',
        'extraction': 'novaideo:views/filter/templates/extraction/metadata_filter.pt'
    },
    'contribution_filter': {
        'default': 'novaideo:views/filter/templates/contribution_filter.pt',
        'extraction': 'novaideo:views/filter/templates/extraction/contribution_filter.pt'
    },
    'text_filter': {
        'default': 'novaideo:views/filter/templates/text_filter.pt',
        'extraction': 'novaideo:views/filter/templates/extraction/text_filter.pt'
    },
    'temporal_filter': {
        'default': 'novaideo:views/filter/templates/temporal_filter.pt',
        'extraction': 'novaideo:views/filter/templates/extraction/temporal_filter.pt'
    },
    'other_filter': {
        'default': 'novaideo:views/filter/templates/other_filter.pt',
        'extraction': 'novaideo:views/filter/templates/extraction/other_filter.pt'
    },
    'filter': {
        'default': 'novaideo:views/filter/templates/filter_template.pt',
        'extraction': 'novaideo:views/filter/templates/extraction/filter_template.pt'
    },
    'global': {
        'default': 'novaideo:views/filter/templates/global.pt',
        'extraction': 'novaideo:views/filter/templates/extraction/global.pt'
    }
}


_marker = object()


#**********************************************Filter queries getters


def content_types_query(node, **args):
    value = None
    if 'metadata_filter' in args:
        value = args['metadata_filter']

    content_types = value.get('content_types', []) if value else []
    request = args.get('request', None)
    if not request:
        request = get_current_request()

    searchable_contents = dict(core.get_searchable_content(request))
    if not content_types:
        content_types = list(searchable_contents.keys())

    if args.get('interfaces', []):
        interfaces = [i.__identifier__ for i in args['interfaces']]
    else:
        interfaces = [list(searchable_contents[i].
                     __implemented__.interfaces())[0].__identifier__
                      for i in content_types if i in searchable_contents]
    #catalog
    dace_catalog = None
    if 'dace' in args:
        dace_catalog = args['dace']
    else:
        dace_catalog = find_catalog('dace')

    #index
    object_provides_index = dace_catalog['object_provides']
    return object_provides_index.any(interfaces)


def states_query(node, **args):
    value = None
    if 'metadata_filter' in args:
        value = args['metadata_filter']

    #catalog
    states = value.get('states', []) if value else []
    dace_catalog = None
    if 'dace' in args:
        dace_catalog = args['dace']
    else:
        dace_catalog = find_catalog('dace')

    #index
    states_index = dace_catalog['object_states']
    if not states:
        return states_index.notany(['version']) if \
            args.get('include_archived', False) \
            else states_index.notany(['archived', 'version'])

    if args.get('all_states', False):
        return states_index.notany(['version']) & states_index.all(states)

    return states_index.notany(['version']) & states_index.any(states)


def keywords_query(node, **args):
    value = None
    if 'metadata_filter' in args:
        value = args['metadata_filter']

    keywords = value.get('keywords', None) if value else []
    if not keywords:
        return None

    keywords = set(keywords)
    keywords = [k.lower() for k in keywords]
    novaideo_catalog = None
    if 'novaideo' in args:
        novaideo_catalog = args['novaideo']
    else:
        novaideo_catalog = find_catalog('novaideo')

    #index
    keywords_index = novaideo_catalog['object_keywords']
    #query
    return keywords_index.any(keywords)


def text_to_search_query(node, **args):
    value = None
    if 'text_filter' in args:
        value = args['text_filter']

    if value is None:
        return None

    text = value.get('text_to_search', None)
    if text:
        if args.get('defined_search', False):
            text = text.replace('(', '').replace(')', '').lower()
            list_text = [t + '*' for t in re.split(', *', text)]
            if not args.get('generate_text_search', False):
                operator = args.get('text_operator', 'AND')
                text = (' ' + operator + ' ').join(list_text)
            else:
                percentage = args.get('percentage', 80)
                text_nb = int((len(list_text) * percentage) / 100)
                result = combinaisons(list_text, text_nb, 1)
                text = ' OR '.join(['('+' AND '.join(
                                   [a+'*' for a in key.split('*') if a]) + ')'
                                     for key in result])
        else:
            text += '*'

    else:
        return None

    novaideo_catalog = None
    if 'novaideo' in args:
        novaideo_catalog = args['novaideo']
    else:
        novaideo_catalog = find_catalog('novaideo')

    relevant_data_index = novaideo_catalog['relevant_data']
    query = None
    if text:
        query = relevant_data_index.contains(text)

    return query


def created_date_query(node, **args):
    value = None
    if 'temporal_filter' in args:
        value = args['temporal_filter']

    if value is None:
        return None

    created_date = value.get('created_date', None)
    if not created_date:
        return None

    novaideo_catalog = None
    if 'novaideo' in args:
        novaideo_catalog = args['novaideo']
    else:
        novaideo_catalog = find_catalog('novaideo')

    #index
    created_after = created_date['created_after']
    created_before = created_date['created_before']
    created_at_index = novaideo_catalog['created_at']
    query = None
    if created_after:
        created_after = datetime.datetime.combine(
            created_after,
            datetime.datetime.min.time()).replace(tzinfo=pytz.UTC)
        query = created_at_index.gt(created_after)

    if created_before:
        created_before = datetime.datetime.combine(
            created_before,
            datetime.datetime.min.time()).replace(tzinfo=pytz.UTC)
        if query is None:
            query = created_at_index.lt(created_before)
        else:
            query = query & created_at_index.lt(created_before)

    return query


def connected_date_query(node, **args):
    value = None
    if 'temporal_filter' in args:
        value = args['temporal_filter']

    if value is None:
        return None

    connected_date = value.get('connected_date', None)
    if not connected_date:
        return None

    novaideo_catalog = None
    if 'novaideo' in args:
        novaideo_catalog = args['novaideo']
    else:
        novaideo_catalog = find_catalog('novaideo')

    #index
    connected_after = connected_date['connected_after']
    connected_before = connected_date['connected_before']
    connected_at_index = novaideo_catalog['last_connection']
    query = None
    if connected_after:
        connected_after = datetime.datetime.combine(
            connected_after,
            datetime.datetime.min.time())
        connected_after = connected_after.replace(tzinfo=pytz.UTC)
        query = connected_at_index.gt(connected_after)

    if connected_before:
        connected_before = datetime.datetime.combine(
            connected_before,
            datetime.datetime.min.time())
        connected_before = connected_before.replace(tzinfo=pytz.UTC)
        if query is None:
            query = connected_at_index.lt(connected_before)
        else:
            query = query & connected_at_index.lt(connected_before)

    return query


def authors_query(node, **args):
    value = None
    if 'contribution_filter' in args:
        value = args['contribution_filter']

    if value is None:
        return None

    authors = value.get('authors', [])
    if not authors:
        return None

    novaideo_catalog = None
    if 'novaideo' in args:
        novaideo_catalog = args['novaideo']
    else:
        novaideo_catalog = find_catalog('novaideo')

    #index
    authors_index = novaideo_catalog['object_authors']
    return authors_index.any([get_oid(v) for v in authors])


def contribution_filter_query(node, **args):
    filter_ = args.get('contribution_filter', {})
    if filter_.get('negation', False):
        query = get_node_query(node, **args)
        return query if not query else Not(query)

    return get_node_query(node, **args)


def geographic_filter_query(node, **args):
    filter_ = args.get('geographic_filter', {})
    if filter_.get('negation', False):
        return Not(get_node_query(node, **args))

    return get_node_query(node, **args)


def metadata_filter_query(node, **args):
    filter_ = args.get('metadata_filter', {})
    if filter_.get('negation', False):
        query = get_node_query(node, **args)
        return query if not query else Not(query)

    return get_node_query(node, **args)


def temporal_filter_query(node, **args):
    filter_ = args.get('temporal_filter', {})
    if filter_.get('negation', False):
        query = get_node_query(node, **args)
        return query if not query else Not(query)

    return get_node_query(node, **args)


def text_filter_query(node, **args):
    filter_ = args.get('text_filter', {})
    if filter_.get('negation', False):
        query = get_node_query(node, **args)
        return query if not query else Not(query)

    return get_node_query(node, **args)


def other_filter_query(node, **args):
    filter_ = args.get('other_filter', {})
    if filter_.get('negation', False):
        query = get_node_query(node, **args)
        return query if not query else Not(query)

    return get_node_query(node, **args)


#********************************************Filter data analyzer


def content_types_analyzer(node, source, validated, validated_value):
    """Return for example
    {'artist': 8610, 'person': 3, 'cinema_review': 769, 'venue': 729,
     'cultural_event': 2487, 'organization': 1, 'review': 4187}
    only includes content type != 0
    """
    if 'metadata_filter' in validated:
        validated['metadata_filter'].pop('content_types', None)

    objects = source(**validated)
    index = find_catalog('system')['content_type']
    intersection = index.family.IF.intersection
    object_ids = getattr(objects, 'ids', objects)
    if isinstance(object_ids, (list, types.GeneratorType)):
        object_ids = index.family.IF.Set(object_ids)

    result = [(content_type, len(intersection(oids, object_ids)))
              for content_type, oids in index._fwd_index.items()]
    result = dict([(k, v) for k, v in result if v != 0])
    return {'content_types': result}


def states_analyzer(node, source, validated, validated_value):
    """Return for example
    {'editable': 250, 'published': 16264, 'archived': 269, 'active': 3}
    """
    if 'metadata_filter' in validated:
        validated['metadata_filter'].pop('states', None)

    objects = source(**validated)
    index = find_catalog('dace')['object_states']
    intersection = index.family.IF.intersection
    object_ids = getattr(objects, 'ids', objects)
    if isinstance(object_ids, (list, types.GeneratorType)):
        object_ids = index.family.IF.Set(object_ids)

    result = [(state_id, len(intersection(oids, object_ids)))
              for state_id, oids in index._fwd_index.items()]
    result = dict([(k, v) for k, v in result
                   if v != 0 and k in FLATTENED_STATES_MEMBER_MAPPING])
    return {'states': result}


def authors_analyzer(node, source, validated, validated_value):
    """Return for example
    dict([('7422658066368290778', 1))])
    7422658066368290778 is the oid of the Person object
    """
    validated_value_ = []
    if 'contribution_filter' in validated:
        validated_value_ = validated['contribution_filter'].pop(
            'authors', [])

    objects = source(**validated)

    index = find_catalog('novaideo')['object_authors']
    intersection = index.family.IF.intersection
    object_ids = getattr(objects, 'ids', objects)
    if isinstance(object_ids, (list, types.GeneratorType)):
        object_ids = index.family.IF.Set(object_ids)

    result = {}
    for author in validated_value_:
        author_oid = get_oid(author)
        oids = index._fwd_index.get(author_oid)
        if oids:
            count = len(intersection(oids, object_ids))
        else:
            count = 0

        result[str(author_oid)] = count

    return {'authors': result}


def contribution_filter_analyzer(node, source, validated, validated_value):
    return get_analyzed_data(
        node, source, validated)


def geographic_filter_analyzer(node, source, validated, validated_value):
    return get_analyzed_data(
        node, source, validated)


def metadata_filter_analyzer(node, source, validated, validated_value):
    return get_analyzed_data(
        node, source, validated)


def temporal_filter_analyzer(node, source, validated, validated_value):
    return get_analyzed_data(
        node, source, validated)


def text_filter_analyzer(node, source, validated, validated_value):
    return get_analyzed_data(
        node, source, validated)


def other_filter_analyzer(node, source, validated, validated_value):
    return get_analyzed_data(
        node, source, validated)


#**************************************Filter repr


def default_repr(value, request, template):
    if template:
        return renderers.render(
            template,
            {'value': value},
            request)

    return str(value)


def metadata_filter_repr(value, request, template_type='default'):
    template = FILTER_TEMPLATES['metadata_filter'].get(template_type, None)
    value_cp = deepcopy(value)
    content_types = value_cp['content_types']
    searchable_contents = dict(core.get_searchable_content())
    content_types = [getattr(searchable_contents[c], 'type_title', c)
                     for c in content_types if c in searchable_contents]
    value_cp['content_types'] = content_types
    tree = value_cp['tree']
    tree = json.dumps(dict(tree))
    value_cp['tree'] = tree
    states = value_cp['states']
    localizer = request.localizer
    states = [', '.join([localizer.translate(st)
                         for st in FLATTENED_STATES_MEMBER_MAPPING[s]])
              for s in states
              if s in FLATTENED_STATES_MEMBER_MAPPING]
    value_cp['states'] = states
    value_cp['title'] = _('Metadata filter')
    return default_repr(value_cp, request, template)


def geographic_filter_repr(value, request, template_type='default'):
    template = FILTER_TEMPLATES['geographic_filter'].get(template_type, None)
    value_cp = value.copy()
    value_cp['title'] = _('Geographic filter')
    return default_repr(value_cp, request, template)


def temporal_filter_repr(value, request, template_type='default'):
    template = FILTER_TEMPLATES['temporal_filter'].get(template_type, None)
    value_cp = value.copy()
    value_cp['title'] = _('Temporal filter')
    return default_repr(value_cp, request, template)


def contribution_filter_repr(value, request, template_type='default'):
    template = FILTER_TEMPLATES['contribution_filter'].get(template_type, None)
    value_cp = value.copy()
    value_cp['title'] = _('Contribution filter')
    return default_repr(value_cp, request, template)


def text_filter_repr(value, request, template_type='default'):
    template = FILTER_TEMPLATES['text_filter'].get(template_type, None)
    value_cp = value.copy()
    value_cp['title'] = _('Text filter')
    return default_repr(value_cp, request, template)


def other_filter_repr(value, request, template_type='default'):
    template = FILTER_TEMPLATES['other_filter'].get(template_type, None)
    value_cp = value.copy()
    value_cp['title'] = _('Other filter')
    return default_repr(value_cp, request, template)


#****************************************Filter data analyzer


def metadata_filter_data(value):
    result = {}
    metadata_filter = value.get('metadata_filter', {})
    if metadata_filter:
        negation = metadata_filter.get('negation', False)
        content_types = metadata_filter.get('content_types', [])
        result['content_types'] = {
            'is_unique': (len(content_types) == 1) and not negation}

        states = metadata_filter.get('states', [])
        result['states'] = {'is_unique': (len(states) == 1) and not negation}

    return result


def geographic_filter_data(value):
    result = {}
    geographic_filter = value.get('geographic_filter', {})
    if geographic_filter:
        negation = geographic_filter.get('negation', False)
        country = geographic_filter.get('country', None)
        result['country'] = {'is_unique': country is not None and not negation}

        valid_zipcodes = geographic_filter.get('valid_zipcodes', [])
        result['valid_zipcodes'] = {
            'is_unique': (len(valid_zipcodes) == 1) and not negation}

    return result


def temporal_filter_data(value):
    result = {}
    return result


def contribution_filter_data(value):
    result = {}
    contribution_filter = value.get('contribution_filter', {})
    if contribution_filter:
        negation = contribution_filter.get('negation', False)
        authors = contribution_filter.get('authors', [])
        result['authors'] = {'is_unique': (len(authors) == 1) and not negation}

    return result


def text_filter_data(value):
    result = {}
    text_filter = value.get('text_filter', {})
    if text_filter:
        negation = text_filter.get('negation', False)
        text_to_search = text_filter.get('text_to_search', None)
        result['text_to_search'] = {
            'is_unique': text_to_search not in (None, '') and not negation}

    return result


def other_filter_data(value):
    result = {}
    other_filter = value.get('other_filter', {})
    if other_filter:
        negation = other_filter.get('negation', False)
        sources = other_filter.get('sources', [])
        result['sources'] = {'is_unique': (len(sources) == 1) and not negation}

    return result


#*****************************************Filter Schema


@colander.deferred
def content_types_choices(node, kw):
    request = node.bindings['request']
    localizer = request.localizer
    analyzed_data = node.bindings.get('analyzed_data', {})
    values = []
    registry = get_current_registry()
    searchable_contents = dict(core.get_searchable_content(request))
    if 'content_types' in analyzed_data:
        values = [(c, '{} ({})'.format(
            localizer.translate(
                getattr(registry.content.content_types[c],
                        'type_title', str(c))),
            str(analyzed_data['content_types'].get(c, 0))))
            for c in sorted(analyzed_data['content_types'].keys())
            if c in searchable_contents]
    else:
        searchable_contents.pop('file')
        searchable_contents.pop('webadvertising')
        exclude_internal = request.user is None
        values = [(key, getattr(c, 'type_title', c.__class__.__name__))
                  for key, c in list(searchable_contents.items())
                  if not exclude_internal or
                  (exclude_internal and not getattr(c, 'internal_type', False))]

    values = sorted(values, key=lambda e: e[0])
    return Select2Widget(values=values, multiple=True)


@colander.deferred
def states_choices(node, kw):
    request = node.bindings['request']
    localizer = request.localizer
    analyzed_data = node.bindings.get('analyzed_data', {})
    searchable_contents = dict(core.get_searchable_content(request))
    values = []
    if 'states' in analyzed_data:
        flattened_states = get_content_types_states(
            searchable_contents, True, request)
        values = [(state, '{} ({})'.format(
            ', '.join([localizer.translate(s)
                       for s in flattened_states[state]]),
            str(analyzed_data['states'].get(state, 0))))
            for state in sorted(analyzed_data['states'].keys())
            if state in flattened_states]
    else:
        searchable_contents.pop('file')
        searchable_contents.pop('webadvertising')
        flattened_states = get_content_types_states(
            searchable_contents, True, request)
        values = [(k, ', '.join([localizer.translate(s)
                  for s in flattened_states[k]]))
                  for k in sorted(flattened_states.keys())]

    return Select2Widget(values=values, multiple=True)


@colander.deferred
def authors_choices(node, kw):
    """Country must be in the select tag for the initialization"""
    context = node.bindings['context']
    request = node.bindings['request']
    analyzed_data = node.bindings.get('analyzed_data', {})
    authors_data = analyzed_data.get('authors', {})
    values = []

    def title_getter(oid):
        author = None
        try:
            author = get_obj(int(oid))
        except Exception:
            return oid

        title = getattr(author, 'title', author.__name__)
        if authors_data:
            title += ' ('+str(authors_data.get(oid, 0))+')'

        return title

    ajax_url = request.resource_url(context,
                                    '@@novaideoapi',
                                    query={'op': 'find_user'})
    return AjaxSelect2Widget(
        values=values,
        ajax_url=ajax_url,
        multiple=True,
        title_getter=title_getter)


@colander.deferred
def keyword_widget(node, kw):
    root = getSite()
    values = [(i, i) for i in sorted(root.keywords)]
    return Select2Widget(values=values,
                         multiple=True)


class MetadataFilter(Schema):
    negation = colander.SchemaNode(
        colander.Boolean(),
        default=False,
        missing=False,
        label=_('Not'),
        title=None,
        description=_('Check the box to exclude values entered below.'),
        description_bottom=True,
        )

    content_types = colander.SchemaNode(
        colander.Set(),
        widget=content_types_choices,
        title=_('Types'),
        description=_('You can select the content types to be displayed.'),
        default=[],
        missing=[],
        query=content_types_query,
        analyzer=content_types_analyzer
        )

    keywords = colander.SchemaNode(
        colander.Set(),
        widget=keyword_widget,
        title=_('keywords'),
        description=_('You can select the keywords of the contents to be displayed.'),
        missing=[],
        query=keywords_query
    )

    states = colander.SchemaNode(
        colander.Set(),
        widget=states_choices,
        title=_('States'),
        description=_('You can select the states of the contents to be displayed.'),
        default=[],
        missing=[],
        query=states_query,
        analyzer=states_analyzer
    )



class CreatedDates(Schema):

    created_after = colander.SchemaNode(
        colander.Date(),
        title=_('Created after'),
        missing=None
        )

    created_before = colander.SchemaNode(
        colander.Date(),
        title=_('Created before'),
        description_bottom=True,
        description=_('You can select the creation dates of contents to be displayed.'),
        missing=None,
        )


class ConnectedDates(Schema):

    connected_after = colander.SchemaNode(
        colander.Date(),
        title=_('Connected after'),
        missing=None
        )

    connected_before = colander.SchemaNode(
        colander.Date(),
        title=_('Connected before'),
        description_bottom=True,
        description=_('You can select the last connection dates of users to be displayed.'),
        missing=None,
        )


class TemporalSchema(Schema):

    negation = colander.SchemaNode(
        colander.Boolean(),
        default=False,
        missing=False,
        label=_('Not'),
        title=None,
        description=_('Check the box to exclude values entered below.'),
        description_bottom=True,
        )

    created_date = omit(CreatedDates(
        widget=SimpleMappingWidget(css_class="filter-block"
                                             " object-well"
                                             " default-well"),
        query=created_date_query
        ),
            ["_csrf_token_"])

    connected_date = omit(ConnectedDates(
        widget=SimpleMappingWidget(css_class="filter-block"
                                             " object-well"
                                             " default-well"),
        query=connected_date_query
        ),
            ["_csrf_token_"])


class ContributionFilterSchema(Schema):

    negation = colander.SchemaNode(
        colander.Boolean(),
        default=False,
        missing=False,
        label=_('Not'),
        title=None,
        description=_('Check the box to exclude values entered below.'),
        description_bottom=True,
        )

    authors = colander.SchemaNode(
        colander.Set(),
        widget=authors_choices,
        title=_('Authors'),
        description=_('You can enter the authors names of the contents to be displayed.'),
        default=[],
        missing=[],
        query=authors_query,
        analyzer=authors_analyzer
        )


class TextFilterSchema(Schema):
    negation = colander.SchemaNode(
        colander.Boolean(),
        default=False,
        missing=False,
        label=_('Not'),
        title=None,
        description=_('Check the box to exclude values entered below.'),
        description_bottom=True,
        )

    text_to_search = colander.SchemaNode(
        colander.String(),
        title=_('Text'),
        description=_("You can enter the words that appear in the contents to be displayed."),
        default='',
        missing='',
        query=text_to_search_query
    )


class FilterSchema(Schema):

    metadata_filter = omit(MetadataFilter(
        widget=SimpleMappingtWidget(
            mapping_css_class='controled-form',
            ajax=True,
            activator_icon="glyphicon glyphicon-cog",
            activator_title=_('Metadata filter')),
        query=metadata_filter_query,
        analyzer=metadata_filter_analyzer,
        repr_value=metadata_filter_repr,
        filter_analyzer=metadata_filter_data
        ),
            ["_csrf_token_"])

    temporal_filter = omit(TemporalSchema(
        widget=SimpleMappingtWidget(
            mapping_css_class='controled-form',
            ajax=True,
            activator_icon="glyphicon glyphicon-calendar",
            activator_title=_('Temporal filter')),
        query=temporal_filter_query,
        analyzer=temporal_filter_analyzer,
        repr_value=temporal_filter_repr,
        filter_analyzer=temporal_filter_data
        ),
            ["_csrf_token_"])

    contribution_filter = omit(ContributionFilterSchema(
        widget=SimpleMappingtWidget(
            mapping_css_class='controled-form',
            ajax=True,
            activator_icon="glyphicon glyphicon-user",
            activator_title=_('Contribution filter')),
        query=contribution_filter_query,
        analyzer=contribution_filter_analyzer,
        repr_value=contribution_filter_repr,
        filter_analyzer=contribution_filter_data
        ),
            ["_csrf_token_"])

    text_filter = omit(TextFilterSchema(
        widget=SimpleMappingtWidget(
            mapping_css_class='controled-form',
            ajax=True,
            activator_icon="glyphicon glyphicon-pencil",
            activator_title=_('Text filter')),
        query=text_filter_query,
        analyzer=text_filter_analyzer,
        repr_value=text_filter_repr,
        filter_analyzer=text_filter_data
        ),
            ["_csrf_token_"])


@view_config(
    name='filter',
    renderer='pontus:templates/views_templates/grid.pt',
    )
class FilterView(FormView):
    title = _('Filter')
    name = 'filter'
    coordinates = 'main'
    schema = FilterSchema()
    formid = 'formfilter'
    wrapper_template = 'daceui:templates/simple_view_wrapper.pt'
    filter_template = 'novaideo:views/templates/filter.pt'

    def __init__(self,
                 context,
                 request,
                 parent=None,
                 wizard=None,
                 stepid=None,
                 **kwargs):
        super(FilterView, self).__init__(context,
                                         request,
                                         parent,
                                         wizard,
                                         stepid,
                                         **kwargs)
        self.error = False
        self.validated = {}
        self._validated = {}
        if self.params('filter_result') is not None or \
           kwargs.get('filter_result', None) is not None:
            self.calculate_posted_filter()

        self.schema = select(FilterSchema(),
                             ['metadata_filter',
                              ('temporal_filter', ['negation', 'created_date']),
                              'contribution_filter', 'text_filter'])

    def calculate_posted_filter(self):
        form, reqts = self._build_form()
        form.formid = self.viewid + '_' + form.formid
        posted_formid = None
        values = self.request.POST or self.request.GET
        if '__formid__' in values:
            posted_formid = values['__formid__']

        if posted_formid is not None and posted_formid == form.formid:
            try:
                controls = values.items()
                validated = form.validate(controls)
                self.validated = validated
                self.validated['request'] = self.request
                self._validated = validated.copy()
            except Exception as e:
                log.warning(e)

    def bind(self):
        analyzed_data = getattr(self, 'analyzed_data', {})
        appstruct = getattr(self, '_validated', {})
        error = getattr(self, 'error', False)
        return {'analyzed_data': analyzed_data,
                'appstruct': appstruct,
                'error': error}

    def default_data(self):
        return getattr(self, '_validated', {})

    def omit_filters(self, filters):
        self.schema = omit(FilterSchema(), filters)

    def select_filters(self, filters):
        self.schema = select(FilterSchema(), filters)

    def analyze_data(self, source):
        self.analyzed_data = get_analyzed_data(
            self.schema, source,
            getattr(self, 'validated', {}), ignore_node=True)

    def get_body(self, filter_data):
        filter_body = self.content(
            args=filter_data,
            template=self.filter_template)['body']
        return filter_body


def get_filter(view, url, omit=(),
               select=(), source=None, **args):
    formid = args.pop('filterid', '') + 'formfilter'
    filter_instance = FilterView(view.context, view.request, formid=formid)
    view.filter_instance = filter_instance
    if omit:
        filter_instance.omit_filters(omit)

    if select:
        filter_instance.select_filters(select)

    if source:
        filter_instance.analyze_data(source)

    filter_form = filter_instance.update()
    filter_body = filter_form['coordinates']\
                             [filter_instance.coordinates][0]['body']
    filter_data = {'filter_body': filter_body,
                   'filter_url': url,
                   'filter_source': args.get('filter_source', view.name),
                   'filter_message': view.title,
                   'filter_resul': view.params('filter_result') is not None,
                   'filter_validated': filter_instance.validated}
    return filter_form, filter_data


def repr_filter(filter_data, request, template_type='default'):
    filter_schema = FilterSchema()
    global_template = FILTER_TEMPLATES['global'][template_type]
    filter_template = FILTER_TEMPLATES['filter'][template_type]
    all_filters = []
    for filter_ in filter_data:
        filter_values = []
        for child in filter_schema.children:
            name = child.name
            value = filter_.get(name, _marker)
            if hasattr(child, 'repr_value') and \
               value is not _marker:
                filter_values.append(
                    child.repr_value(
                        value, request, template_type))

        values = {'bodies': filter_values}
        all_filters.append(renderers.render(
            filter_template,
            values, request))

    values = {'bodies': all_filters}
    body = renderers.render(
        global_template,
        values, request)
    return body


def find_entities(user=None,
                  add_query=None,
                  intersect=None,
                  force_publication_date=False,
                  sort_on=None,
                  reverse=False,
                  filters=[],
                  filter_op='and',
                  **args):
    if intersect is not None and len(intersect) == 0:
        return ResultSet([], 0, None)

    schema = FilterSchema()
    dace_catalog = find_catalog('dace')
    novaideo_catalog = find_catalog('novaideo')
    system_catalog = find_catalog('system')
    filters = deepcopy(filters)
    root = getSite()
    for filter_ in filters:
        filter_['dace'] = dace_catalog
        filter_['novaideo'] = novaideo_catalog
        filter_['system'] = system_catalog
        filter_['root'] = root

    query = get_filters_query(schema, filters, filter_op)
    and_op = QUERY_OPERATORS.get('and', 'default')
    if add_query:
        query = and_op(query, add_query)

    if args:
        args['dace'] = dace_catalog
        args['novaideo'] = novaideo_catalog
        args['system'] = system_catalog
        args['root'] = root
        args_query = get_filters_query(schema, [args], filter_op)
        query = and_op(query, args_query)

    if user:
        root = getSite()
        access_keys = novaideo_catalog['access_keys']
        keys = getattr(user, '__access_keys__', _marker)
        if keys is _marker:
            keys = core.generate_access_keys(user, root)

        keys = list(keys)
        if not(isinstance(user, Anonymous) and \
               getattr(root, 'only_for_members', False)):
            keys.append('always')

        query = and_op(query, access_keys.any(keys))

    #add publication interval
    # if force_publication_date or \
    #    not has_any_roles(roles=('PortalManager',)):
    #     start_date = end_date = datetime.datetime.now()
    #     start_date = datetime.datetime.combine(
    #         start_date,
    #         datetime.time(0, 0, 0, tzinfo=pytz.UTC))
    #     end_date = datetime.datetime.combine(
    #         end_date,
    #         datetime.time(23, 59, 59, tzinfo=pytz.UTC))
    #     start_date_index = novaideo_catalog['publication_start_date']
    #     query = and_op(query, start_date_index.inrange_with_not_indexed(
    #         start_date, end_date))

    #    print(query.print_tree())
    #    from timeit import default_timer as timer
    #    start = timer()
    try:
        result_set = query.execute()
    except ParseError as error:
        log.warning(error)
        return []
    #    end = timer() - start
    #    print(end)
    if intersect is not None:
        result_set = result_set.intersect(intersect)

    if sort_on is not None:
        result_set = result_set.sort(
            novaideo_catalog[sort_on], reverse=reverse)

    return result_set


def find_more_contents(obj):
    user = get_current()
    request = get_current_request()
    registry = request.registry
    content_type = registry.content.typeof(obj)
    query, args = obj.get_more_contents_criteria()
    if args is None:
        return []

    if 'objects' in args:
        return args['objects']

    if content_type:
        args['request'] = request
        return find_entities(
            user=user,
            add_query=query,
            sort_on='release_date',
            reverse=True,
            **args)

    return []


def get_entities_by_title(interfaces, title, **args):
    user = get_current()
    novaideo_catalog = find_catalog('novaideo')
    #index
    title_index = novaideo_catalog['object_title']
    #query
    titles = []
    if isinstance(title, (list, tuple, set)):
        titles = [normalize_title(t) for t in title]
    else:
        titles = [normalize_title(title)]

    query = title_index.any(titles)
    return find_entities(
        user=user,
        interfaces=interfaces,
        add_query=query,
        **args)


def get_users_by_keywords(keywords):
    if not keywords:
        return []

    return find_entities(
        metadata_filter={'content_types': ['person'],
                         'states': ['active'],
                         'keywords': keywords})


def get_users_by_preferences(content):
    novaideo_catalog = find_catalog('novaideo')
    favorites_index = novaideo_catalog['favorites']
    oid = get_oid(content, None)
    if oid is None:
        return []

    query = favorites_index.any([oid])

    return find_entities(
        metadata_filter={'content_types': ['person'],
                         'states': ['active']},
        add_query=query)


def get_contents_by_keywords(
    filter_, user, root,
    date_from, date_to):
    novaideo_catalog = find_catalog('novaideo')
    date_index = novaideo_catalog['published_at']
    query = None
    if date_from:
        date_from = datetime.datetime.combine(
            date_from,
            datetime.datetime.min.time())
        date_from = date_from.replace(tzinfo=pytz.UTC)
        query = date_index.gt(date_from)

    if date_to:
        date_to = datetime.datetime.combine(
            date_to,
            datetime.datetime.min.time())
        date_to = date_to.replace(tzinfo=pytz.UTC)
        if query is None:
            query = date_index.lt(date_to)
        else:
            query = query & date_index.lt(date_to)

    keywords = filter_.get('keywords', root.keywords)
    keywords_mapping = dict([(k.lower(), k) for k in keywords])
    objects = find_entities(
        user=user,
        add_query=query,
        **filter_)

    index = novaideo_catalog['object_keywords']
    intersection = index.family.IF.intersection
    object_ids = getattr(objects, 'ids', objects)
    if isinstance(object_ids, (list, types.GeneratorType)):
        object_ids = index.family.IF.Set(object_ids)

    result = [(keyword_id, len(intersection(oids, object_ids)))
              for keyword_id, oids in index._fwd_index.items()]
    result = dict([(keywords_mapping.get(k, k), v)
                   for k, v in result if v != 0])
    return result, object_ids.__len__()


def get_contents_by_states(
    filter_, user, root,
    date_from, date_to):
    novaideo_catalog = find_catalog('novaideo')
    date_index = novaideo_catalog['published_at']
    query = None
    if date_from:
        date_from = datetime.datetime.combine(
            date_from,
            datetime.datetime.min.time())
        date_from = date_from.replace(tzinfo=pytz.UTC)
        query = date_index.gt(date_from)

    if date_to:
        date_to = datetime.datetime.combine(
            date_to,
            datetime.datetime.min.time())
        date_to = date_to.replace(tzinfo=pytz.UTC)
        if query is None:
            query = date_index.lt(date_to)
        else:
            query = query & date_index.lt(date_to)

    objects = find_entities(
        user=user,
        add_query=query,
        **filter_)
    content_types = filter_.get('metadata_filter').get('content_types')
    states = filter_.get('metadata_filter').get('states')
    flattened_states = get_content_types_states(content_types, True)
    index = find_catalog('dace')['object_states']
    intersection = index.family.IF.intersection
    object_ids = getattr(objects, 'ids', objects)
    if isinstance(object_ids, (list, types.GeneratorType)):
        object_ids = index.family.IF.Set(object_ids)

    result = [(state_id, len(intersection(oids, object_ids)))
              for state_id, oids in index._fwd_index.items()]
    result = dict([(k, v) for k, v in result if v != 0 and
                   k in list(flattened_states.keys())])
    return result, object_ids.__len__()


def get_contents_by_dates(
    filter_, user, root,
    date_of, frequency,
    date_from, date_to):
    novaideo_catalog = find_catalog('novaideo')
    if date_of == 'examination':
        date_index = novaideo_catalog['examined_at']
    else:
        date_index = novaideo_catalog['published_at']

    query = None
    if date_from:
        date_from = datetime.datetime.combine(
            date_from,
            datetime.datetime.min.time())
        date_from = date_from.replace(tzinfo=pytz.UTC)
        query = date_index.gt(date_from)

    if date_to:
        date_to = datetime.datetime.combine(
            date_to,
            datetime.datetime.min.time())
        date_to = date_to.replace(tzinfo=pytz.UTC)
        if query is None:
            query = date_index.lt(date_to)
        else:
            query = query & date_index.lt(date_to)

    objects = find_entities(
        user=user,
        add_query=query,
        **filter_)
    index = novaideo_catalog[
        INDEX_MAPPING.get((date_of, frequency), 'published_at_month_str')]
    intersection = index.family.IF.intersection
    object_ids = getattr(objects, 'ids', objects)
    if isinstance(object_ids, (list, types.GeneratorType)):
        object_ids = index.family.IF.Set(object_ids)

    result = [(dateid, len(intersection(oids, object_ids)))
              for dateid, oids in index._fwd_index.items()]

    result = dict([(k, v) for k, v in result if v != 0])
    return result, object_ids.__len__()
