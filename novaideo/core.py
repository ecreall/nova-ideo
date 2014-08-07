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
from dace.descriptors import SharedMultipleProperty
from pontus.widget import Select2Widget
from pontus.schema import Schema
from pontus.file import Object as ObjectType
from pontus.core import VisualisableElement
from pontus.widget import SequenceWidget

from novaideo import _
from novaideo.content.interface import (
    ISerchableEntity,
    IVersionableEntity,
    IDuplicableEntity,
    ISerchableEntity,
    ICommentabl)



@implementer(ICommentabl)
class Commentabl(VisualisableElement, Entity):
    name = renamer()
    comments = CompositeMultipleProperty('comments')

    def __init__(self, **kwargs):
        super(Commentabl, self).__init__(**kwargs)


@implementer(IVersionableEntity)
class VersionableEntity(Entity):

    version = CompositeUniqueProperty('version', 'nextversion')
    nextversion = SharedUniqueProperty('nextversion', 'version')

    def __init__(self, **kwargs):
        super(VersionableEntity, self).__init__(**kwargs)

    @property
    def current_version(self):
        if self.newtversion is None:
            return self
        else:
            return self.nextversion.current_version

    @property
    def history(self):
        return allSubobjectsOfKind(interface=IVersionableEntity)


@implementer(IDuplicableEntity)
class DuplicableEntity(Entity):

    originalideas = SharedMultipleProperty('originalideas')

    def __init__(self, **kwargs):
        super(DuplicableEntity, self).__init__(**kwargs)


@colander.deferred
def keywords_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = []
    root = getSite()
    prop = sorted(root.keywords, key=lambda p: p.title)
    values = [i.title for i in prop]
    return deform.widget.AutocompleteInputWidget(values=values)


@colander.deferred
def default_keywords_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite()
    if context is root:
        return []

    values = sorted(context.keywords)
    return values


class SerchableEntitySchema(Schema):

    keywords =  colander.SchemaNode(
                    colander.Sequence(),
                    colander.SchemaNode(
                         colander.String(),
                         widget=keywords_choice,
                         name='keyword'),
                default=default_keywords_choice,
                title=_('Keywords')
                )



@implementer(ISerchableEntity)
class SerchableEntity(Entity):
    result_template = 'novaideo:templates/views/default_result.pt'    
    keywords_ref = SharedMultipleProperty('keywords_ref', 'referenced_elements')

    def __init__(self, **kwargs):
        super(SerchableEntity, self).__init__(**kwargs)

    def setkeywords(self, keywords):
        self.setproperty('keywords', keywords)

    @property
    def keywords(self):
        return [k.title for k in self.keywords_ref]
