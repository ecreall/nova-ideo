
from zope.interface import Interface, implementer
from pyramid.threadlocal import get_current_registry

from substanced.util import get_oid
from substanced.catalog import (
    catalog_factory,
    Keyword,
    Field,
    Text,
    indexview,
    indexview_defaults,
    )

from dace.util import Adapter, adapter

# from novaideo.utilities.tree_utility import (
#     get_branches, tree_to_keywords)
from novaideo import get_access_keys
from novaideo.fr_lexicon import (
    Splitter, CaseNormalizer,
    StopWordRemover, Lexicon,
    normalize_word)
from novaideo.content.interface import (
    IEntity,
    IPerson)


class ISearchableObject(Interface):

    def release_date():
        pass

    # def publication_start_date():
    #     pass

    # def publication_end_date():
    #     pass

    def object_keywords():
        pass

    def object_authors():
        pass

    def created_at():
        pass

    def modified_at():
        pass

    def object_title():
        pass

    def object_access_control():
        pass

    def access_keys():
        pass

    def relevant_data():
        pass

    def is_workable():
        pass

    def favorites():
        pass

    def last_connection():
        pass


@indexview_defaults(catalog_name='novaideo')
class NovaideoCatalogViews(object):

    def __init__(self, resource):
        self.resource = resource

    @indexview()
    def release_date(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        return adapter.release_date()

    # @indexview()
    # def publication_start_date(self, default):
    #     adapter = get_current_registry().queryAdapter(
    #         self.resource, ISearchableObject)
    #     if adapter is None:
    #         return default

    #     return adapter.publication_start_date()

    # @indexview()
    # def publication_end_date(self, default):
    #     adapter = get_current_registry().queryAdapter(
    #         self.resource, ISearchableObject)
    #     if adapter is None:
    #         return default

    #     return adapter.publication_end_date()

    @indexview()
    def object_keywords(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        return adapter.object_keywords()

    @indexview()
    def object_authors(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        return adapter.object_authors()

    @indexview()
    def access_keys(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        return adapter.access_keys()

    @indexview()
    def created_at(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        created_at = adapter.created_at()
        if created_at is None:
            return default

        return created_at

    @indexview()
    def modified_at(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        modified_at = adapter.modified_at()
        if modified_at is None:
            return default

        return modified_at

    @indexview()
    def object_title(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        object_title = adapter.object_title()
        if object_title is None:
            return default

        return object_title

    @indexview()
    def object_access_control(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        object_access_control = adapter.object_access_control()
        if object_access_control is None:
            return default

        return object_access_control

    @indexview()
    def relevant_data(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        relevant_data = adapter.relevant_data()
        if relevant_data is None:
            return default

        return relevant_data

    @indexview()
    def is_workable(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        is_workable = adapter.is_workable()
        if is_workable is None:
            return default

        return is_workable

    @indexview()
    def favorites(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        favorites = adapter.favorites()
        if favorites is None:
            return default

        return favorites

    @indexview()
    def last_connection(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        last_connection = adapter.last_connection()
        if last_connection is None:
            return default

        return last_connection


@catalog_factory('novaideo')
class NovaideoIndexes(object):

    object_keywords = Keyword()
    object_authors = Keyword()
    created_at = Field()
    modified_at = Field()
    release_date = Field()
    is_workable = Field()
    favorites = Keyword()
    last_connection = Field()
    # publication_start_date = Field()
    # publication_end_date = Field()
    object_id = Field()
    object_title = Field()
    object_access_control = Keyword()
    access_keys = Keyword()
    relevant_data = Text(
        lexicon=Lexicon(Splitter(), CaseNormalizer(), StopWordRemover()))


@adapter(context=IEntity)
@implementer(ISearchableObject)
class SearchableObject(Adapter):
    """Return all keywords.
    """

    def release_date(self):
        return getattr(self.context, 'release_date', self.modified_at())

    def object_keywords(self):
        keywords = list(getattr(self.context, 'keywords', []))
        if keywords:
            keywords = list([k.lower() for k in keywords])

        return keywords

    def object_authors(self):
        author = getattr(self.context, 'author', None)
        if author:
            try:
                return [get_oid(author)]
            except:
                return []

        return []

    def object_title(self):
        title = getattr(self.context, 'title', '')
        title = normalize_word(title)
        return title.replace('(', '').replace(')', '')

    def access_keys(self):
        return get_access_keys(self.context)

    def created_at(self):
        return getattr(self.context, 'created_at', None)

    def modified_at(self):
        return getattr(self.context, 'modified_at', None)

    def object_access_control(self):
        access_control = getattr(self.context, 'access_control', ['all'])
        if access_control:
            return [str(a) for a in access_control]

        return ['all']

    def relevant_data(self):
        relevant_data = ', '.join(getattr(self.context, 'relevant_data', []))
        if not relevant_data:
            return None

        return relevant_data

    def is_workable(self):
        return getattr(self.context, 'is_workable', False)

    def favorites(self):
        return []

    def last_connection(self):
        return None


@adapter(context=IPerson)
@implementer(ISearchableObject)
class ArtistSearch(SearchableObject):

    def favorites(self):
        selections = getattr(self.context, 'selections', [])
        return [get_oid(s) for s in selections]

    def last_connection(self):
        return getattr(self.context, 'last_connection', None)
