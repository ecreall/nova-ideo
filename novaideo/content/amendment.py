import colander
import deform
from zope.interface import implementer
from pyramid.threadlocal import get_current_request

from substanced.interfaces import IUserLocator
from substanced.principal import DefaultUserLocator
from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import getSite
from dace.objectofcollaboration.principal.util import get_current
from dace.descriptors import (
    CompositeMultipleProperty,
    SharedUniqueProperty,
    SharedMultipleProperty
)
from pontus.widget import RichTextWidget,Select2Widget, CheckboxChoiceWidget, Length
from pontus.core import VisualisableElementSchema
from pontus.schema import Schema
from pontus.file import Object as ObjectType

from .interface import IAmendment
from novaideo.core import (
    SearchableEntity,
    SearchableEntitySchema,
    CorrelableEntity,
    Commentable,
    PresentableEntity,
    DuplicableEntity,
    can_access)
from novaideo import _
from novaideo.views.widget import ConfirmationWidget, Select2WidgetSearch
from novaideo.content.idea import Idea


@colander.deferred
def intention_choice(node, kw):
    root = getSite()
    intentions = sorted(root.idea_intentions)
    values = [(i, i) for i in intentions ]
    values.insert(0, ('', '- Select -'))
    return Select2Widget(values=values)


@colander.deferred
def replaced_idea_choice(node, kw):
    context = node.bindings['context']
    root = getSite()
    user = get_current()
    ideas = [i for i in context.related_ideas if can_access(user, i)]
    values = [(i, i.title) for i in ideas]
    return Select2Widget(values=values)



@colander.deferred
def idea_replacement_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite()
    user = get_current()
    _ideas = list(user.ideas)
    _ideas.extend([ i for i in user.selections if isinstance(i, Idea)])
    ideas = [i for i in _ideas if can_access(user, i)]
    values = [(i, i.title) for i in ideas]
    return Select2Widget(values=values)


@colander.deferred
def ideas_choice(node, kw):
    root = getSite()
    user = get_current()
    ideas = [i for i in root.ideas if can_access(user, i) and not('deprecated' in i.state)]
    values = [(i, i.title) for i in ideas]
    return Select2Widget(values=values, multiple=True)


def context_is_a_amendment(context, request):
    return request.registry.content.istype(context, 'amendment')


class AmendmentSchema(VisualisableElementSchema, SearchableEntitySchema):

    name = NameSchemaNode(
        editing=context_is_a_amendment,
        )

    text = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget()
        )

    related_ideas = colander.SchemaNode(
        colander.Set(),
        widget=ideas_choice,
        title=_('Related ideas'),
        validator=Length(_, min=1), #TODO message
        default=[],
        )

    replaced_idea = colander.SchemaNode(
            ObjectType(),
            widget=replaced_idea_choice,
            title=_('Replaced idea'),
            missing=[]
        )

    ideas_of_replacement = colander.SchemaNode(
            ObjectType(),
            widget=idea_replacement_choice,
            title=_('Idea of replacement'),
            missing=[],
        )


@content(
    'amendment',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IAmendment)
class Amendment(Commentable, CorrelableEntity, SearchableEntity, DuplicableEntity, PresentableEntity):
    name = renamer()
    result_template = 'novaideo:views/templates/amendment_result.pt'
    author = SharedUniqueProperty('author')
    proposal = SharedUniqueProperty('proposal', 'amendments')
    replaced_idea = SharedUniqueProperty('replaced_idea', isunique=True)
    idea_of_replacement = SharedUniqueProperty('idea_of_replacement', isunique=True)
    related_ideas = SharedMultipleProperty('related_ideas', isunique=True)

    def __init__(self, **kwargs):
        super(Amendment, self).__init__(**kwargs)
        self.set_data(kwargs)
