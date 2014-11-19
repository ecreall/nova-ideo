
import colander
import deform
from zope.interface import implementer
from persistent.dict import PersistentDict

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import getSite, get_obj
from dace.objectofcollaboration.principal.util import get_current
from dace.descriptors import SharedUniqueProperty

from pontus.widget import RichTextWidget, SimpleMappingWidget
from pontus.core import VisualisableElementSchema
from pontus.schema import Schema, select

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
from novaideo.views.widget import (
    Select2WidgetSearch, 
    AddIdeaWidget, 
    LimitedTextAreaWidget)
from novaideo.content.idea import Idea, IdeaSchema


@colander.deferred
def idea_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    used_ideas = context.get_used_ideas()
    root = getSite()
    user = get_current()
    ideas = list(getattr(user, 'ideas', []))
    ideas.extend([ i for i in getattr(user, 'selections', []) \
                   if isinstance(i, Idea) and can_access(user, i)])
    ideas.extend(used_ideas)
    ideas = set(ideas) 
    values = [(i, i.title) for i in ideas if not('archived' in i.state)]
    return Select2WidgetSearch(multiple= True, 
                               values=values,  
                               item_css_class='search-idea-form',
                               url=request.resource_url(root, '@@search',
                                     query={'op':'toselect',
                                            'content_types':['Idea']}
                                     ))


@colander.deferred
def add_new_idea_widget(node, kw):
    request = node.bindings['request']
    root = getSite()
    url = request.resource_url(root, '@@ideasmanagement')
    return AddIdeaWidget(url=url, item_css_class='new-idea-form hide-bloc')
    

@colander.deferred
def replacedideas_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    used_ideas = context.get_used_ideas()
    root = getSite()
    ideas = list(context.proposal.related_ideas.keys())
    ideas.extend(used_ideas)
    ideas = set(ideas)
    values = [(i, i.title) for i in ideas]
    return Select2WidgetSearch(multiple= True, 
                               values=values,
                               item_css_class='search-idea-form',
                               url=request.resource_url(root, '@@search', 
                                query={'op':'toselect',
                                       'content_types':['Idea']}
                                ))


@colander.deferred
def ideasofreplacement_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    used_ideas = context.get_used_ideas()
    root = getSite()
    user = get_current()
    ideas = list(getattr(user, 'ideas', []))
    ideas.extend([ i for i in getattr(user, 'selections', []) \
                   if isinstance(i, Idea) and can_access(user, i)])
    ideas.extend(used_ideas)
    ideas = set(ideas) 
    values = [(i, i.title) for i in ideas if not('archived' in i.state)]
    return Select2WidgetSearch(multiple= True, 
                               values=values, 
                               item_css_class='search-idea-form',
                               url=request.resource_url(root, '@@search', 
                                    query={'op':'toselect',
                                           'content_types':['Idea']}
                                ))


class RelatedExplanationSchema(Schema):
    """Schema for related explanation"""

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


class IdeasSchema(Schema):
    """Schema for related ideas"""

    edited_ideas = colander.SchemaNode(
        colander.Set(),
        widget=replacedideas_choice,
        title=_('Edited ideas'),
        description=_('Choose edited ideas.'),
        missing=[],
        default=[],
        )

    removed_ideas = colander.SchemaNode(
        colander.Set(),
        widget=replacedideas_choice,
        title=_('Removed ideas'),
        description=_('Choose removed ideas.'),
        missing=[],
        default=[],
        )

    added_ideas = colander.SchemaNode(
        colander.Set(),
        widget=ideasofreplacement_choice,
        title=_('Added ideas'),
        description=_('Choose added ideas.'),
        missing=[],
        default=[],
        )


class IntentionItemSchema(Schema):
    """Schema for Intention item"""

    comment = colander.SchemaNode(
        colander.String(),
        title= _('Explanation'),
        description=_('The explanation of your intention (300 caracteres maximum)'),
        validator=colander.Length(max=300),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        )

    related_ideas = IdeasSchema(widget=SimpleMappingWidget())

    add_new_idea = NewIdeaSchema(widget=add_new_idea_widget)


class Intention(object):
    """Intention class"""

    schema = IntentionItemSchema
    parameters = ['comment', 'edited_ideas', 'removed_ideas', 'added_ideas']

    @classmethod
    def get_explanation_data(cls, args):
        """Return the value of the intention"""

        result = {}
        for (k, value) in args.items():
            if k in cls.parameters:
                try:
                    if isinstance(value, list):
                        listvalue = []
                        for val in value:
                            obj = get_obj(int(val), True)
                            if obj is None :
                                raise Exception()
 
                            listvalue.append(obj)

                        result[k] = listvalue

                    else:
                        obj = get_obj(int(value), True)
                        if obj is None :
                            raise Exception()
                       
                        result[k] = obj

                except Exception:
                    result[k] = value

        return result

    @classmethod
    def get_explanation_ideas(cls, args):
        """Return all related ideas"""

        data = cls.get_explanation_data(args)
        result = data['added_ideas']
        result.extend(data['removed_ideas'])
        result.extend(data['edited_ideas'])
        return result

    @classmethod
    def get_explanation_default_data(cls, args):
        """Return related ideas"""

        data = cls.get_explanation_data(args)
        data['related_ideas'] = {'added_ideas': data.pop('added_ideas'),
                                 'removed_ideas': data.pop('removed_ideas'),
                                 'edited_ideas': data.pop('edited_ideas'),
                                }
        return data

    @classmethod
    def eq(cls, intention1, intention2):
        """Return True if intention1 has a relation with intention2"""

        ideas1 = list(intention1['removed_ideas'])
        ideas2 = list(intention2['removed_ideas'])
        ideas1.extend(list(intention1['edited_ideas']))
        ideas2.extend(list(intention2['edited_ideas']))
        added_ideas1 = list(intention1['added_ideas'])
        added_ideas2 = list(intention2['added_ideas'])
        edited_inter =  (not ideas1 and not ideas2) or \
                         any((e in ideas2) for e in ideas1)
        added_inter = (not added_ideas1 and not added_ideas2) or \
                       any((e in added_ideas2) for e in added_ideas1)
        return edited_inter or added_inter

    @classmethod
    def get_intention(cls, view):
        """Return the value of the intention from the view"""

        result = {}
        for param in cls.parameters:
            value = view.params(param)
            if value is None:
                value = []

            result[param] = value

        return result


class IntentionSchema(Schema):
    """Schema for Intention"""

    relatedexplanation = RelatedExplanationSchema(
                         widget=SimpleMappingWidget(
                                  item_css_class="explanations-bloc")
                         )

    intention = IntentionItemSchema(
                widget=SimpleMappingWidget(
                       item_css_class="intention-bloc")
                )


def context_is_a_amendment(context, request):
    return request.registry.content.istype(context, 'amendment')


class AmendmentSchema(VisualisableElementSchema, SearchableEntitySchema):
    """Schema for Amendment"""

    name = NameSchemaNode(
        editing=context_is_a_amendment,
        )

    description = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=300),
        widget=LimitedTextAreaWidget(rows=5, 
                                     cols=30, 
                                     limit=300),
        title=_("Abstract")
        )

    text = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget(),
        title=_("Text")
        )


@content(
    'amendment',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IAmendment)
class Amendment(Commentable,
                CorrelableEntity,
                SearchableEntity,
                DuplicableEntity,
                PresentableEntity):
    """Amendment class"""

    name = renamer()
    result_template = 'novaideo:views/templates/amendment_result.pt'
    author = SharedUniqueProperty('author')
    proposal = SharedUniqueProperty('proposal', 'amendments')

    def __init__(self, **kwargs):
        super(Amendment, self).__init__(**kwargs)
        self.explanations = PersistentDict()
        self.set_data(kwargs)

   # @region.cache_on_arguments() 
    def get_used_ideas(self):
        """Return used ideas"""

        result = []
        if not hasattr(self, 'explanations'):
            return result

        for explanation in self.explanations.values():
            if explanation['intention'] is not None:
                try:
                    result.extend(
                          Intention.get_explanation_ideas(
                             explanation['intention'])
                          )
                except Exception:
                    pass

        return list(set(result))

    @property
    def added_ideas(self):
        """Return added ideas"""

        result = []
        for explanation in self.explanations.values():
            if explanation['intention'] is not None:
                try:
                    result.extend(
                        Intention.get_explanation_data(
                            explanation['intention'])['added_ideas']
                        )
                except Exception:
                    pass

        return list(set(result))

    @property
    def edited_ideas(self):
        """Return edited ideas"""

        result = []
        for explanation in self.explanations.values():
            if explanation['intention'] is not None:
                try:
                    result.extend(
                        Intention.get_explanation_data(
                            explanation['intention'])['edited_ideas']
                        )
                except Exception:
                    pass

        return list(set(result))

    @property
    def removed_ideas(self):
        """Return removed ideas"""

        result = []
        for explanation in self.explanations.values():
            if explanation['intention'] is not None:
                try:
                    result.extend(
                        Intention.get_explanation_data(
                            explanation['intention'])['removed_ideas']
                        )
                except Exception:
                    pass


        return list(set(result))

    @property
    def explanation(self):
        """Return all comments"""

        result = []
        values = sorted(list(self.explanations.values()),
                        key=lambda e: e['oid'])
        for explanation in values:
            if explanation['intention'] is not None:
                try:
                    result.append(
                        '<p>'+(Intention.get_explanation_data(
                            explanation['intention'])['comment'])+'</p>'
                        )
                except Exception:
                    pass

        if result:
            return '<div>'+"\n".join(list(set(result)))+'</div>'
    
        return ''

