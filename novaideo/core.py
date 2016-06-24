# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
import venusian
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from zope.interface import implementer
from pyramid.threadlocal import get_current_request

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
from dace.util import getSite, get_obj
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
    IPrivateChannel,
    IChannel,
    ICorrelableEntity,
    IPresentableEntity,
    IFile,
    INode)


BATCH_DEFAULT_SIZE = 8

SEARCHABLE_CONTENTS = {}

NOVAIDO_ACCES_ACTIONS = {}

ADVERTISING_CONTAINERS = {}


def get_searchable_content(request=None):
    if request is None:
        request = get_current_request()

    return getattr(request, 'searchable_contents', {})


class advertising_banner_config(object):
    """ A function, class or method decorator which allows a
    developer to create advertising banner registrations.

    Advertising banner is a panel. See pyramid_layout.panel_config.
    """
    def __init__(self, name='', context=None, renderer=None, attr=None):
        self.name = name
        self.context = context
        self.renderer = renderer
        self.attr = attr

    def __call__(self, wrapped):
        settings = self.__dict__.copy()

        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            config.add_panel(panel=ob, **settings)
            ADVERTISING_CONTAINERS[self.name] = {'title': ob.title,
                                                 'description': ob.description,
                                                 'order': ob.order,
                                                 'validator': ob.validator,
                                                 'tags': ob.tags
                                                 #TODO add validator ob.validator
                                                 }

        info = venusian.attach(wrapped, callback, category='pyramid_layout')

        if info.scope == 'class':
            # if the decorator was attached to a method in a class, or
            # otherwise executed at class scope, we need to set an
            # 'attr' into the settings if one isn't already in there
            if settings['attr'] is None:
                settings['attr'] = wrapped.__name__

        settings['_info'] = info.codeinfo # fbo "action_method"
        return wrapped


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
    return get_access_keys(
        user, root=root)


@implementer(ICommentable)
class Commentable(VisualisableElement, Entity):
    """ A Commentable entity is an entity that can be comment"""

    name = renamer()
    comments = CompositeMultipleProperty('comments')

    def __init__(self, **kwargs):
        super(Commentable, self).__init__(**kwargs)
        self.len_comments = 0

    def update_len_comments(self):
        result = len(self.comments)
        result += sum([c.update_len_comments() for c in self.comments])
        self.len_comments = result
        return self.len_comments

    def addtoproperty(self, name, value, moving=None):
        super(Commentable, self).addtoproperty(name, value, moving)
        if name == 'comments':
            channel = getattr(self, 'channel', self)
            channel.len_comments += 1
            if self is not channel:
                self.len_comments += 1

    def delfromproperty(self, name, value, moving=None):
        super(Commentable, self).delfromproperty(name, value, moving)
        if name == 'comments':
            channel = getattr(self, 'channel', self)
            channel.len_comments -= 1
            if self is not channel:
                self.len_comments -= 1


@content(
    'channel',
    icon='icon novaideo-icon icon-idea',
    )
@implementer(IChannel)
class Channel(Commentable):
    """Channel class"""

    type_title = _('Channel')
    icon = 'icon novaideo-icon icon-idea'
    templates = {'default': 'novaideo:views/templates/channel_result.pt'}
    name = renamer()
    members = SharedMultipleProperty('members', 'following_channels')
    subject = SharedUniqueProperty('subject', 'channels')

    def __init__(self, **kwargs):
        super(Channel, self).__init__(**kwargs)
        self.set_data(kwargs)

    def get_subject(self, user=None):
        subject = self.subject
        return subject if subject else getattr(self, '__parent__', None)

    def get_title(self, user=None):
        title = getattr(self, 'title', '')
        if not title:
            return getattr(self.get_subject(user), 'title', None)

        return title

    def is_discuss(self):
        return self.subject.__class__.__name__.lower() == 'person'


@content(
    'privatechannel',
    icon='icon novaideo-icon icon-idea',
    )
@implementer(IPrivateChannel)
class PrivateChannel(Channel):
    """Channel class"""

    def __init__(self, **kwargs):
        super(PrivateChannel, self).__init__(**kwargs)
        self.set_data(kwargs)

    def get_subject(self, user=None):
        subject = None
        for member in self.members:
            if member is not user:
                subject = member
                break

        return subject if subject else getattr(self, '__parent__', None)

    def get_title(self, user=None):
        title = getattr(self, 'title', '')
        if not title:
            return getattr(self.get_subject(user), 'title', None)

        return title


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
class SearchableEntity(VisualisableElement, Entity):
    """ A Searchable entity is an entity that can be searched"""

    templates = {'default': 'novaideo:templates/views/default_result.pt',
                 'bloc': 'novaideo:templates/views/default_result.pt'}
    channels = CompositeMultipleProperty('channels', 'subject')
    comments = CompositeMultipleProperty('comments')

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

    @property
    def channel(self):
        channels = getattr(self, 'channels', [])
        return channels[0] if channels else None

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
    def len_contacted(self):
        return len(self._email_persons_contacted)

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


@implementer(INode)
class Node(Entity):

    def __init__(self, **kwargs):
        super(Node, self).__init__(**kwargs)
        self.graph = PersistentDict()

    def get_node_id(self):
        return str(self.__oid__).replace('-', '_')

    def init_graph(self, calculated=[]):
        result = self.get_nodes_data()
        self.graph = PersistentDict(result[0])
        oid = self.get_node_id()
        newcalculated = list(calculated)
        newcalculated.append(oid)
        for node in self.graph:
            if node not in newcalculated:
                node_obj = get_obj(self.graph[node]['oid'])
                if node_obj:
                    graph, newcalculated = node_obj.init_graph(
                        newcalculated)

        return self.graph, newcalculated

    def get_nodes_data(self, calculated=[]):
        pass


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
