# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
import venusian
from persistent.list import PersistentList
from zope.interface import implementer
from pyramid.threadlocal import get_current_request, get_current_registry

from substanced.util import get_oid
from substanced.interfaces import IUserLocator
from substanced.principal import DefaultUserLocator
from substanced.util import renamer
from substanced.content import content

from dace.objectofcollaboration.principal.role import DACE_ROLES
from dace.objectofcollaboration.principal.util import get_access_keys
from dace.objectofcollaboration.entity import Entity
from dace.descriptors import (
    SharedUniqueProperty,
    CompositeUniqueProperty,
    SharedMultipleProperty,
    CompositeMultipleProperty)
from dace.util import getSite
from pontus.schema import Schema
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import (
    RichTextWidget, Select2Widget)

from novaideo import _, ACCESS_ACTIONS
from novaideo.content.interface import (
    IVersionableEntity,
    IDuplicableEntity,
    ISearchableEntity,
    ICommentable,
    ICorrelableEntity,
    IPresentableEntity,
    IFile)


BATCH_DEFAULT_SIZE = 100

SEARCHABLE_CONTENTS = {}

NOVAIDO_ACCES_ACTIONS = {}


def get_searchable_content(request=None):
    if request is None:
        request = get_current_request()

    return getattr(request, 'searchable_contents', {})


class access_action(object):
    """ Decorator for creationculturelle access actions.
    An access action allows to view an object"""

    def __init__(self, access_key=None):
        self.access_key = access_key

    def __call__(self, wrapped):
        def callback(scanner, name, ob):
            if ob.context in ACCESS_ACTIONS:
                ACCESS_ACTIONS[ob.context].append({'action': ob,
                                                   'access_key': self.access_key})
            else:
                ACCESS_ACTIONS[ob.context] = [{'action': ob,
                                               'access_key': self.access_key}]

        venusian.attach(wrapped, callback)
        return wrapped


def can_access(user, context, request=None, root=None):
    """ Return 'True' if the user can access to the context"""
    declared = context.__provides__.declared[0]
    for data in ACCESS_ACTIONS.get(declared, []):
        if data['action'].processsecurity_validation(None, context):
            return True

    return False


_marker = object()


def serialize_roles(roles, root=None):
    result = []
    principal_root = getSite()
    if principal_root is None:
        return []

    if root is None:
        root = principal_root

    root_oid = str(get_oid(root, ''))
    principal_root_oid = str(get_oid(principal_root, ''))
    for role in roles:
        if isinstance(role, tuple):
            obj_oid = str(get_oid(role[1], ''))
            result.append((role[0]+'_'+obj_oid).lower())
            superiors = getattr(DACE_ROLES.get(role[0], _marker),
                                'all_superiors', [])
            result.extend([(r.name+'_'+obj_oid).lower()
                           for r in superiors])
        else:
            result.append(role.lower()+'_'+root_oid)
            superiors = getattr(DACE_ROLES.get(role, _marker),
                                'all_superiors', [])
            result.extend([(r.name+'_'+root_oid).lower() for r in
                           superiors])

        for superior in superiors:
            if superior.name == 'Admin':
                result.append('admin_'+principal_root_oid)
                break

    return list(set(result))


def generate_access_keys(user, root):
    root_oid = str(get_oid(root))
    access_keys = get_access_keys(
        user, root=root)
    root_keys = [a for a in access_keys if a.endswith(root_oid)]
    root_roles = [(a, a.replace('_'+root_oid, '')) for a in root_keys]
    local_keys = list(set(access_keys) - set(root_keys))

    def is_valid(role, local_keys):
        return role == 'admin' or\
            any(a.startswith(role)
                for a in local_keys)

    valid_root_keys = [a for a, role in root_roles
                       if is_valid(role, local_keys)]
    valid_access_keys = local_keys
    valid_access_keys.extend(valid_root_keys)
    return valid_access_keys


@implementer(ICommentable)
class Commentable(VisualisableElement, Entity):
    """ A Commentable entity is an entity that can be comment"""

    name = renamer()
    comments = CompositeMultipleProperty('comments')


@implementer(IVersionableEntity)
class VersionableEntity(Entity):
    """ A Versionable entity is an entity that can be versioned"""

    version = CompositeUniqueProperty('version', 'nextversion')
    nextversion = SharedUniqueProperty('nextversion', 'version')

    @property
    def current_version(self):
        """ Return the current version"""

        if self.nextversion is None:
            return self
        else:
            return self.nextversion.current_version

    @property
    def history(self):
        """ Return all versions"""

        result = []
        if self.version is None:
            return [self]
        else:
            result.append(self)
            result.extend(self.version.history)

        return result

    def destroy(self):
        """Remove branch"""

        if self.version:
            self.version.destroy()

        if self.nextversion:
            self.nextversion.delfromproperty('version', self)


@implementer(IDuplicableEntity)
class DuplicableEntity(Entity):
    """ A Duplicable entity is an entity that can be duplicated"""

    originalentity = SharedUniqueProperty('originalentity', 'duplicates')
    duplicates = SharedMultipleProperty('duplicates', 'originalentity')


@colander.deferred
def keywords_choice(node, kw):
    root = getSite()
    values = [(i, i) for i in sorted(root.keywords)]
    create = getattr(root, 'can_add_keywords', True)
    return Select2Widget(max_len=5,
                         values=values,
                         create=create,
                         multiple=True)


class SearchableEntitySchema(Schema):

    keywords = colander.SchemaNode(
        colander.Set(),
        widget=keywords_choice,
        title=_('Keywords'),
        description=_("To add keywords, you need to tap the « Enter »"
                      " key after each keyword or separate them with commas.")
        )


@implementer(ISearchableEntity)
class SearchableEntity(Entity):
    """ A Searchable entity is an entity that can be searched"""

    templates = {'default': 'novaideo:templates/views/default_result.pt',
                 'bloc': 'novaideo:templates/views/default_result.pt'}

    def __init__(self, **kwargs):
        super(SearchableEntity, self).__init__(**kwargs)
        self.keywords = PersistentList()

    @property
    def is_published(self):
        return 'published' in self.state

    @property
    def is_workable(self):
        return self.is_published

    @property
    def relevant_data(self):
        return [getattr(self, 'title', ''),
                getattr(self, 'description', ''),
                ', '.join(self.keywords)]

    def _init_presentation_text(self):
        pass

    def get_release_date(self):
        return getattr(self, 'release_date', self.modified_at)

    def presentation_text(self, nb_characters=400):
        return getattr(self, 'description', "")[:nb_characters]+'...'

    def get_more_contents_criteria(self):
        "return specific query, filter values"
        return None, {
            'metadata_filter': {
                'states': ['published'],
                'keywords': list(self.keywords)
            }
        }


@implementer(IPresentableEntity)
class PresentableEntity(Entity):
    """ A Presentable entity is an entity that can be presented"""

    def __init__(self, **kwargs):
        super(PresentableEntity, self).__init__(**kwargs)
        self._email_persons_contacted = PersistentList()

    @property
    def persons_contacted(self):
        """ Return all contacted persons"""

        request = get_current_request()
        adapter = request.registry.queryMultiAdapter(
                (self, request),
                IUserLocator
                )
        if adapter is None:
            adapter = DefaultUserLocator(self, request)

        result = []
        for email in self._email_persons_contacted:
            user = adapter.get_user_by_email(email)
            if user is not None:
                result.append(user)
            else:
                result.append(email.split('@')[0].split('+')[0])

        return set(result)


@implementer(ICorrelableEntity)
class CorrelableEntity(Entity):
    """
    A Correlable entity is an entity that can be correlated.
    A correlation is an abstract association between source entity
    and targets entities.
    """

    source_correlations = SharedMultipleProperty('source_correlations',
                                                 'source')
    target_correlations = SharedMultipleProperty('target_correlations',
                                                 'targets')

    @property
    def correlations(self):
        """Return all source correlations and target correlations"""
        result = [c.target for c in self.source_correlations]
        result.extend([c.source for c in self.target_correlations])
        return list(set(result))


class FileSchema(VisualisableElementSchema, SearchableEntitySchema):

    text = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget(),
        title=_("Text")
        )


@content(
    'file',
    icon='icon novaideo-icon icon-user',
    )
@implementer(IFile)
class FileEntity(SearchableEntity):
    """ A file entity is an entity that can be searched"""

    icon = "glyphicon glyphicon-file"
    templates = {'default': 'novaideo:views/templates/file_result.pt'}
    type_title = _('File')

    def __init__(self, **kwargs):
        super(FileEntity, self).__init__(**kwargs)
        self.set_data(kwargs)
