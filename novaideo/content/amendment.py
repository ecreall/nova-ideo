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
from pontus.widget import RichTextWidget,Select2Widget
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
    can_access)
from novaideo import _
from novaideo.views.widget import ConfirmationWidget


@colander.deferred
def intention_choice(node, kw):
    root = getSite()
    intentions = sorted(root.idea_intentions)
    values = [(i, i) for i in intentions ]
    values.insert(0, ('', '- Select -'))
    return Select2Widget(values=values)

def context_is_a_amendment(context, request):
    return request.registry.content.istype(context, 'amendment')


@colander.deferred
def replaced_ideas_choice(node, kw):
    context = node.bindings['context']
    root = getSite()
    user = get_current()
    ideas = [i for i in context.related_ideas if can_access(user, i)]
    values = [(i, i.title) for i in ideas]
    values.insert(0, ('', '- Select -'))
    return Select2Widget(values=values)


class ReplacedIdeaSchema(Schema):

    replaced_idea = colander.SchemaNode(
            ObjectType(),
            widget=replaced_ideas_choice,
            title=_('Replaced ideas'),
            missing=None,
            description=_('Choose the replaced idea')
        )

    not_identified =  colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Idea not identified'),
        title =_(''),
        missing=False
        )


@colander.deferred
def ideas_replacement_choice(node, kw):
    root = getSite()
    user = get_current()
    ideas = [i for i in root.ideas if can_access(user, i)]
    values = [(i, i.title) for i in ideas]
    values.insert(0, ('', '- Select -'))
    return Select2Widget(values=values)


class IdeaOfReplacementSchema(Schema):

    idea_of_replacement = colander.SchemaNode(
            ObjectType(),
            widget=ideas_replacement_choice,
            title=_('Idea of replacement'),
            missing=None,
            description=_('Choose the idea of replacement')
        )

    new_idea =  colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Creat a new idea'),
        title =_(''),
        missing=False
        )

class AmendmentConfirmationSchema(Schema):

    intention = colander.SchemaNode(
        colander.String(),
        widget=intention_choice,
        title=_('Intention'),
        )

    comment = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=500),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        )

    replaced_idea = ReplacedIdeaSchema(widget=deform.widget.MappingWidget())

    idea_of_replacement = IdeaOfReplacementSchema(widget=deform.widget.MappingWidget())


class AmendmentSchema(VisualisableElementSchema, SearchableEntitySchema):

    name = NameSchemaNode(
        editing=context_is_a_amendment,
        )

    text = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget()
        )

    confirmation = AmendmentConfirmationSchema(widget=ConfirmationWidget(css_class='confirmation'))



@content(
    'amendment',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IAmendment)
class Amendment(Commentable, CorrelableEntity, SearchableEntity, PresentableEntity):
    name = renamer()
    author = SharedUniqueProperty('author')
    proposal = SharedUniqueProperty('proposal', 'amendments')
    replaced_idea = SharedUniqueProperty('replaced_idea')
    idea_of_replacement = SharedUniqueProperty('idea_of_replacement')

    def __init__(self, **kwargs):
        super(Amendment, self).__init__(**kwargs)
        self.set_data(kwargs)
