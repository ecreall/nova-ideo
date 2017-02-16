# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
import colander
from persistent.dict import PersistentDict
from collections import OrderedDict
from persistent.list import PersistentList
from zope.interface import implementer
from pyramid.threadlocal import get_current_request

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer, get_oid

from dace.util import getSite, get_obj
from dace.descriptors import (
    SharedUniqueProperty, CompositeMultipleProperty)
from pontus.core import VisualisableElementSchema
from pontus.widget import (
    SequenceWidget,
    AjaxSelect2Widget)
from pontus.file import ObjectData, File, Object as ObjectType

from .interface import Iidea
from novaideo.content.correlation import CorrelationType
from novaideo import _, log
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
    Debatable,
    Tokenable)
from novaideo.content import get_file_widget
from novaideo.utilities.util import (
    text_urls_format, truncate_text, get_files_data)


OPINIONS = OrderedDict([
    ('favorable', _('Positive')),
    ('to_study', _('To be re-worked upon')),
    ('unfavorable', _('Negative'))
])


@colander.deferred
def challenge_choice(node, kw):
    request = node.bindings['request']
    is_home_form = node.bindings.get('is_home_form', False)
    request_context = request.context
    challenge = getattr(request_context, 'challenge', None)
    root = getSite()
    values = [('', _('- Select -'))]
    if challenge is not None and challenge.can_add_content:
        values = [(get_oid(challenge), challenge.title)]

    def title_getter(id):
        try:
            obj = get_obj(int(id), None)
            if obj:
                return obj.title
            else:
                return id
        except Exception as e:
            log.warning(e)
            return id

    ajax_url = request.resource_url(
        root, '@@novaideoapi',
        query={'op': 'find_challenges'})
    item_css_class = 'challenge-input'
    is_challenge_content = is_home_form and challenge
    if is_challenge_content:
        item_css_class += ' challenge-content'

    return AjaxSelect2Widget(
        template='novaideo:views/idea_management/templates/ajax_select2.pt',
        values=values,
        ajax_url=ajax_url,
        ajax_item_template="related_item_template",
        title_getter=title_getter,
        challenge=challenge,
        is_challenge_content=is_challenge_content,
        multiple=False,
        add_clear=True,
        page_limit=20,
        item_css_class=item_css_class)


def context_is_a_idea(context, request):
    return request.registry.content.istype(context, 'idea')


class IdeaSchema(VisualisableElementSchema, SearchableEntitySchema):
    """Schema for idea"""

    name = NameSchemaNode(
        editing=context_is_a_idea,
        )

    challenge = colander.SchemaNode(
        ObjectType(),
        widget=challenge_choice,
        missing=None,
        title=_("Challenge (optional)"),
        description=_("You can select and/or modify the challenge associated to this idea. "
                      "For an open idea, do not select anything in the « Challenge » field.")
    )

    text = colander.SchemaNode(
        colander.String(),
        widget=LimitedTextAreaWidget(
            rows=5,
            cols=30,
            limit=2000,
            alert_template='novaideo:views/templates/idea_text_alert.pt',
            alert_values={'limit': 2000},
            item_css_class='content-preview-form',
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
           ExaminableEntity, Node, Emojiable, SignalableEntity, Debatable,
           Tokenable):
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
    challenge = SharedUniqueProperty('challenge', 'ideas')
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
        return [proposal[0] for proposal in self.get_related_contents(
            CorrelationType.solid, ['related_proposals'])]

    @property
    def related_contents(self):
        """Return all related contents"""
        return [content[0] for content in self.all_related_contents]

    @property
    def transformed_from(self):
        """Return all related contents"""
        transformed_from = [correlation[1].context for correlation
                            in self.get_related_contents(
                                CorrelationType.solid, ['transformation'])
                            if correlation[1].context]
        return transformed_from[0] if transformed_from else None

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
        return get_files_data(self.attached_files)

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
