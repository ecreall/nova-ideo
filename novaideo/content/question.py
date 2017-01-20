# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
from persistent.dict import PersistentDict
from zope.interface import implementer
from BTrees.OOBTree import OOBTree

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer, get_oid

from dace.descriptors import SharedUniqueProperty, CompositeMultipleProperty
from pontus.core import VisualisableElementSchema
from pontus.widget import (
    SequenceWidget, Select2Widget)
from pontus.file import ObjectData, File

from .interface import IQuestion, IAnswer
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
    SignalableEntity,
    Sustainable,
    can_access)
from novaideo.content import get_file_widget
from novaideo.content.comment import CommentSchema, Comment
from novaideo.utilities.util import text_urls_format, truncate_text


def context_is_a_question(context, request):
    return request.registry.content.istype(context, 'question')


class QuestionSchema(VisualisableElementSchema, SearchableEntitySchema):
    """Schema for question"""

    name = NameSchemaNode(
        editing=context_is_a_question,
        )

    title = colander.SchemaNode(
        colander.String(),
        title=_("Question")
        )

    options = colander.SchemaNode(
        colander.Set(),
        widget=Select2Widget(
            max_len=5,
            values=[],
            create=True,
            multiple=True),
        title=_('Options'),
        description=_("To add options, you need to tap the « Enter »"
                      " key after each keyword or separate them with commas."),
        missing=[]
        )

    text = colander.SchemaNode(
        colander.String(),
        widget=LimitedTextAreaWidget(
            rows=5,
            cols=30,
            limit=2000,
            alert_values={'limit': 2000},
            item_css_class='content-preview-form',
            placeholder=_('I have a question!')),
        title=_("Details"),
        missing=''
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
    'question',
    icon='icon novaideo-icon icon-question',
    )
@implementer(IQuestion)
class Question(VersionableEntity, DuplicableEntity,
               SearchableEntity, CorrelableEntity, PresentableEntity,
               ExaminableEntity, Node, Emojiable, SignalableEntity,
               Sustainable):
    """Question class"""

    type_title = _('Question')
    icon = 'md md-live-help'
    templates = {'default': 'novaideo:views/templates/question_result.pt',
                 'bloc': 'novaideo:views/templates/question_bloc.pt',
                 'small': 'novaideo:views/templates/small_question_result.pt',
                 'popover': 'novaideo:views/templates/question_popover.pt'}
    template = 'novaideo:views/templates/question_list_element.pt'
    name = renamer()
    author = SharedUniqueProperty('author', 'questions')
    organization = SharedUniqueProperty('organization')
    attached_files = CompositeMultipleProperty('attached_files')
    url_files = CompositeMultipleProperty('url_files')
    related_correlation = SharedUniqueProperty('related_correlation', 'targets')
    answers = CompositeMultipleProperty('answers', 'question')

    def __init__(self, **kwargs):
        super(Question, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.addtoproperty('channels', Channel())
        self.urls = PersistentDict({})
        self.len_answers = 0

    @property
    def authors(self):
        return [self.author]

    @property
    def relevant_data(self):
        return [getattr(self, 'title', ''),
                getattr(self, 'text', ''),
                ', '.join(self.keywords)]

    def __setattr__(self, name, value):
        super(Question, self).__setattr__(name, value)
        if name == 'author':
            self.init_organization()

    def update_len_answers(self):
        self.len_answers = len(self.answers)
        return self.len_answers

    def addtoproperty(self, name, value, moving=None):
        super(Question, self).addtoproperty(name, value, moving)
        if name == 'answers':
            self.len_answers += 1

    def delfromproperty(self, name, value, moving=None):
        super(Question, self).delfromproperty(name, value, moving)
        if name == 'answers':
            self.len_answers -= 1

    def init_organization(self):
        if not self.organization:
            organization = getattr(self.author, 'organization', None)
            if organization:
                self.setproperty('organization', organization)

    def presentation_text(self, nb_characters=400):
        return truncate_text(getattr(self, 'text', ""), nb_characters)

    def get_more_contents_criteria(self):
        "return specific query, filter values"
        return None, {
            'metadata_filter': {
                'content_types': ['question'],
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

    def get_node_descriminator(self):
        return 'question'

    def format(self, request):
        text = getattr(self, 'text', '')
        all_urls, url_files, text_urls, formatted_text = text_urls_format(
            text, request)
        self.urls = PersistentDict(all_urls)
        self.setproperty('url_files', url_files)
        self.formatted_text = formatted_text
        self.formatted_urls = text_urls

##################################### Answer ##################################


class AnswerSchema(CommentSchema):
    """Schema for Answer"""
    pass


@content(
    'answer',
    icon='icon novaideo-icon icon-question',
    )
@implementer(IAnswer)
class Answer(CorrelableEntity, PresentableEntity,
             ExaminableEntity, Node, Emojiable,
             SignalableEntity, Sustainable):
    """Answer class"""

    type_title = _('Answer')
    icon = 'md md-live-help'
    templates = {'default': 'novaideo:views/templates/answer_result.pt',
                 'bloc': 'novaideo:views/templates/answer_bloc.pt',
                 'small': 'novaideo:views/templates/small_answer_result.pt',
                 'popover': 'novaideo:views/templates/answer_popover.pt'}
    template = 'novaideo:views/templates/answer_list_element.pt'
    name = renamer()
    author = SharedUniqueProperty('author')
    files = CompositeMultipleProperty('files')
    url_files = CompositeMultipleProperty('url_files')
    related_correlation = SharedUniqueProperty('related_correlation', 'targets')
    channels = CompositeMultipleProperty('channels', 'subject')
    question = SharedUniqueProperty('question', 'answers')

    def __init__(self, **kwargs):
        super(Answer, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.addtoproperty('channels', Channel())
        self.urls = PersistentDict({})

    @property
    def related_contents(self):
        if self.related_correlation:
            return [t for t
                    in self.related_correlation.targets
                    if not isinstance(t, Comment)]
        return []

    @property
    def relevant_data(self):
        return [getattr(self, 'comment', ''),
                getattr(self.author, 'title',
                        getattr(self.author, '__name__', ''))]

    @property
    def channel(self):
        channels = getattr(self, 'channels', [])
        return channels[0] if channels else None

    def get_title(self, user=None):
        return getattr(self.question, 'title', '')

    def subscribe_to_channel(self, user):
        channel = getattr(self, 'channel', None)
        if channel and (user not in channel.members):
            channel.addtoproperty('members', user)

    def get_related_contents(self, user):
        return [r for r in self.related_contents if can_access(user, r)]

    def get_attached_files_data(self):
        result = []
        for picture in self.files:
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

    def get_node_descriminator(self):
        return 'answer'

    def format(self, request):
        comment = getattr(self, 'comment', '')
        all_urls, url_files, text_urls, formatted_text = text_urls_format(
            comment, request)
        self.urls = PersistentDict(all_urls)
        self.setproperty('url_files', url_files)
        self.formatted_comment = formatted_text
        self.formatted_urls = text_urls
