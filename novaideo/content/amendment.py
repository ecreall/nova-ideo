import colander
import deform
from zope.interface import implementer
from pyramid.threadlocal import get_current_request

from substanced.interfaces import IUserLocator
from substanced.principal import DefaultUserLocator
from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer, get_oid

from dace.util import getSite, get_obj
from dace.objectofcollaboration.principal.util import get_current
from dace.descriptors import (
    CompositeMultipleProperty,
    SharedUniqueProperty,
    SharedMultipleProperty
)
from pontus.widget import RichTextWidget,Select2Widget, CheckboxChoiceWidget, Length, SimpleMappingWidget
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
def idea_choice(node, kw):
     context = node.bindings['context']
     request = node.bindings['request']
     root = getSite()
     user = get_current()
     _ideas = list(user.ideas)
     _ideas.extend([ i for i in user.selections if isinstance(i, Idea)])
     _ideas = set(_ideas) 
     ideas = [i for i in _ideas if can_access(user, i) and not('deprecated' in i.state)]
     values = [(i, i.title) for i in ideas]
     values.insert(0, ('', '- Select -'))
     return Select2WidgetSearch(multiple= True, values=values, item_css_class='search-idea-form',
                                url=request.resource_url(root, '@@search', query={'op':'toselect', 'content_types':['Idea']}))


class IntentionItemSchema(Schema):

    comment = colander.SchemaNode(
        colander.String(),
        title= _('Object'),
        validator=colander.Length(max=2000),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        )

class Intention(object):
    intention_id = NotImplemented
    title = NotImplemented
    schema = NotImplemented
    parameters = []

    @classmethod
    def get_explanation_dict(cls, **args):
        result = {}
        for (k, value) in args.items():
            if k in cls.parameters:
                try:
                    result[k] = get_oid(value)
                except Exception:
                    result[K] = value

        return result

    @classmethod
    def get_explanation_data(cls, **args):
        result = {}
        for (k, value) in args.items():
            if k in cls.parameters:
                try:
                    result[k] = get_obj(value)
                except Exception:
                    result[K] = value

        return result


class RemoveIdeasSchema(IntentionItemSchema):

    ideas = colander.SchemaNode(
        colander.Set(),
        widget=idea_choice,
        title=_('Preciser les idees'),
        validator=Length(_, min=1), #TODO message
        default=[],
        )


class RemoveIdeas(Intention):
    itention_id = "removeideas"
    title = "Remove ideas"
    schema = RemoveIdeasSchema()
    parameters = ['ideas']


class AddIdeasSchema(IntentionItemSchema):

    ideas = colander.SchemaNode(
        colander.Set(),
        widget=idea_choice,
        title=_('Ajouter des idees'),
        validator=Length(_, min=1), #TODO message
        default=[],
        )


class AddIdeas(Intention):
    itention_id = "addideas"
    title = "Add ideas"
    schema = AddIdeasSchema()
    parameters = ['ideas']


class CompleteIdeasSchema(IntentionItemSchema):

    ideas = colander.SchemaNode(
        colander.Set(),
        widget=idea_choice,
        title=_('Completer les idees'),
        validator=Length(_, min=1), #TODO message
        default=[],
        )


class CompleteIdeas(Intention):
    itention_id = "completeideas"
    title = "Complete ideas"
    schema = CompleteIdeasSchema()
    parameters = ['ideas']


@colander.deferred
def replacedideas_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite()
    user = get_current()
    ideas = [i for i in context.proposal.related_ideas if can_access(user, i)]
    values = [(i, i.title) for i in ideas]
    values.insert(0, ('', '- Select -'))
    return Select2WidgetSearch(multiple= True, values=values, item_css_class='search-idea-form',
                                url=request.resource_url(root, '@@search', query={'op':'toselect', 'content_types':['Idea']}))


@colander.deferred
def ideasofreplacement_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite()
    user = get_current()
    _ideas = list(user.ideas)
    _ideas.extend([ i for i in user.selections if isinstance(i, Idea)])
    _ideas = set(_ideas) 
    ideas = [i for i in _ideas if can_access(user, i) and not('deprecated' in i.state)]
    values = [(i, i.title) for i in ideas]
    values.insert(0, ('', '- Select -'))
    return Select2WidgetSearch(multiple= True, values=values, item_css_class='search-idea-form',
                                url=request.resource_url(root, '@@search', query={'op':'toselect', 'content_types':['Idea']}))


class ReplaceIdeasSchema(IntentionItemSchema):

    replacedideas = colander.SchemaNode(
        colander.Set(),
        widget=replacedideas_choice,
        title=_('Replaced ideas'),
        validator=Length(_, min=1), #TODO message
        default=[],
        )

    ideasofreplacement = colander.SchemaNode(
        colander.Set(),
        widget=ideasofreplacement_choice,
        title=_('Ideas of replacement'),
        validator=Length(_, min=1), #TODO message
        default=[],
        )


class ReplaceIdeas(Intention):
    itention_id = "replaceideas"
    title = "Replace ideas"
    schema = ReplaceIdeasSchema()
    parameters = ['replacedideas', 'ideasofreplacement']


class CompleteText(Intention):
    itention_id = "completetext"
    title = "Complete text"
    schema = IntentionItemSchema()
    parameters = []


explanation_intentions = {RemoveIdeas.itention_id: RemoveIdeas, 
                          AddIdeas.itention_id: AddIdeas, 
                          CompleteIdeas.itention_id: CompleteIdeas, 
                          ReplaceIdeas.itention_id: ReplaceIdeas, 
                          CompleteText.itention_id: CompleteText}


@colander.deferred
def intention_choice(node, kw):
    root = getSite()
    values = [(i.itention_id, i.title) for i in explanation_intentions.values()]
    values.insert(0, ('', '- Select -'))
    return Select2Widget(values=values, css_class="explanation-intention")


class IntentionSchema(Schema):

    relatedexplanation = colander.SchemaNode(
        colander.Integer(),
        title=_('Appliquer l in tention de la modification'),
        missing=None
        )

    intention = colander.SchemaNode(
        colander.String(),
        widget=intention_choice,
        title=_('Intention'),
        )

    remove = RemoveIdeasSchema(widget=SimpleMappingWidget(item_css_class="removeideas-intention form-intention hide-bloc"))

    add = AddIdeasSchema(widget=SimpleMappingWidget(item_css_class="addideas-intention form-intention hide-bloc"))

    complete = CompleteIdeasSchema(widget=SimpleMappingWidget(item_css_class="completeideas-intention form-intention hide-bloc"))

    replaced = ReplaceIdeasSchema(widget=SimpleMappingWidget(item_css_class="replaceideas-intention form-intention hide-bloc"))

    completetext = IntentionItemSchema(widget=SimpleMappingWidget(item_css_class="completetext-intention form-intention hide-bloc"))


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
    replaced_idea = SharedMultipleProperty('replaced_ideas', isunique=True)
    idea_of_replacement = SharedMultipleProperty('ideas_of_replacement', isunique=True)

    def __init__(self, **kwargs):
        super(Amendment, self).__init__(**kwargs)
        self.explanations = {}
        self.set_data(kwargs)

