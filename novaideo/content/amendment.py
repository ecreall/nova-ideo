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
from pontus.widget import RichTextWidget,Select2Widget, CheckboxChoiceWidget
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

def context_is_a_amendment(context, request):
    return request.registry.content.istype(context, 'amendment')


@colander.deferred
def replaced_ideas_choice(node, kw):
    context = node.bindings['context']
    root = getSite()
    user = get_current()
    ideas = [i for i in context.related_ideas if can_access(user, i)]
    values = [(i, i.title) for i in ideas]
    return Select2Widget(values=values, multiple=True)


class ReplacedIdeasSchema(Schema):

    replaced_ideas = colander.SchemaNode(
            colander.Set(),
            widget=replaced_ideas_choice,
            title=_('Replaced ideas'),
            missing=[]
        )


@colander.deferred
def ideas_replacement_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite()
    user = get_current()
    _ideas = list(user.ideas)
    _ideas.extend([ i for i in user.selections if isinstance(i, Idea)])
    ideas = [i for i in _ideas if can_access(user, i)]
    values = [(i, i.title) for i in ideas]
    return Select2Widget(values=values, multiple=True)



class IdeasOfReplacementSchema(Schema):

    ideas_of_replacement = colander.SchemaNode(
            colander.Set(),
            widget=ideas_replacement_choice,
            title=_('Ideas of replacement'),
            missing=[],
        )


class AmendmentIdeaManagmentSchema(Schema):

    replaced_ideas = ReplacedIdeasSchema(widget=deform.widget.MappingWidget(mapping_css_class='col-md-6 col-bloc'))

    ideas_of_replacement = IdeasOfReplacementSchema(widget=deform.widget.MappingWidget(mapping_css_class='col-md-6 col-bloc'))


class AmendmentSchema(VisualisableElementSchema, SearchableEntitySchema):

    name = NameSchemaNode(
        editing=context_is_a_amendment,
        )

    text = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget()
        )

    ideas = AmendmentIdeaManagmentSchema(widget=deform.widget.MappingWidget(mapping_css_class='row hide-bloc'))



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
    replaced_ideas = SharedMultipleProperty('replaced_ideas', isunique=True)
    ideas_of_replacement = SharedMultipleProperty('ideas_of_replacement', isunique=True)

    def __init__(self, **kwargs):
        super(Amendment, self).__init__(**kwargs)
        self.set_data(kwargs)
