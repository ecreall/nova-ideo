# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
from BTrees.OOBTree import OOBTree
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer, get_oid

from dace.descriptors import SharedUniqueProperty, CompositeMultipleProperty
from pontus.core import VisualisableElementSchema
from pontus.widget import (
    SequenceWidget)
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
    Debatable,
    can_access)
from novaideo.content import get_file_widget
from novaideo.content.comment import CommentSchema
from novaideo.utilities.util import (
    text_urls_format, truncate_text, to_localized_time,
    get_files_data)


def context_is_a_question(context, request):
    return request.registry.content.istype(context, 'question')


class Options(colander.SequenceSchema):
    option = colander.SchemaNode(
        colander.String()
        )


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
        colander.Sequence(),
        colander.SchemaNode(
            colander.String(),
            name=_("Option")
            ),
        widget=SequenceWidget(
            add_subitem_text_template='',
            orderable=True),
        title=_('Options'),
        description=_("You can add options to your question. "
                      "Users can only answer questions with options once. "
                      "Statistics will be provided indicating the percentage "
                      "of each option."),
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
               Sustainable, Debatable):
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
    answer = SharedUniqueProperty('answer')

    def __init__(self, **kwargs):
        super(Question, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.addtoproperty('channels', Channel())
        self.selected_options = OOBTree()
        self.users_options = OOBTree()
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
        return truncate_text(getattr(self, 'text', ''), nb_characters)

    def get_more_contents_criteria(self):
        "return specific query, filter values"
        return None, {
            'metadata_filter': {
                'content_types': ['question'],
                'keywords': list(self.keywords)
            }
        }

    def get_attached_files_data(self):
        return get_files_data(self.attached_files)

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

    def add_selected_option(self, user, option):
        self.remove_selected_option(user)
        oid = get_oid(user)
        self.selected_options[oid] = option
        self.users_options.setdefault(option, [])
        if option in self.users_options:
            self.users_options[option].append(oid)
        else:
            self.users_options[option] = PersistentList([oid])

    def remove_selected_option(self, user):
        oid = get_oid(user)
        if oid in self.selected_options:
            option = self.selected_options.pop(oid)
            if oid in self.users_options[option]:
                user_options = self.users_options[option]
                user_options.remove(oid)
                self.users_options[option] = PersistentList(
                    list(set(user_options)))

    def get_selected_option(self, user):
        oid = get_oid(user)
        if oid in self.selected_options:
            return self.selected_options.get(oid)

        return None

    def get_user_with_option(self, option):
        options = getattr(self, 'options', [])
        if options and option in self.users_options:
            return self.users_options[option]

        return []

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
             SignalableEntity, Sustainable, Debatable):
    """Answer class"""

    type_title = _('Answer')
    icon = 'glyphicon glyphicon-saved'
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
    question = SharedUniqueProperty('question', 'answers')

    def __init__(self, **kwargs):
        super(Answer, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.addtoproperty('channels', Channel())
        self.urls = PersistentDict({})

    def init_title(self):
        self.title = 'Answer: {question} {date}'.format(
            question=getattr(self.question, 'title', ''),
            date=to_localized_time(self.created_at, translate=True))

    @property
    def related_contents(self):
        if self.related_correlation:
            return [t for t
                    in self.related_correlation.targets
                    if t is not self]
        return []

    @property
    def relevant_data(self):
        return [getattr(self, 'comment', ''),
                getattr(self, 'title', ''),
                getattr(self.author, 'title',
                        getattr(self.author, '__name__', ''))]

    @property
    def subject(self):
        return self

    def presentation_text(self, nb_characters=400):
        return truncate_text(getattr(self, 'comment', ''), nb_characters)

    def get_related_contents(self, user):
        return [r for r in self.related_contents if can_access(user, r)]

    def get_attached_files_data(self):
        return get_files_data(self.files)

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
