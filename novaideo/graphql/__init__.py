# -*- coding: utf-8 -*-
from graphene.types.resolver import set_default_resolver


def substanced_attr_resolver(attname, default_value, root, args, context, info):
    """attr_resolver that handle SubstanceD objects."""
    if attname == 'id':
        attname = '__oid__'

    return getattr(root, attname, default_value)


set_default_resolver(substanced_attr_resolver)


def includeme(config):
    config.add_route('graphql', '/graphql')
    config.scan()
