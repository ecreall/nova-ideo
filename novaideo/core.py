import colander
import venusian
import deform.widget
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
from dace.util import getSite, allSubobjectsOfKind, acces_validation
from pontus.schema import Schema
from pontus.core import VisualisableElement
from pontus.widget import SequenceWidget, Select2WidgetCreateSearchChoice

from novaideo import _
from novaideo.content.interface import (
    IVersionableEntity,
    IDuplicableEntity,
    ISearchableEntity,
    ICommentable,
    ICorrelableEntity,
    IPresentableEntity)



BATCH_DEFAULT_SIZE = 5


novaideo_acces_actions = {}


class acces_action(object):

    def __call__(self, wrapped):
        def callback(scanner, name, ob):
            if ob.context in novaideo_acces_actions:
                novaideo_acces_actions[ob.context].append(ob)
            else: 
                novaideo_acces_actions[ob.context] = [ob]
 
        venusian.attach(wrapped, callback)
        return wrapped


def can_access(user, context, request=None, root=None):
    declared = context.__provides__.declared[0]
    if declared in novaideo_acces_actions:
        for action in novaideo_acces_actions[declared]:
            if action.processsecurity_validation(None, context):
                return True

    return False


@implementer(ICommentable)
class Commentable(VisualisableElement, Entity):
    name = renamer()
    comments = CompositeMultipleProperty('comments')


@implementer(IVersionableEntity)
class VersionableEntity(Entity):

    version = CompositeUniqueProperty('version', 'nextversion')
    nextversion = SharedUniqueProperty('nextversion', 'version')

    @property
    def current_version(self):
        if self.nextversion is None:
            return self
        else:
            return self.nextversion.current_version

    @property
    def history(self):
        result = []
        if self.version is None:
            return [self]
        else:
            result.append(self)
            result.extend(self.version.history)

        return result


@implementer(IDuplicableEntity)
class DuplicableEntity(Entity):

    originalentity = SharedUniqueProperty('originalentity')#('originalentity', 'children')
    #TODO children = = SharedMultipleProperty('children', 'originalentity')

@colander.deferred
def keywords_choice(node, kw):
    values = []
    root = getSite()
    prop = sorted(root.keywords, key=lambda p: p.title)
    values = [(i.title, i.title) for i in prop]
    return Select2WidgetCreateSearchChoice(max_len=5, values=values, multiple=True)


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
    result_template = 'novaideo:templates/views/default_result.pt'
    keywords_ref = SharedMultipleProperty('keywords_ref', 'referenced_elements')

    @property
    def keywords(self):
        return [k.title for k in self.keywords_ref]


@implementer(IPresentableEntity)
class PresentableEntity(Entity):


    def __init__(self, **kwargs):
        super(PresentableEntity, self).__init__(**kwargs)
        self.email_persons_contacted = PersistentList()

    @property
    def persons_contacted(self):
        request = get_current_request()
        adapter = request.registry.queryMultiAdapter(
                (self, request),
                IUserLocator
                )
        if adapter is None:
            adapter = DefaultUserLocator(self, request)

        result = []
        for email in self.email_persons_contacted:
            user = adapter.get_user_by_email(email)
            if user is not None:
                result.append(user)
            else:
                result.append(email)

        return set(result)


@implementer(ICorrelableEntity)
class CorrelableEntity(Entity):
    source_correlations = SharedMultipleProperty('source_correlations', 'source')
    target_correlations = SharedMultipleProperty('target_correlations', 'target')

    @property
    def correlations(self):
        result = [c.target for c in self.source_correlations]
        result.extend([c.source for c in self.target_correlations])
        return list(set(result))
