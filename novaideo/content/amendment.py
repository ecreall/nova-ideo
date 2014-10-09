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
from pontus.schema import Schema, select, omit
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
from novaideo.views.widget import ConfirmationWidget, Select2WidgetSearch, AddIdeaWidget
from novaideo.content.idea import Idea, IdeaSchema
from novaideo.cache import region



@colander.deferred
def idea_choice(node, kw):
     context = node.bindings['context']
     request = node.bindings['request']
     _used_ideas = context.get_used_ideas()
     root = getSite()
     user = get_current()
     _ideas = list(user.ideas)
     _ideas.extend([ i for i in user.selections if isinstance(i, Idea)])
     _ideas.extend(_used_ideas)
     _ideas = set(_ideas) 
     ideas = [i for i in _ideas if can_access(user, i) and not('deprecated' in i.state)]
     values = [(i, i.title) for i in ideas]
     values.insert(0, ('', '- Select -'))
     return Select2WidgetSearch(multiple= True, values=values, item_css_class='search-idea-form',
                                url=request.resource_url(root, '@@search', query={'op':'toselect', 'content_types':['Idea']}))

@colander.deferred
def add_new_idea_widget(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite()
    url = request.resource_url(root, '@@ideasmanagement')
    return AddIdeaWidget(url=url, item_css_class='new-idea-form hide-bloc')
    

@colander.deferred
def replacedideas_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    _used_ideas = context.get_used_ideas()
    root = getSite()
    user = get_current()
    ideas = list(context.proposal.related_ideas)
    ideas.extend(_used_ideas)
    ideas = set(ideas)
    ideas = [i for i in ideas if can_access(user, i)]
    values = [(i, i.title) for i in ideas]
    values.insert(0, ('', '- Select -'))
    return Select2WidgetSearch(multiple= True, 
                               values=values,
                               item_css_class='search-idea-form',
                               url=request.resource_url(root, '@@search', query={'op':'toselect', 'content_types':['Idea']}))


@colander.deferred
def ideasofreplacement_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    _used_ideas = context.get_used_ideas()
    root = getSite()
    user = get_current()
    _ideas = list(user.ideas)
    _ideas.extend([ i for i in user.selections if isinstance(i, Idea)])
    _ideas.extend(_used_ideas)
    _ideas = set(_ideas) 
    ideas = [i for i in _ideas if can_access(user, i) and not('deprecated' in i.state)]
    values = [(i, i.title) for i in ideas]
    values.insert(0, ('', '- Select -'))
    return Select2WidgetSearch(multiple= True, 
                               values=values, 
                               item_css_class='search-idea-form',
                               url=request.resource_url(root, '@@search', query={'op':'toselect', 'content_types':['Idea']}))


class RelatedExplanationSchema(Schema):

    relatedexplanation = colander.SchemaNode(
        colander.Integer(),
        title=_('Apply the same intention'),
        description=_('Choose the intention to apply'),
        missing=None
        )


class NewIdeaSchema(Schema):

    new_idea = select(IdeaSchema(factory=Idea, 
                                 editable=True,
                                 omit=['keywords'], 
                                 widget=SimpleMappingWidget()),
                      ['title',
                       'description',
                       'keywords'])


class IdeasRowSchema(Schema):

    removed_ideas = colander.SchemaNode(
        colander.Set(),
        widget=replacedideas_choice,
        title=_('Removed ideas'),
        description=_('Choose ideas to remove.'),
        missing=[],
        default=[],
        )

    edited_ideas = colander.SchemaNode(
        colander.Set(),
        widget=replacedideas_choice,
        title=_('Edited ideas'),
        description=_('Choose ideas to edit.'),
        missing=[],
        default=[],
        )

    added_ideas = colander.SchemaNode(
        colander.Set(),
        widget=ideasofreplacement_choice,
        title=_('Added ideas'),
        description=_('Choose ideas to add.'),
        missing=[],
        default=[],
        )


class IntentionItemSchema(Schema):

    comment = colander.SchemaNode(
        colander.String(),
        title= _('Object'),
        description=_('The object of your intention (300 caracteres maximum).'),
        validator=colander.Length(max=300),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        )

    related_ideas = IdeasRowSchema(widget=SimpleMappingWidget())

    add_new_idea = NewIdeaSchema(widget=add_new_idea_widget)


class Intention(object):
    intention_id = "replaceideas"
    title = "Replace ideas"
    schema = IntentionItemSchema

    @classmethod
    def get_parameters(cls):
        schemainstanceideas = cls.schema().get('related_ideas')
        schemainstance = omit(cls.schema(), ['related_ideas', 'add_new_idea'])
        parameters = [ c.name for c in schemainstanceideas.children if c.name != '_csrf_token_']
        parameters.extend([ c.name for c in schemainstance.children if c.name != '_csrf_token_'])
        return parameters

    @classmethod
    def get_explanation_data(cls, args):
        result = {}
        parameters = cls.get_parameters()
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

    @classmethod
    def get_explanation_ideas(cls, args):
        data = cls.get_explanation_data(args)
        result = data['added_ideas']
        result.extend(data['removed_ideas'])
        result.extend(data['edited_ideas'])
        return result

    @classmethod
    def get_explanation_default_data(cls, args):
        data = cls.get_explanation_data(args);
        data['related_ideas'] = {'added_ideas': data.pop('added_ideas'),
                                 'removed_ideas': data.pop('removed_ideas'),
                                 'edited_ideas': data.pop('edited_ideas'),
                                }
        return data

    @classmethod
    def eq(cls, intention1, intention2):
        ideas1 = intention1['removed_ideas']
        ideas2 = intention2['removed_ideas']
        ideas1.extend(intention1['edited_ideas'])
        ideas2.extend(intention2['edited_ideas'])
        edited_inter = any((e in ideas2) for e in ideas1)
        return edited_inter

    @classmethod
    def get_intention(cls, view):
        result = {}
        parameters = cls.get_parameters()
        for param in parameters:
            value = view.params(param)
            if value is None:
                value = []

            result[param] = value

        return result

    @classmethod
    def get_explanation_dict(cls, args):
        result = {}
        parameters = cls.get_parameters()
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
    def get_related_ideas(cls, args):
        data = cls.get_explanation_ideas(args)
        return {'related_ideas': data}


class IntentionSchema(Schema):

    relatedexplanation = RelatedExplanationSchema(widget=SimpleMappingWidget(item_css_class="explanations-bloc"))

    intention = IntentionItemSchema(widget=SimpleMappingWidget(item_css_class="intention-bloc"))


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

    def __init__(self, **kwargs):
        super(Amendment, self).__init__(**kwargs)
        self.explanations = PersistentDict()
        self.set_data(kwargs)

    @region.cache_on_arguments() 
    def get_used_ideas(self):
        result = []
        if not hasattr(self, 'explanations'):
            return result

        for explanation in self.explanations.values():
            if explanation['intention'] is not None:
                result.extend(Intention.get_explanation_ideas(explanation['intention']))

        return result

    @property
    def added_ideas(self):
        result = []
        for explanation in self.explanations.values():
            if explanation['intention'] is not None:
                result.extend(Intention.get_explanation_data(explanation['intention'])['added_ideas'])

        return list(set(result))

    @property
    def edited_ideas(self):
        result = []
        for explanation in self.explanations.values():
            if explanation['intention'] is not None:
                result.extend(Intention.get_explanation_data(explanation['intention'])['edited_ideas'])

        return list(set(result))

    @property
    def removed_ideas(self):
        result = []
        for explanation in self.explanations.values():
            if explanation['intention'] is not None:
                result.extend(Intention.get_explanation_data(explanation['intention'])['removed_ideas'])

        return list(set(result))

    @property
    def explanation(self):
        result = []
        values = sorted(list(self.explanations.values()), key=lambda e: e['oid'])
        for explanation in values:
            if explanation['intention'] is not None:
                result.append('<p>'+(Intention.get_explanation_data(explanation['intention'])['comment'])+'</p>')

        if result:
            return '<div>'+"\n".join(result)+'</div>'
    
        return ''

