# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from zope.interface import implementer
from persistent.dict import PersistentDict

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import getSite, get_obj
from dace.descriptors import (
    SharedUniqueProperty,
    SharedMultipleProperty)

from pontus.widget import (
    RichTextWidget,
    SimpleMappingWidget,
    AjaxSelect2Widget)
from pontus.core import VisualisableElementSchema
from pontus.schema import Schema, select, omit

from .interface import IAmendment
from novaideo.core import (
    SearchableEntity,
    SearchableEntitySchema,
    CorrelableEntity,
    Channel,
    PresentableEntity,
    DuplicableEntity)
from novaideo import _
from novaideo.views.widget import (
    AddIdeaWidget,
    LimitedTextAreaWidget,
    SimpleMappingtWidget)
from novaideo.content.idea import Idea, IdeaSchema
from novaideo.content.proposal import AddFilesSchemaSchema
from novaideo.utilities.util import html_to_text


@colander.deferred
def add_new_idea_widget(node, kw):
    request = node.bindings['request']
    root = getSite()
    url = request.resource_url(root, '@@ideasmanagement')
    return AddIdeaWidget(url=url, item_css_class='new-idea-form hide-bloc')


@colander.deferred
def relatedideas_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    used_ideas = context.get_used_ideas()
    root = getSite()
    ideas = list(context.proposal.related_ideas.keys())
    ideas.extend(used_ideas)
    ideas = set(ideas)
    values = [(i, i.title) for i in ideas]
    ajax_url = request.resource_url(root, '@@novaideoapi',
                                    query={'op': 'find_ideas'}
                               )
    return AjaxSelect2Widget(values=values,
                        ajax_url=ajax_url,
                        css_class="search-idea-form",
                        multiple=True)


class RelatedExplanationSchema(Schema):
    """Schema for related explanation"""

    relatedexplanation = colander.SchemaNode(
        colander.Integer(),
        title=_('Apply the same explanation'),
        description=_('Choose the imrovement to apply'),
        missing=None
        )


class NewIdeaSchema(Schema):

    new_idea = select(IdeaSchema(factory=Idea,
                                 editable=True,
                                 widget=SimpleMappingWidget()),
                      ['title',
                       'text',
                       'keywords'])


class IntentionItemSchema(Schema):
    """Schema for Intention item"""

    comment = colander.SchemaNode(
        colander.String(),
        title=_('Give a specific explanation'),
        validator=colander.Length(max=300),
        widget=LimitedTextAreaWidget(rows=5,
                                     cols=30,
                                     limit=300),
        )

    related_ideas = colander.SchemaNode(
        colander.Set(),
        widget=relatedideas_choice,
        title=_('Related ideas'),
        description=_('Choose related ideas.'),
        missing=[],
        default=[],
        )

    add_new_idea = NewIdeaSchema(widget=add_new_idea_widget)


class Intention(object):
    """Intention class"""

    schema = IntentionItemSchema
    parameters = ['comment', 'related_ideas']

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
                            if obj is None:
                                raise Exception()
 
                            listvalue.append(obj)

                        result[k] = listvalue

                    else:
                        obj = get_obj(int(value), True)
                        if obj is None:
                            raise Exception()
                       
                        result[k] = obj

                except Exception:
                    result[k] = value

        return result

    @classmethod
    def get_explanation_ideas(cls, args):
        """Return all related ideas"""
        return cls.get_explanation_data(args)['related_ideas']

    @classmethod
    def get_explanation_default_data(cls, args):
        """Return related ideas"""
        data = cls.get_explanation_data(args)
        data['related_ideas'] = data.pop('related_ideas')
        return data

    @classmethod
    def eq(cls, intention1, intention2):
        """Return True if intention1 has a relation with intention2"""
        if intention1['comment'] != intention2['comment']:
            return False

        related_ideas1 = list(intention1['related_ideas'])
        related_ideas2 = list(intention2['related_ideas'])
        related_ideas_eq = (len(related_ideas1) == len(related_ideas2)) and \
                     all((e in related_ideas2) for e in related_ideas1)
        if not related_ideas_eq:
            return False

        return True

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
                                  css_class="explanations-bloc")
                         )

    intention = IntentionItemSchema(
                widget=SimpleMappingWidget(
                       css_class="intention-bloc")
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

    add_files = omit(AddFilesSchemaSchema(
                    widget=SimpleMappingtWidget(
                    mapping_css_class='controled-form'
                                      ' object-well default-well hide-bloc',
                    ajax=True,
                    activator_icon="glyphicon glyphicon-file",
                    activator_title=_('Add files'))),
                        ["_csrf_token_"])


@content(
    'amendment',
    icon='icon novaideo-icon icon-amendment',
    )
@implementer(IAmendment)
class Amendment(CorrelableEntity,
                SearchableEntity,
                DuplicableEntity,
                PresentableEntity):
    """Amendment class"""

    type_title = _('Amendment')
    icon = 'icon novaideo-icon icon-amendment'
    name = renamer()
    templates = {
        'default': 'novaideo:views/templates/amendment_result.pt'
    }
    author = SharedUniqueProperty('author')
    proposal = SharedUniqueProperty('proposal', 'amendments')
    attached_files = SharedMultipleProperty('attached_files')

    def __init__(self, **kwargs):
        super(Amendment, self).__init__(**kwargs)
        self.explanations = PersistentDict()
        self.set_data(kwargs)
        self.addtoproperty('channels', Channel())

    @property
    def is_published(self):
        return 'submitted' in self.state

    @property
    def working_group(self):
        return self.proposal.working_group

    @property
    def authors(self):
        return [self.author]

    def _init_presentation_text(self):
        self._presentation_text = html_to_text(
            getattr(self, 'text', ''))

    def __setattr__(self, name, value):
        super(Amendment, self).__setattr__(name, value)
        if name == 'text':
            self._init_presentation_text()

    def presentation_text(self, nb_characters=400):
        text = getattr(self, '_presentation_text', None)
        if text is None:
            self._init_presentation_text()
            text = getattr(self, '_presentation_text', '')

        return text[:nb_characters]+'...'


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
    def related_ideas(self):
        """Return added ideas"""

        result = []
        for explanation in self.explanations.values():
            if explanation['intention'] is not None:
                try:
                    result.extend(
                        Intention.get_explanation_data(
                            explanation['intention'])['related_ideas']
                        )
                except Exception:
                    pass

        return list(set(result))
