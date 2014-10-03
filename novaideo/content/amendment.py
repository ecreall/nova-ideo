import colander
import deform
from zope.interface import implementer
from pyramid.threadlocal import get_current_request
from persistent.dict import PersistentDict

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
from pontus.widget import RichTextWidget, Select2Widget, CheckboxChoiceWidget, Length, SimpleMappingWidget
from pontus.core import VisualisableElementSchema
from pontus.schema import Schema, select
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
from novaideo.content.idea import Idea, IdeaSchema



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
        description=_('The object of your intention (300 caracteres maximum).'),
        validator=colander.Length(max=300),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        )


class NewIdeaSchema(Schema):

    new_idea = select(IdeaSchema(factory=Idea, 
                                 editable=True,
                                 omit=['keywords'], 
                                 widget=SimpleMappingWidget(item_css_class='hide-bloc new-idea-form')),
                      ['title',
                       'description',
                       'keywords'])


class Intention(object):
    intention_id = NotImplemented
    title = NotImplemented
    schema = NotImplemented

    @classmethod
    def get_intention(cls, view):
        result = {}
        schemainstance = cls.schema()
        parameters = [ c.name for c in schemainstance.children if c.name != '_csrf_token_']
        for param in parameters:
            result[param] = view.params(param)

        result['id'] = cls.intention_id
        return result

    @classmethod
    def get_explanation_dict(cls, args):
        result = {}
        schemainstance = cls.schema()
        parameters = [ c.name for c in schemainstance.children if c.name != '_csrf_token_']
        for (k, value) in args.items():
            if k in parameters:
                try:
                    if isinstance(value, list):
                        listvalue = []
                        for v in value:
                            listvalue.append(get_oid(v))

                        result[k] = listvalue
                    else:
                        result[k] = get_oid(value)
                except Exception:
                    result[k] = value

        return result

    @classmethod
    def get_explanation_data(cls, args):
        result = {}
        schemainstance = cls.schema()
        parameters = [ c.name for c in schemainstance.children if c.name != '_csrf_token_']
        for (k, value) in args.items():
            if k in parameters:
                try:
                    if isinstance(value, list):
                        listvalue = []
                        for v in value:
                            obj = get_obj(int(v))
                            if obj is None:
                                raise Exception()
 
                            listvalue.append(obj)

                        result[k] = listvalue

                    else:
                        obj = get_obj(int(value))
                        if obj is None:
                            raise Exception()
                       
                        result[k] = obj

                except Exception:
                    result[k] = value

        return result


class RemoveIdeasSchema(IntentionItemSchema):

    ideas = colander.SchemaNode(
        colander.Set(),
        widget=idea_choice,
        title=_('Ideas to remove'),
        description=_('Choose ideas to remove.'),
        validator=Length(_, min=1), #TODO message
        default=[],
        )


class RemoveIdeas(Intention):
    intention_id = "removeideas"
    title = "Remove ideas"
    schema = RemoveIdeasSchema


class AddIdeasSchema(IntentionItemSchema):

    ideas = colander.SchemaNode(
        colander.Set(),
        widget=idea_choice,
        title=_('Ideas to add'),
        description=_('Choose ideas to add.'),
        validator=Length(_, min=1), #TODO message
        default=[],
        )


class AddIdeas(Intention):
    intention_id = "addideas"
    title = "Add ideas"
    schema = AddIdeasSchema


class CompleteIdeasSchema(IntentionItemSchema):

    ideas = colander.SchemaNode(
        colander.Set(),
        widget=idea_choice,
        title=_('Ideas to complete'),
        description=_('Choose ideas to complete.'),
        validator=Length(_, min=1), #TODO message
        default=[],
        )


class CompleteIdeas(Intention):
    intention_id = "completeideas"
    title = "Complete ideas"
    schema = CompleteIdeasSchema


@colander.deferred
def replacedideas_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite()
    user = get_current()
    ideas = [i for i in context.proposal.related_ideas if can_access(user, i)]
    values = [(i, i.title) for i in ideas]
    values.insert(0, ('', '- Select -'))
    return Select2WidgetSearch(multiple= True, 
                               values=values,
                               item_css_class='search-idea-form search-idea-bloc col-md-6',
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
    return Select2WidgetSearch(multiple= True, 
                               values=values, 
                               item_css_class='search-idea-form search-idea-bloc col-md-6',
                               url=request.resource_url(root, '@@search', query={'op':'toselect', 'content_types':['Idea']}))


class ReplaceIdeasSchema(IntentionItemSchema):

    replacedideas = colander.SchemaNode(
        colander.Set(),
        widget=replacedideas_choice,
        title=_('Replaced ideas'),
        description=_('Choose ideas to replace.'),
        validator=Length(_, min=1), #TODO message
        default=[],
        )

    ideasofreplacement = colander.SchemaNode(
        colander.Set(),
        widget=ideasofreplacement_choice,
        title=_('Ideas of replacement'),
        description=_('Choose ideas of replacement.'),
        validator=Length(_, min=1), #TODO message
        default=[],
        )


class ReplaceIdeas(Intention):
    intention_id = "replaceideas"
    title = "Replace ideas"
    schema = ReplaceIdeasSchema


class CompleteText(Intention):
    intention_id = "completetext"
    title = "Complete text"
    schema = IntentionItemSchema


explanation_intentions = {RemoveIdeas.intention_id: RemoveIdeas, 
                          AddIdeas.intention_id: AddIdeas, 
                          CompleteIdeas.intention_id: CompleteIdeas, 
                          ReplaceIdeas.intention_id: ReplaceIdeas, 
                          CompleteText.intention_id: CompleteText}


@colander.deferred
def intention_choice(node, kw):
    root = getSite()
    values = [(i.intention_id, i.title) for i in explanation_intentions.values()]
    values = sorted(values, key=lambda e: e[1])
    values.insert(0, ('', '- Select -'))
    return Select2Widget(values=values, css_class="explanation-intention")


class RelatedExplanationSchema(Schema):

    relatedexplanation = colander.SchemaNode(
        colander.Integer(),
        title=_('Apply the same intention'),
        description=_('Choose the intention to apply'),
        missing=None
        )

class NewIntentionSchema(Schema):

    intention = colander.SchemaNode(
        colander.String(),
        widget=intention_choice,
        title=_('Intention'),
        description=_('Choose your intention.'),
        )


class IntentionSchema(Schema):

    relatedexplanation = RelatedExplanationSchema(widget=SimpleMappingWidget())

    intention = NewIntentionSchema(widget=SimpleMappingWidget(item_css_class="intention-bloc"))


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
        self.explanations = PersistentDict()
        self.set_data(kwargs)

