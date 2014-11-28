# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from substanced.catalog import (
    catalog_factory,
    Keyword,
    indexview,
    indexview_defaults,
    )

from dace.util import getSite


@indexview_defaults(catalog_name='novaideo')
class NovaideoCatalogViews(object):

    def __init__(self, resource):
        self.resource = resource

    @indexview()
    def object_keywords(self, default):
        """index objects by their keywords"""
        root = getSite()
        if self.resource is None:
            return default

        keywords = getattr(self.resource, 'keywords', default)
        if self.resource is root:
            keywords = root.keywords_ids

        if not keywords is default:
            keywords = [k.lower() for k in keywords]

        return keywords


@catalog_factory('novaideo')
class NovaideoIndexes(object):

    object_keywords = Keyword()
