# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
import colander
from webob.multidict import MultiDict
from persistent.dict import PersistentDict
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
from novaideo import _
from novaideo.views.widget import LimitedTextAreaWidget
from novaideo.core import (
    VersionableEntity,
    DuplicableEntity,
    SearchableEntity,
    SearchableEntitySchema,
    CorrelableEntity,
    PresentableEntity,
    ExaminableEntity,
    Channel,
    Node,
    Emojiable,
    SignalableEntity)
from novaideo.content import get_file_widget
from novaideo.utilities.util import text_urls_format, truncate_text


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
            limit=2000,
            alert_template='novaideo:views/templates/idea_text_alert.pt',
            alert_values={'limit': 2000},
            item_css_class='idea-text',
            placeholder=_('I have an idea!')),
        title=_("Text")
        )

    note = colander.SchemaNode(
        colander.String(),
        widget=LimitedTextAreaWidget(
            rows=3,
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
            add_subitem_text_template='',
            item_css_class='files-block'),
        missing=[],
        title=_('Attached files'),
        )


@content(
    'idea',
    icon='icon novaideo-icon icon-idea',
    )
@implementer(Iidea)
class Idea(VersionableEntity, DuplicableEntity,
           SearchableEntity, CorrelableEntity, PresentableEntity,
           ExaminableEntity, Node, Emojiable, SignalableEntity):
    """Idea class"""

    type_title = _('Idea')
    icon = 'icon novaideo-icon icon-idea'
    templates = {'default': 'novaideo:views/templates/idea_result.pt',
                 'bloc': 'novaideo:views/templates/idea_bloc.pt',
                 'small': 'novaideo:views/templates/small_idea_result.pt',
                 'popover': 'novaideo:views/templates/idea_popover.pt'}
    template = 'novaideo:views/templates/idea_list_element.pt'
    name = renamer()
    author = SharedUniqueProperty('author', 'ideas')
    organization = SharedUniqueProperty('organization')
    attached_files = CompositeMultipleProperty('attached_files')
    url_files = CompositeMultipleProperty('url_files')
    tokens_opposition = CompositeMultipleProperty('tokens_opposition')
    tokens_support = CompositeMultipleProperty('tokens_support')
    opinions_base = OPINIONS

    def __init__(self, **kwargs):
        super(Idea, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.addtoproperty('channels', Channel())
        self.urls = PersistentDict({})

    @property
    def is_workable(self):
        request = get_current_request()
        idea_to_examine = 'idea' in request.content_to_examine
        if idea_to_examine:
            return True if 'favorable' in self.state else False

        return True

    @property
    def related_proposals(self):
        """Return all proposals that uses this idea"""
        return MultiDict([(item, c) for (item, c) in
                          self.all_target_related_contents.items()
                          if c.type == CorrelationType.solid and
                          'related_proposals' in c.tags])

    @property
    def related_contents(self):
        """Return all related contents"""
        return MultiDict([(item, c) for (item, c) in
                          self.all_source_related_contents.items()
                          if c.type == CorrelationType.weak])

    @property
    def tokens(self):
        result = list(self.tokens_opposition)
        result.extend(list(self.tokens_support))
        return result

    @property
    def authors(self):
        return [self.author]

    @property
    def relevant_data(self):
        return [getattr(self, 'title', ''),
                getattr(self, 'text', ''),
                ', '.join(self.keywords)]

    def __setattr__(self, name, value):
        super(Idea, self).__setattr__(name, value)
        if name == 'author':
            self.init_organization()

    def init_organization(self):
        if not self.organization:
            organization = getattr(self.author, 'organization', None)
            if organization:
                self.setproperty('organization', organization)

    def init_published_at(self):
        setattr(self, 'published_at', datetime.datetime.now(tz=pytz.UTC))

    def init_examined_at(self):
        setattr(self, 'examined_at', datetime.datetime.now(tz=pytz.UTC))

    def init_support_history(self):
        if not hasattr(self, '_support_history'):
            setattr(self, '_support_history', PersistentList())

    def presentation_text(self, nb_characters=400):
        return truncate_text(getattr(self, 'text', ""), nb_characters)

    def get_more_contents_criteria(self):
        "return specific query, filter values"
        return None, {
            'metadata_filter': {
                'content_types': ['proposal', 'idea'],
                'keywords': list(self.keywords)
            }
        }

    def get_attached_files_data(self):
        result = []
        for picture in self.attached_files:
            if picture:
                if picture.mimetype.startswith('image'):
                    result.append({
                        'content': picture.url,
                        'type': 'img'})

                if picture.mimetype.startswith(
                        'application/x-shockwave-flash'):
                    result.append({
                        'content': picture.url,
                        'type': 'flash'})

                if picture.mimetype.startswith('text/html'):
                    blob = picture.blob.open()
                    blob.seek(0)
                    content = blob.read().decode("utf-8")
                    blob.seek(0)
                    blob.close()
                    result.append({
                        'content': content,
                        'type': 'html'})

        return result

    def get_token(self, user):
        tokens = [t for t in getattr(user, 'tokens', []) if
                  not t.proposal]
        return tokens[-1] if tokens else None

    def get_node_descriminator(self):
        return 'idea'

    def format(self, request):
        text = getattr(self, 'text', '')
        all_urls, url_files, text_urls, formatted_text = text_urls_format(
            text, request)
        self.urls = PersistentDict(all_urls)
        self.setproperty('url_files', url_files)
        self.formatted_text = formatted_text
        self.formatted_urls = text_urls
