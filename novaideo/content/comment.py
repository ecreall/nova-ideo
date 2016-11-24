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
    SharedUniqueProperty, CompositeMultipleProperty)
from dace.util import getSite, get_obj
from pontus.core import VisualisableElementSchema
from pontus.widget import (
    Select2Widget, AjaxSelect2Widget,
    SequenceWidget)
from pontus.schema import Schema
from pontus.file import ObjectData, File

from .interface import IComment
from novaideo.core import (
    Commentable, Emojiable, can_access, SignalableEntity)
from novaideo import _, log
from novaideo.content import get_file_widget
from novaideo.utilities.util import (
    text_urls_format,
    get_emoji_form)


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
                  t in context.related_contents]

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

    related_contents = colander.SchemaNode(
        colander.Set(),
        widget=relatedcontents_choice,
        title=_('Associated contents'),
        description=_('Choose contents to associate.'),
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

    related_contents = colander.SchemaNode(
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
class Comment(Commentable, Emojiable, SignalableEntity):
    """Comment class"""
    icon = 'icon ion-chatbubbles'
    templates = {'default': 'novaideo:views/templates/comment_result.pt'}
    name = renamer()
    author = SharedUniqueProperty('author')
    files = CompositeMultipleProperty('files')
    url_files = CompositeMultipleProperty('url_files')
    related_correlation = SharedUniqueProperty('related_correlation', 'targets')

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
    def relevant_data(self):
        return [getattr(self, 'comment', ''),
                getattr(self.author, 'title',
                        getattr(self.author, '__name__', ''))]

    @property
    def related_contents(self):
        if self.related_correlation:
            return [t for t
                    in self.related_correlation.targets
                    if not isinstance(t, Comment)]
        return []

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

    def format(self, request):
        comment = getattr(self, 'comment', '')
        all_urls, url_files, text_urls, formatted_text = text_urls_format(
            comment, request)
        self.urls = PersistentDict(all_urls)
        self.setproperty('url_files', url_files)
        self.formatted_comment = formatted_text
        self.formatted_urls = text_urls

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

    def can_add_reaction(self, process):
        return True
