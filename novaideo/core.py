
import colander
import venusian
from persistent.list import PersistentList
from zope.interface import implementer
from pyramid.threadlocal import get_current_request

from substanced.interfaces import IUserLocator
from substanced.principal import DefaultUserLocator
from substanced.util import renamer

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import (
    SharedUniqueProperty,
    CompositeUniqueProperty,
    SharedMultipleProperty,
    CompositeMultipleProperty)
from dace.util import getSite
from pontus.schema import Schema
from pontus.core import VisualisableElement
from pontus.widget import Select2WidgetCreateSearchChoice

from novaideo import _
from novaideo.content.interface import (
    IVersionableEntity,
    IDuplicableEntity,
    ISearchableEntity,
    ICommentable,
    ICorrelableEntity,
    IPresentableEntity)



BATCH_DEFAULT_SIZE = 100


NOVAIDO_ACCES_ACTIONS = {}


class acces_action(object):
    """ Decorator for novaideo access actions. 
    An access action allows to view an object"""

    def __call__(self, wrapped):
        def callback(scanner, name, ob):
            if ob.context in NOVAIDO_ACCES_ACTIONS:
                NOVAIDO_ACCES_ACTIONS[ob.context].append(ob)
            else: 
                NOVAIDO_ACCES_ACTIONS[ob.context] = [ob]
 
        venusian.attach(wrapped, callback)
        return wrapped


def can_access(user, context, request=None, root=None):
    """ Return 'True' if the user can access to the context"""

    declared = context.__provides__.declared[0]
    if declared in NOVAIDO_ACCES_ACTIONS:
        return any(action.processsecurity_validation(None, context) \
                   for action in NOVAIDO_ACCES_ACTIONS[declared])

    return False


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


@implementer(IDuplicableEntity)
class DuplicableEntity(Entity):
    """ A Duplicable entity is an entity that can be duplicated"""

    originalentity = SharedUniqueProperty('originalentity')


@colander.deferred
def keywords_choice(node, kw):
    values = []
    root = getSite()
    prop = sorted(root.keywords, key=lambda p: p.title)
    values = [(i.title, i.title) for i in prop]
    return Select2WidgetCreateSearchChoice(max_len=5,
                                           values=values,
                                           multiple=True)


@colander.deferred
def default_keywords_choice(node, kw):
    context = node.bindings['context']
    root = getSite()
    if context is root:
        return []

    values = sorted(context.keywords)
    return values


class SearchableEntitySchema(Schema):

    keywords =  colander.SchemaNode(
        colander.Set(),
        default=default_keywords_choice,
        widget=keywords_choice,
        title=_('Keywords'),
        )


@implementer(ISearchableEntity)
class SearchableEntity(Entity):
    """ A Searchable entity is an entity that can be searched"""

    result_template = 'novaideo:templates/views/default_result.pt'
    keywords_ref = SharedMultipleProperty('keywords_ref', 'referenced_elements')

    @property
    def keywords(self):
        return [k.title for k in self.keywords_ref]


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
                result.append(email)

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
                                                 'target')

    @property
    def correlations(self):
        """Return all source correlations and target correlations"""

        result = [c.target for c in self.source_correlations]
        result.extend([c.source for c in self.target_correlations])
        return list(set(result))
