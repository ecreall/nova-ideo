# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
import colander
from collections import OrderedDict
from webob.multidict import MultiDict
from persistent.list import PersistentList
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer, get_oid

from dace.util import get_obj, getSite
from dace.descriptors import (
    CompositeMultipleProperty,
    SharedUniqueProperty,
    SharedMultipleProperty)
from pontus.widget import (
    RichTextWidget, AjaxSelect2Widget,
    Length, SequenceWidget, Select2Widget)
from pontus.file import ObjectData, File
from pontus.core import VisualisableElementSchema
from pontus.schema import omit, Schema

from .interface import IProposal
from novaideo.content.correlation import CorrelationType
from novaideo import _, log
from novaideo.views.widget import LimitedTextAreaWidget
from novaideo.core import (
    SearchableEntity,
    Channel,
    SearchableEntitySchema,
    CorrelableEntity,
    DuplicableEntity,
    VersionableEntity,
    PresentableEntity,
    Node)
from novaideo.views.widget import SimpleMappingtWidget
from novaideo.content import get_file_widget


OPINIONS = OrderedDict([
    ('favorable', _('Favorable')),
    ('to_study', _('To study')),
    ('unfavorable', _('Unfavorable'))
])


@colander.deferred
def ideas_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = []
    ajax_url = request.resource_url(context,
                                    '@@novaideoapi',
                                    query={'op': 'find_ideas'})

    def title_getter(oid):
        try:
            obj = get_obj(int(oid), None)
            if obj:
                return obj.title
            else:
                return oid
        except Exception as e:
            log.warning(e)
            return oid

    return AjaxSelect2Widget(
        values=values,
        ajax_url=ajax_url,
        multiple=True,
        title_getter=title_getter,
        )


@colander.deferred
def files_choice(node, kw):
    context = node.bindings['context']
    values = []
    root = getSite()
    if context is not root:
        workspace = context.working_group.workspace
        values = [(get_oid(file_), file_.title) for file_ in workspace.files]

    return Select2Widget(
        values=values,
        multiple=True
        )


class AddFilesSchemaSchema(Schema):
    """Schema for interview"""

    ws_files = colander.SchemaNode(
        colander.Set(),
        widget=files_choice,
        missing=[],
        title=_("Connect to workspace's files")
        )

    attached_files = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            ObjectData(File),
            name=_("File"),
            widget=get_file_widget()
            ),
        widget=SequenceWidget(
            add_subitem_text_template=_('Upload a new file')),
        missing=[],
        title=_('Upload new files'),
        )


def context_is_a_proposal(context, request):
    return request.registry.content.istype(context, 'proposal')


class ProposalSchema(VisualisableElementSchema, SearchableEntitySchema):
    """Schema for Proposal"""

    name = NameSchemaNode(
        editing=context_is_a_proposal,
        )

    description = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=600),
        widget=LimitedTextAreaWidget(rows=5,
                                     cols=30,
                                     limit=600),
        title=_("Abstract")
        )

    text = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget(),
        title=_("Text")
        )

    related_ideas = colander.SchemaNode(
        colander.Set(),
        widget=ideas_choice,
        title=_('Related ideas'),
        validator=Length(_, min=1),
        default=[],
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
    'proposal',
    icon='icon novaideo-icon icon-proposal',
    )
@implementer(IProposal)
class Proposal(VersionableEntity,
               SearchableEntity,
               DuplicableEntity,
               CorrelableEntity,
               PresentableEntity,
               Node):
    """Proposal class"""

    type_title = _('Proposal')
    icon = 'icon novaideo-icon icon-proposal'
    templates = {'default': 'novaideo:views/templates/proposal_result.pt',
                 'small': 'novaideo:views/templates/small_proposal_result.pt'}
    template = 'novaideo:views/templates/proposal_list_element.pt'
    name = renamer()
    author = SharedUniqueProperty('author')
    working_group = SharedUniqueProperty('working_group', 'proposal')
    tokens_opposition = CompositeMultipleProperty('tokens_opposition')
    tokens_support = CompositeMultipleProperty('tokens_support')
    amendments = CompositeMultipleProperty('amendments', 'proposal')
    corrections = CompositeMultipleProperty('corrections', 'proposal')
    attached_files = SharedMultipleProperty('attached_files')

    def __init__(self, **kwargs):
        super(Proposal, self).__init__(**kwargs)
        self.set_data(kwargs)
        self._amendments_counter = 1
        self.addtoproperty('channels', Channel())

    @property
    def related_ideas(self):
        lists_targets = [(c.targets, c) for c in self.source_correlations
                         if c.type == CorrelationType.solid and
                         'related_ideas' in c.tags]
        return MultiDict([(target, c) for targets, c in lists_targets
                          for target in targets])

    @property
    def tokens(self):
        result = list(self.tokens_opposition)
        result.extend(list(self.tokens_support))
        return result

    @property
    def opinion_value(self):
        return OPINIONS.get(
            getattr(self, 'opinion', {}).get('opinion', ''), None)

    @property
    def is_published(self):
        return 'published' in self.state

    @property
    def authors(self):
        return self.working_group.members

    def init_published_at(self):
        setattr(self, 'published_at', datetime.datetime.now(tz=pytz.UTC))

    def init_examined_at(self):
        setattr(self, 'examined_at', datetime.datetime.now(tz=pytz.UTC))

    def init_support_history(self):
        # [(user_oid, date, support_type), ...], support_type = {1:support, 0:oppose, -1:withdraw}
        if not hasattr(self, '_support_history'):
            setattr(self, '_support_history', PersistentList())

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

    def get_nodes_data(self, calculated=[]):
        oid = self.get_node_id()
        newcalculated = list(calculated)
        if oid in calculated:
            return {}, newcalculated

        related_ideas = self.related_ideas
        result = {oid: {
            'oid': self.__oid__,
            'title': self.title,
            'descriminator': 'proposal',
            'targets': [t.get_node_id()
                        for t in related_ideas]
        }}

        newcalculated.append(oid)
        for idea in related_ideas:
            sub_result, newcalculated = idea.get_nodes_data(newcalculated)
            result.update(sub_result)

        return result, newcalculated
