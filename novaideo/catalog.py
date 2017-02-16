
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
from dace.objectofcollaboration.principal.util import (
    get_objects_with_role)
# from novaideo.utilities.tree_utility import (
#     get_branches, tree_to_keywords)
from novaideo import get_access_keys
from novaideo.fr_lexicon import (
    Splitter, CaseNormalizer,
    StopWordRemover, Lexicon,
    normalize_word)
from novaideo.content.interface import (
    IEntity,
    IPerson,
    IProposal,
    Iidea,
    IComment,
    IPreregistration,
    IInvitation,
    IAlert,
    ISustainable)
from novaideo.dateindex import DateRecurring


class ISearchableObject(Interface):

    def release_date():
        pass

    def publication_start_date():
        pass

    def publication_end_date():
        pass

    def object_keywords():
        pass

    def object_authors():
        pass

    def organizations():
        pass

    def created_at():
        pass

    def modified_at():
        pass

    def published_at():
        pass

    def examined_at():
        pass
    #str
    def published_at_str():
        pass

    def examined_at_str():
        pass

    def published_at_month_str():
        pass

    def examined_at_month_str():
        pass

    def published_at_year_str():
        pass

    def examined_at_year_str():
        pass
    #end
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

    def related_contents():
        pass

    def has_related_contents():
        pass

    def has_file():
        pass

    def identifier():
        pass

    def is_pinned():
        pass

    def is_edited():
        pass

    def alert_keys():
        pass

    def alert_exclude_keys():
        pass

    def support():
        pass

    def oppose():
        pass

    def support_diff():
        pass

    def challenges():
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

    @indexview()
    def publication_start_date(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        return adapter.publication_start_date()

    @indexview()
    def publication_end_date(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        return adapter.publication_end_date()

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
    def organizations(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        return adapter.organizations()

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
    def published_at(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        published_at = adapter.published_at()
        if published_at is None:
            return default

        return published_at

    @indexview()
    def examined_at(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        examined_at = adapter.examined_at()
        if examined_at is None:
            return default

        return examined_at

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

    @indexview()
    def related_contents(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        related_contents = adapter.related_contents()
        if related_contents is None:
            return default

        return related_contents

    @indexview()
    def published_at_str(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        published_at_str = adapter.published_at_str()
        if published_at_str is None:
            return default

        return published_at_str

    @indexview()
    def examined_at_str(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        examined_at_str = adapter.examined_at_str()
        if examined_at_str is None:
            return default

        return examined_at_str

    @indexview()
    def published_at_month_str(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        published_at_month_str = adapter.published_at_month_str()
        if published_at_month_str is None:
            return default

        return published_at_month_str

    @indexview()
    def examined_at_month_str(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        examined_at_month_str = adapter.examined_at_month_str()
        if examined_at_month_str is None:
            return default

        return examined_at_month_str

    @indexview()
    def published_at_year_str(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        published_at_year_str = adapter.published_at_year_str()
        if published_at_year_str is None:
            return default

        return published_at_year_str

    @indexview()
    def examined_at_year_str(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        examined_at_year_str = adapter.examined_at_year_str()
        if examined_at_year_str is None:
            return default

        return examined_at_year_str

    @indexview()
    def has_related_contents(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        has_related_contents = adapter.has_related_contents()
        if has_related_contents is None:
            return default

        return has_related_contents

    @indexview()
    def has_file(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        has_file = adapter.has_file()
        if has_file is None:
            return default

        return has_file

    @indexview()
    def identifier(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        identifier = adapter.identifier()
        if identifier is None:
            return default

        return identifier

    @indexview()
    def is_pinned(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        is_pinned = adapter.is_pinned()
        if is_pinned is None:
            return default

        return is_pinned

    @indexview()
    def is_edited(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        is_edited = adapter.is_edited()
        if is_edited is None:
            return default

        return is_edited

    @indexview()
    def alert_keys(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        alert_keys = adapter.alert_keys()
        if alert_keys is None:
            return default

        return alert_keys

    @indexview()
    def alert_exclude_keys(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        alert_exclude_keys = adapter.alert_exclude_keys()
        if alert_exclude_keys is None:
            return default

        return alert_exclude_keys


    @indexview()
    def support(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        support = adapter.support()
        if support is None:
            return default

        return support

    @indexview()
    def oppose(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        oppose = adapter.oppose()
        if oppose is None:
            return default

        return oppose

    @indexview()
    def support_diff(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        support_diff = adapter.support_diff()
        if support_diff is None:
            return default

        return support_diff

    @indexview()
    def challenges(self, default):
        adapter = get_current_registry().queryAdapter(
            self.resource, ISearchableObject)
        if adapter is None:
            return default

        challenges = adapter.challenges()
        if challenges is None:
            return default

        return challenges


@catalog_factory('novaideo')
class NovaideoIndexes(object):

    object_keywords = Keyword()
    object_authors = Keyword()
    organizations = Keyword()
    created_at = Field()
    modified_at = Field()
    published_at = Field()
    examined_at = Field()
    published_at_str = Field()
    examined_at_str = Field()
    published_at_month_str = Field()
    examined_at_month_str = Field()
    published_at_year_str = Field()
    examined_at_year_str = Field()
    release_date = Field()
    is_workable = Field()
    favorites = Keyword()
    related_contents = Keyword()
    last_connection = Field()
    publication_start_date = DateRecurring()
    publication_end_date = DateRecurring()
    object_id = Field()
    object_title = Field()
    object_access_control = Keyword()
    access_keys = Keyword()
    relevant_data = Text(
        lexicon=Lexicon(Splitter(), CaseNormalizer(), StopWordRemover()))
    has_related_contents = Field()
    has_file = Field()
    identifier = Keyword()
    is_pinned = Field()
    is_edited = Field()
    alert_keys = Keyword()
    alert_exclude_keys = Keyword()
    support = Field()
    oppose = Field()
    support_diff = Field()
    challenges = Keyword()


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
            return [get_oid(author)]

        return []

    def organizations(self):
        organization = getattr(self.context, 'organization', None)
        if organization:
            return [get_oid(organization)]

        return [0]

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

    def published_at(self):
        return getattr(self.context, 'published_at', self.created_at())

    def examined_at(self):
        return getattr(self.context, 'examined_at', None)

    def published_at_str(self):
        date = getattr(self.context, 'published_at', self.created_at())
        return date.strftime("%d/%m/%Y")

    def examined_at_str(self):
        date = getattr(self.context, 'examined_at', None)
        if date:
            return date.strftime("%d/%m/%Y")

        return None

    def published_at_month_str(self):
        date = getattr(self.context, 'published_at', self.created_at())
        return date.strftime("%m/%Y")

    def examined_at_month_str(self):
        date = getattr(self.context, 'examined_at', None)
        if date:
            return date.strftime("%m/%Y")

        return None

    def published_at_year_str(self):
        date = getattr(self.context, 'published_at', self.created_at())
        return date.strftime("%Y")

    def examined_at_year_str(self):
        date = getattr(self.context, 'examined_at', None)
        if date:
            return date.strftime("%Y")

        return None

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
        return self.modified_at()

    def related_contents(self):
        return []

    def publication_start_date(self):
        start_date = getattr(
            self.context, 'visibility_dates_start_date', None)
        if start_date:
            return {'attr': 'visibility_dates',
                    'date': start_date}

        return None

    def publication_end_date(self):
        end_date = getattr(
            self.context, 'visibility_dates_end_date', None)
        if end_date:
            return {'attr': 'visibility_dates',
                    'date': end_date}

        return None

    def has_related_contents(self):
        return False

    def has_file(self):
        return False

    def identifier(self):
        return []

    def is_pinned(self):
        return False

    def is_edited(self):
        return False

    def alert_keys(self):
        return []

    def alert_exclude_keys(self):
        return []

    def support(self):
        return 0

    def oppose(self):
        return 0

    def support_diff(self):
        return 0

    def challenges(self):
        challenge = getattr(self.context, 'challenge', None)
        return [get_oid(challenge)] if challenge else []


@adapter(context=IPerson)
@implementer(ISearchableObject)
class PersonSearch(SearchableObject):

    def favorites(self):
        selections = getattr(self.context, 'selections', [])
        return [get_oid(s) for s in selections]

    def last_connection(self):
        return getattr(self.context, 'last_connection', None)

    def identifier(self):
        identifiers = [getattr(self.context, 'identifier', None),
                       getattr(self.context, 'email', None)]
        return [i for i in identifiers if i]

    def organizations(self):
        organization = getattr(self.context, 'organization', None)
        if organization:
            return [get_oid(organization)]

        return []

    def challenges(self):
        challenges = get_objects_with_role(
            self.context, 'ChallengeParticipant')
        return [get_oid(challenge) for challenge in challenges]


@adapter(context=IPreregistration)
@implementer(ISearchableObject)
class PreregistrationSearch(SearchableObject):

    def identifier(self):
        identifiers = [getattr(self.context, 'identifier', None),
                       getattr(self.context, 'email', None)]
        return [i for i in identifiers if i]


@adapter(context=IInvitation)
@implementer(ISearchableObject)
class InvitationSearch(SearchableObject):

    def identifier(self):
        return [getattr(self.context, 'email', None)]


@adapter(context=IProposal)
@implementer(ISearchableObject)
class ProposalSearch(SearchableObject):

    def related_contents(self):
        ideas = getattr(self.context, 'related_ideas', [])
        ids = list(set([get_oid(i, None) for i in ideas]))
        if None in ids:
            ids.remove(None)

        return ids

    def has_related_contents(self):
        return True if self.related_contents() else False

    def has_file(self):
        return True if self.context.attached_files else False

    def support(self):
        return len(getattr(self.context, 'tokens_support', []))

    def oppose(self):
        return len(getattr(self.context, 'tokens_opposition', []))

    def support_diff(self):
        return self.support() - self.oppose()


@adapter(context=Iidea)
@implementer(ISearchableObject)
class IdeaSearch(SearchableObject):

    def related_contents(self):
        proposals = getattr(self.context, 'related_proposals', [])
        ids = list(set([get_oid(i, None) for i in proposals]))
        if None in ids:
            ids.remove(None)

        return ids

    def has_related_contents(self):
        return True if self.related_contents() else False

    def has_file(self):
        return True if self.context.attached_files else False

    def support(self):
        return len(getattr(self.context, 'tokens_support', []))

    def oppose(self):
        return len(getattr(self.context, 'tokens_opposition', []))

    def support_diff(self):
        return self.support() - self.oppose()


@adapter(context=IComment)
@implementer(ISearchableObject)
class CommentSearch(SearchableObject):

    def related_contents(self):
        related_contents = getattr(
            self.context.related_correlation, 'targets', [])
        ids = list(set([get_oid(i, None) for i in related_contents]))
        if None in ids:
            ids.remove(None)

        return ids

    def has_related_contents(self):
        return True if self.related_contents() else False

    def has_file(self):
        return True if self.context.files else False

    def is_pinned(self):
        return getattr(self.context, 'pinned', False)

    def is_edited(self):
        return getattr(self.context, 'edited', False)


@adapter(context=IAlert)
@implementer(ISearchableObject)
class AlertSearch(SearchableObject):

    def related_contents(self):
        subjects = getattr(self.context, 'subjects', [])
        ids = list(set([get_oid(i, None) for i in subjects]))
        if None in ids:
            ids.remove(None)

        return ids

    def alert_keys(self):
        return list(self.context.users_toalert)

    def alert_exclude_keys(self):
        users_toexclude = list(self.context.users_toexclude)
        return users_toexclude if users_toexclude else ['no_one']


@adapter(context=ISustainable)
@implementer(ISearchableObject)
class SustainableSearch(SearchableObject):

    def support(self):
        return len(getattr(self.context, 'votes_positive', []))

    def oppose(self):
        return len(getattr(self.context, 'votes_negative', []))

    def support_diff(self):
        return self.support() - self.oppose()