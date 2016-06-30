# Copyright (c) 2015 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import re
from dace.util import getSite

from novaideo import core
from novaideo.utilities.util import (
    deepcopy)


def _and_operator(query1, query2):
    if not query1:
        return query2

    if not query2:
        return query1

    return (query1 & query2)


def _or_operator(query1, query2):
    if not query1:
        return query2

    if not query2:
        return query1

    return (query1 | query2)


QUERY_OPERATORS = {
    'and': _and_operator,
    'or': _or_operator,
    'default': _and_operator
}


def get_node_query(node, operator='and', **args):
    query = None
    operator_op = QUERY_OPERATORS.get(operator, 'default')
    for child in node.children:
        if hasattr(child, 'query'):
            child_query = child.query(child, **args)
            if child_query:
                if query:
                    query = operator_op(query, child_query)
                else:
                    query = child_query
    return query


def get_filters_query(node, filters, operator='and'):
    query = None
    operator_op = QUERY_OPERATORS.get(operator, 'default')
    for filter_ in filters:
        filter_query = get_node_query(node, 'and', **filter_)
        if query:
            query = operator_op(query, filter_query)
        else:
            query = filter_query

    return query


def get_analyzed_data(node, source, validated, ignore_node=False):
    result = {}
    for child in node.children:
        if hasattr(child, 'analyzer'):
            validated_cp = deepcopy(validated)
            if not ignore_node and child.name in validated_cp:
                validated_cp.pop(child.name)

            result_child = child.analyzer(
                child, source, validated_cp,
                validated.get(child.name, []))
            if result_child is not None:
                result.update(result_child)

    return result


def get_filter_nodes_to_omit(node, filter_):
    result_node = []
    for child in node.children:
        if hasattr(child, 'filter_analyzer'):
            filter_cp = deepcopy(filter_)
            result_child = child.filter_analyzer(filter_cp)
            if result_child:
                nodes_to_omit = [n for n in result_child.keys()
                                 if result_child[n]['is_unique']]
                result_node.append((child.name, nodes_to_omit))

    return result_node


def match_in(zipcode, zipcodes, negation=False):
    for dep in zipcodes:
        if re.match(dep, zipcode):
            return True

    return False


def get_zipcodes(zipcodes, country=None):
    root = getSite()
    resourcemanager = root.resourcemanager
    queries = []
    for zipcode in zipcodes:
        queries.append({"regexp": {"zipcode": zipcode}})

    query = {"bool": {"should": queries,
                      "minimum_should_match": 1}}
    if country:
        country_query = {
            "must": [{"match": {"country_name": {"query": country,
                                                 "operator": "and"}}}]}
        query["bool"].update(country_query)

    result = resourcemanager.get_entries(
        key='city',
        query=query,
        params={"from": 0,
                "size": 100000},
        fields=["zipcode"])
    if result[1] == 0:
        return []

    return result[0]


def get_zipcodes_from_cities(cities, country=None):
    root = getSite()
    resourcemanager = root.resourcemanager
    queries = []
    for city in cities:
        queries.append({"match": {"city_normalized_name": city}})

    query = {"bool": {"should": queries,
                      "minimum_should_match": 1}}
    if country:
        country_query = {
            "must": [{"match": {"country_name": {"query": country,
                                                 "operator": "and"}}}]}
        query["bool"].update(country_query)

    result = resourcemanager.get_entries(
        key='city',
        query=query,
        params={"from": 0,
                "size": 100000},
        fields=["zipcode"])

    if result[1] == 0:
        return []

    result = list(set([str(item) for c in result[0]
                       for item in c['fields']['zipcode']]))
    return result


def get_valid_interfaces(interfaces, args):
    selected_interfaces = []
    if interfaces:
        def _interface_in(other_interface, interfaces):
            for interface in interfaces:
                if other_interface.isOrExtends(interface):
                    return True

            return False

        content_types = args.get('content_types', [])
        searchable_contents = core.get_searchable_content()
        valid_interfaces = [list(searchable_contents[i].
                                 __implemented__.declared)
                            for i in content_types if i in searchable_contents]
        valid_interfaces = [item for sublist in
                            valid_interfaces for item in sublist]
        selected_interfaces = [i for i in valid_interfaces
                               if _interface_in(i, interfaces)]

    return selected_interfaces


def merge_with_filter_view(view, args):
    validated = None
    if view and getattr(view, 'filter_instance', None):
        validated = view.filter_instance.validated

    if not validated:
        return deepcopy(args)

    if not args:
        return deepcopy(validated)

    result = deepcopy(validated)
    for arg in deepcopy(args):
        if arg not in validated:
            result[arg] = args[arg]

    return result
