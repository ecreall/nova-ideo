# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform.widget
from persistent.dict import PersistentDict
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer, get_oid

from dace.descriptors import (
    SharedUniqueProperty, CompositeMultipleProperty,
    SharedMultipleProperty)
from dace.util import getSite, get_obj
from pontus.core import VisualisableElementSchema
from pontus.widget import (
    Select2Widget, AjaxSelect2Widget,
    SequenceWidget)
from pontus.schema import Schema
from pontus.file import ObjectData, File

from .interface import IComment
from novaideo.core import (
    Commentable, Emojiable, can_access, SignalableEntity,
    CorrelableEntity)
from novaideo import _, log
from novaideo.content import get_file_widget
from novaideo.utilities.util import (
    text_urls_format,
    get_emoji_form,
    get_files_data, connect, disconnect)
from novaideo.content.correlation import CorrelationType


@colander.deferred
def intention_choice(node, kw):
    root = getSite()
    values = [(str(i), i) for i in root.comment_intentions]
    values.insert(0, ('', _('- Select -')))
    return Select2Widget(
        values=values,
        item_css_class="comment-form-group comment-intention-form")


@colander.deferred
def relatedcontents_choice(node, kw):
    request = node.bindings['request']
    context = node.bindings['context']
    root = getSite()
    values = []
    if isinstance(context, Comment) and\
       context.related_correlation:
        values = [(get_oid(t), t.title) for
                  t in context.associated_contents]

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
        query={'op': 'find_correlable_entity'})
    return AjaxSelect2Widget(
        values=values,
        ajax_url=ajax_url,
        ajax_item_template="related_item_template",
        css_class="search-idea-form",
        title_getter=title_getter,
        multiple=True,
        page_limit=50,
        item_css_class="comment-form-group comment-related-form")


class RelatedContentsSchema(Schema):
    """Schema for associtation"""

    associated_contents = colander.SchemaNode(
        colander.Set(),
        widget=relatedcontents_choice,
        title=_('Associated contents'),
        description=_('Choose the contents to be associated'),
        missing=[],
        default=[],
        )

    associate = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(
            item_css_class="hide-bloc"),
        label='',
        title='',
        default=False,
        missing=False
        )


@colander.deferred
def comment_textarea(node, kw):
    request = node.bindings['request']
    emoji_form = get_emoji_form(
        request, emoji_class='comment-form-group')
    return deform.widget.TextAreaWidget(
        rows=2, cols=60, item_css_class="comment-form-group comment-textarea",
        emoji_form=emoji_form,
        template='novaideo:views/templates/textarea_comment.pt')


def context_is_a_comment(context, request):
    return request.registry.content.istype(context, 'comment')


class CommentSchema(VisualisableElementSchema):
    """Schema for comment"""

    name = NameSchemaNode(
        editing=context_is_a_comment,
        )

    intention = colander.SchemaNode(
        colander.String(),
        widget=intention_choice,
        title=_('Intention'),
        description=_('Choose your intention'),
        default=_('Remark')
        )

    associated_contents = colander.SchemaNode(
        colander.Set(),
        widget=relatedcontents_choice,
        title=_('Associated contents'),
        description=_('Choose contents to associate'),
        missing=[],
        default=[],
        )

    files = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            ObjectData(File),
            name=_("File"),
            widget=get_file_widget()
            ),
        widget=SequenceWidget(
            add_subitem_text_template='',
            item_css_class="files-block comment-form-group comment-files"),
        missing=[],
        description=_('Add files to your comment'),
        title=_('Attached files'),
        )

    comment = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        widget=comment_textarea,
        title=_("Message")
        )


@content(
    'comment',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IComment)
class Comment(Commentable, CorrelableEntity, Emojiable, SignalableEntity):
    """Comment class"""
    icon = 'icon ion-chatbubbles'
    templates = {'default': 'novaideo:views/templates/comment_result.pt'}
    name = renamer()
    author = SharedUniqueProperty('author')
    files = CompositeMultipleProperty('files')
    url_files = CompositeMultipleProperty('url_files')
    related_correlation = SharedUniqueProperty('related_correlation', 'targets')
    contextualized_correlations = SharedMultipleProperty(
        'contextualized_correlations', 'context')

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.urls = PersistentDict({})
        self.edited = False
        self.pinned = False

    @property
    def channel(self):
        """Return the channel of th commented entity"""

        if not isinstance(self.__parent__, Comment):
            return self.__parent__
        else:
            return self.__parent__.channel

    @property
    def root(self):
        """Return the root comment"""

        if not isinstance(self.__parent__, Comment):
            return self
        else:
            return self.__parent__.root

    @property
    def comment_parent(self):
        """Return the root comment"""

        if isinstance(self.__parent__, Comment):
            return self.__parent__
        else:
            return None

    @property
    def subject(self):
        """Return the commented entity"""
        return self.channel.get_subject()

    @property
    def challenge(self):
        return getattr(self.subject, 'challenge', None)

    @property
    def relevant_data(self):
        return [getattr(self, 'comment', ''),
                getattr(self.author, 'title',
                        getattr(self.author, '__name__', ''))]

    @property
    def related_contents(self):
        subject = self.subject
        return [content[0] for content in self.contextualized_contents
                if content[0] is not subject]

    @property
    def associated_contents(self):
        subject = self.subject
        return [content[0] for content in self.contextualized_contents
                if content[0] is not subject and not getattr(content[1], 'tags', [])]

    def set_associated_contents(self, associated_contents, user):
        subject = self.subject
        current_associated_contents = self.associated_contents
        associated_contents_to_add = [i for i in associated_contents
                                      if i not in current_associated_contents]
        associated_contents_to_del = [i for i in current_associated_contents
                                      if i not in associated_contents and
                                      i not in associated_contents_to_add]
        correlations = connect(
            subject,
            associated_contents_to_add,
            {'comment': _('Add related contents'),
             'type': _('Edit the comment')},
            author=user,)
        for correlation in correlations:
            correlation.setproperty('context', self)

        disconnect(
            subject,
            associated_contents_to_del)

    def get_title(self):
        return self.subject.title

    def presentation_text(self, nb_characters=400):
        return getattr(self, 'comment', "")[:nb_characters]+'...'

    def get_discuss_url(self, request, user):
        subject = self.channel.get_subject(user)
        return request.resource_url(
            subject, "@@index") + '#comment-' + str(get_oid(self, 'None'))

    def get_url(self, request):
        return request.resource_url(
            request.root, "@@seecomment", query={'comment_id': get_oid(self)})

    def get_related_contents(self, user):
        return [r for r in self.related_contents if can_access(user, r)]

    def format(self, request, is_html=False):
        comment = getattr(self, 'comment', '')
        all_urls, url_files, text_urls, formatted_text = text_urls_format(
            comment, request, is_html)
        self.urls = PersistentDict(all_urls)
        self.setproperty('url_files', url_files)
        self.formatted_comment = formatted_text
        self.formatted_urls = text_urls

    def get_attached_files_data(self):
        return get_files_data(self.files)

    def can_add_reaction(self, process):
        return True
