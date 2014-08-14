import colander
import deform.widget
from zope.interface import implementer

from substanced.util import renamer

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import (
    SharedUniqueProperty,
    CompositeUniqueProperty,
    SharedMultipleProperty,
    CompositeMultipleProperty)
from dace.util import getSite, allSubobjectsOfKind
from pontus.schema import Schema
from pontus.core import VisualisableElement
from pontus.widget import SequenceWidget

from novaideo import _
from novaideo.content.interface import (
    IVersionableEntity,
    IDuplicableEntity,
    ISearchableEntity,
    ICommentable,
    ICorrelableEntity)


BATCH_DEFAULT_SIZE = 5


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

    originalideas = SharedMultipleProperty('originalideas')


@colander.deferred
def keywords_choice(node, kw):
    values = []
    root = getSite()
    prop = sorted(root.keywords, key=lambda p: p.title)
    values = [i.title for i in prop]
    return deform.widget.AutocompleteInputWidget(values=values)


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
        colander.Sequence(),
        colander.SchemaNode(
             colander.String(),
             widget=keywords_choice,
             name='keyword'),
        default=default_keywords_choice,
        widget=SequenceWidget(max_len=5, min_len=1),
        title=_('Keywords'),
        )


@implementer(ISearchableEntity)
class SearchableEntity(Entity):
    result_template = 'novaideo:templates/views/default_result.pt'
    keywords_ref = SharedMultipleProperty('keywords_ref', 'referenced_elements')

    @property
    def keywords(self):
        return [k.title for k in self.keywords_ref]


@implementer(ICorrelableEntity)
class CorrelableEntity(Entity):
    source_correlations = SharedMultipleProperty('source_correlations', 'source')
    target_correlations = SharedMultipleProperty('target_correlations', 'target')

    @property
    def correlations(self):
        result = [c.target for c in self.source_correlations]
        result.extend([c.source for c in self.target_correlations])
        return list(set(result))
