# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
import colander
from webob.multidict import MultiDict
from collections import OrderedDict
from persistent.list import PersistentList
from zope.interface import implementer
from pyramid.threadlocal import get_current_request

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.descriptors import SharedUniqueProperty, CompositeMultipleProperty
from pontus.core import VisualisableElementSchema
from pontus.widget import (
    SequenceWidget)
from pontus.file import ObjectData, File

from .interface import Iidea
from novaideo.content.correlation import CorrelationType
from novaideo.core import Commentable
from novaideo import _
from novaideo.views.widget import LimitedTextAreaWidget
from novaideo.core import (
    VersionableEntity,
    DuplicableEntity,
    SearchableEntity,
    SearchableEntitySchema,
    CorrelableEntity,
    PresentableEntity)
from novaideo.content import get_file_widget


OPINIONS = OrderedDict([
    ('favorable', _('Favorable')),
    ('to_study', _('To study')),
    ('unfavorable', _('Unfavorable'))
])


def context_is_a_idea(context, request):
    return request.registry.content.istype(context, 'idea')


class IdeaSchema(VisualisableElementSchema, SearchableEntitySchema):
    """Schema for idea"""

    name = NameSchemaNode(
        editing=context_is_a_idea,
        )

    text = colander.SchemaNode(
        colander.String(),
        widget=LimitedTextAreaWidget(
            rows=5,
            cols=30,
            limit=600,
            alert_template='novaideo:views/templates/idea_text_alert.pt',
            alert_values={'limit': 600}),
        title=_("Text")
        )

    note = colander.SchemaNode(
        colander.String(),
        widget=LimitedTextAreaWidget(
            rows=5,
            cols=30,
            limit=300,
            alert_values={'limit': 300}),
        title=_("Note"),
        missing=""
        )

    attached_files = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            ObjectData(File),
            name=_("File"),
            widget=get_file_widget()
            ),
        widget=SequenceWidget(
            add_subitem_text_template=_('Add file')),
        missing=[],
        title=_('Attached files'),
        )


@content(
    'idea',
    icon='icon novaideo-icon icon-idea',
    )
@implementer(Iidea)
class Idea(Commentable, VersionableEntity, DuplicableEntity,
           SearchableEntity, CorrelableEntity, PresentableEntity):
    """Idea class"""

    type_title = _('Idea')
    icon = 'icon novaideo-icon icon-idea'
    templates = {'default': 'novaideo:views/templates/idea_result.pt',
                 'bloc': 'novaideo:views/templates/idea_result.pt'}
    template = 'novaideo:views/templates/idea_list_element.pt'
    name = renamer()
    author = SharedUniqueProperty('author', 'ideas')
    attached_files = CompositeMultipleProperty('attached_files')
    tokens_opposition = CompositeMultipleProperty('tokens_opposition')
    tokens_support = CompositeMultipleProperty('tokens_support')

    def __init__(self, **kwargs):
        super(Idea, self).__init__(**kwargs)
        self.set_data(kwargs)

    @property
    def is_workable(self):
        request = get_current_request()
        idea_to_examine = 'idea' in request.content_to_examine
        if idea_to_examine:
            return True if 'favorable' in self.state else False

        return True

    @property
    def opinion_value(self):
        return OPINIONS.get(
            getattr(self, 'opinion', {}).get('opinion', ''), None)

    @property
    def related_proposals(self):
        """Return all proposals that uses this idea"""
        return MultiDict([(c.source, c) for c in self.target_correlations
                          if c.type == CorrelationType.solid and
                          'related_proposals' in c.tags])

    @property
    def tokens(self):
        result = list(self.tokens_opposition)
        result.extend(list(self.tokens_support))
        return result

    @property
    def authors(self):
        return [self.author]

    def init_published_at(self):
        setattr(self, 'published_at', datetime.datetime.now(tz=pytz.UTC))

    def init_examined_at(self):
        setattr(self, 'examined_at', datetime.datetime.now(tz=pytz.UTC))

    def init_support_history(self):
        if not hasattr(self, '_support_history'):
            setattr(self, '_support_history', PersistentList())

    def presentation_text(self, nb_characters=400):
        return getattr(self, 'text', "")[:nb_characters]+'...'

    def get_more_contents_criteria(self):
        "return specific query, filter values"
        return None, {
            'metadata_filter': {
                'content_types': ['proposal', 'idea'],
                'keywords': list(self.keywords)
            }
        }
