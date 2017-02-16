# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
import datetime
import pytz
import deform
import colander
import json
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer, get_oid

from dace.util import getSite, get_obj
from dace.descriptors import (
    SharedUniqueProperty,
    SharedMultipleProperty,
    CompositeUniqueProperty,
    CompositeMultipleProperty)
from pontus.core import VisualisableElementSchema
from pontus.widget import (
    RichTextWidget, ImageWidget, SequenceWidget,
    AjaxSelect2Widget)
from pontus.file import ObjectData, File
from pontus.form import FileUploadTempStore

from .interface import IChallenge
from novaideo.core import (
    SearchableEntity,
    Channel,
    SearchableEntitySchema,
    CorrelableEntity,
    PresentableEntity,
    ExaminableEntity,
    Node,
    Emojiable,
    SignalableEntity,
    Debatable)
from novaideo.content.correlation import CorrelationType
from novaideo.views.widget import LimitedTextAreaWidget
from novaideo import _, log
from novaideo.file import Image
from novaideo.utilities.util import (
    text_urls_format, get_files_data)
from novaideo.content import get_file_widget


@colander.deferred
def image_widget(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite()
    tmpstore = FileUploadTempStore(request)
    source = None
    if context is not root:
        if context.image:
            source = context.image

    return ImageWidget(
        tmpstore=tmpstore,
        source=source,
        selection_message=_("Upload image.")
        )


@colander.deferred
def users_to_invite(node, kw):
    request = node.bindings['request']
    context = node.bindings['context']
    state = 'closed'
    if request.POST and json.loads(
       request.POST.get('is_restricted', 'false')):
        state = ''

    root = getSite()
    values = []
    if isinstance(context, Challenge) and\
       context.invited_users:
        values = [(get_oid(t), t.title) for
                  t in context.invited_users]

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
        query={'op': 'find_groups'})
    return AjaxSelect2Widget(
        values=values,
        ajax_url=ajax_url,
        ajax_item_template="related_item_template",
        item_css_class='invitedusers-input '+state,
        title_getter=title_getter,
        multiple=True,
        page_limit=50,)


def context_is_a_challenge(context, request):
    return request.registry.content.istype(context, 'challenge')


class ChallengeSchema(VisualisableElementSchema, SearchableEntitySchema):
    """Schema for challenge"""

    name = NameSchemaNode(
        editing=context_is_a_challenge,
        )

    description = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=300),
        widget=LimitedTextAreaWidget(rows=5,
                                     cols=30,
                                     limit=300),
        title=_("Abstract"),
        description=_("Describe in a few words the challenge.")
        )

    text = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget(),
        title=_("Text"),
        description=_("You can describe in detail the challenge.")
        )

    image = colander.SchemaNode(
        ObjectData(Image),
        widget=image_widget,
        title=_('Image'),
        description=_('You see a square on the top left of the image if it exceeds the maximum'
                      ' size allowed. Move and enlarge it if necessary, to determine an area of'
                      ' interest. Several images will be generated from this area.'),
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

    is_restricted = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(
            item_css_class='is-restricted-input'),
        label=_('Is restricted'),
        title='',
        description=_('Check this box if the challenge is restricted to a set of members. '
                      'Only concerned members can add and see the contents created in this challenge.'),
        missing=False
    )

    invited_users = colander.SchemaNode(
        colander.Set(),
        widget=users_to_invite,
        title=_('Concerned users'),
        description=_('Find and select the concerned members or organizations. '
                      'If you want to see the members or organizations... already '
                      'registered on the platform, enter a *'),
        missing=[],
    )

    deadline = colander.SchemaNode(
        colander.Date(),
        title=_('Deadline'),
        description=_("If your challenge is punctual, you can add a deadline for participation."),
        missing=None
    )


@content(
    'challenge',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IChallenge)
class Challenge(
    SearchableEntity,
    CorrelableEntity,
    PresentableEntity,
    ExaminableEntity,
    Node,
    Emojiable,
    SignalableEntity,
    Debatable):
    """Challenge class"""
    type_title = _('Challenge')
    icon = 'ion-trophy'
    templates = {'default': 'novaideo:views/templates/challenge_result.pt',
                 'bloc': 'novaideo:views/templates/challenge_bloc.pt',
                 'small': 'novaideo:views/templates/small_challenge_result.pt',
                 'popover': 'novaideo:views/templates/challenge_popover.pt'}
    name = renamer()
    author = SharedUniqueProperty('author', 'challenges')
    image = CompositeUniqueProperty('image')
    proposals = SharedMultipleProperty('proposals', 'challenge')
    ideas = SharedMultipleProperty('ideas', 'challenge')
    questions = SharedMultipleProperty('questions', 'challenge')
    attached_files = CompositeMultipleProperty('attached_files')
    invited_users = SharedMultipleProperty('invited_users')
    url_files = CompositeMultipleProperty('url_files')

    def __init__(self, **kwargs):
        super(Challenge, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.addtoproperty('channels', Channel())
        self.urls = PersistentDict({})

    def __setattr__(self, name, value):
        super(Challenge, self).__setattr__(name, value)
        if name in ('deadline', 'published_at', 'created_at') and value:
            self.init_total_days()

    @property
    def related_contents(self):
        return [content[0] for content in self.all_related_contents]

    @property
    def challenge(self):
        return self

    @property
    def transformed_from(self):
        """Return all related contents"""
        transformed_from = [correlation[1].context for correlation
                            in self.get_related_contents(
                                CorrelationType.solid, ['transformation'])
                            if correlation[1].context]
        return transformed_from[0] if transformed_from else None

    @property
    def is_expired(self):
        if 'closed' in self.state:
            return True

        deadline = getattr(self, 'deadline', None)
        if deadline is not None:
            now = datetime.datetime.now(tz=pytz.UTC)
            return now.date() >= deadline

        return False

    @property
    def can_add_content(self):
        return not self.is_expired and 'pending' in self.state

    @property
    def remaining_duration(self):
        deadline = getattr(self, 'deadline', None)
        duration = getattr(self, 'duration', None)
        if deadline is not None and duration is not None:
            now = datetime.datetime.now(tz=pytz.UTC)
            remaining = (deadline - now.date()).days
            return remaining if remaining >= 0 else 0

        return None

    def init_published_at(self):
        setattr(self, 'published_at', datetime.datetime.now(tz=pytz.UTC))

    def init_support_history(self):
        if not hasattr(self, '_support_history'):
            setattr(self, '_support_history', PersistentList())

    def init_total_days(self):
        deadline = getattr(self, 'deadline', None)
        date = getattr(self, 'published_at', None)
        date = date if date else getattr(self, 'created_at', None)
        if deadline is not None and date is not None:
            duration = (deadline - date.date()).days
            setattr(self, 'duration', duration)

    def get_attached_files_data(self):
        return get_files_data(self.attached_files)

    def get_all_attached_files_data(self):
        files = list(self.attached_files)
        files.append(self.image)
        return get_files_data(files)

    def get_node_descriminator(self):
        return 'challenge'

    def format(self, request):
        text = getattr(self, 'text', '')
        all_urls, url_files, text_urls, formatted_text = text_urls_format(
            text, request, True)
        self.urls = PersistentDict(all_urls)
        self.setproperty('url_files', url_files)
        self.formatted_text = formatted_text
        self.formatted_urls = text_urls
