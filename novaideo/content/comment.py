# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform.widget
from persistent.dict import PersistentDict
from zope.interface import implementer
from pyramid import renderers

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
from novaideo.core import Commentable, Emojiable
from novaideo import _, log
from novaideo.content import get_file_widget
from novaideo.utilities.url_extractor import extract_urls
from novaideo.utilities.util import (
    html_to_text, extract_urls_metadata, get_emoji_form)


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
                  t in context.get_related_contents()]

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
class Comment(Commentable, Emojiable):
    """Comment class"""
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

    def get_related_contents(self):
        if self.related_correlation:
            return [t for t
                    in self.related_correlation.targets
                    if not isinstance(t, Comment)]
        return []

    def init_urls(self):
        self.urls = PersistentDict({})

    def format(self, request):
        comment = getattr(self, 'comment', '')
        url_results = []
        self.init_urls()
        self.setproperty('url_files', [])
        if comment:
            urls = extract_urls(comment)
            for data_url in extract_urls_metadata(urls):
                if data_url['image']:
                    new_image = data_url.pop('image')
                    self.addtoproperty('url_files', new_image)
                    data_url['image_url'] = new_image.url

                self.urls[data_url['url']] = data_url
                value = renderers.render(
                    'novaideo:views/templates/comment_url.pt',
                    data_url, request)
                url_results.append(value)

        comment_urls = '<p>' + ''.join(url_results) + '</p>'
        urls = extract_urls(html_to_text(comment_urls))
        for url in urls:
            comment_urls = comment_urls.replace(
                url, '<a  target="_blank" href="'+url+'">'+url+'</a>')

        urls = extract_urls(comment)
        comment = comment.replace('\n', '<br/>')
        for url in urls:
            comment = comment.replace(
                url, '<a  target="_blank" href="'+url+'">'+url+'</a>')

        self.formated_comment = '<p class="emoji-container">' + comment + '</p>'
        self.formated_urls = comment_urls

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
