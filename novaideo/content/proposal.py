# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
import colander
from collections import OrderedDict
from persistent.list import PersistentList
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer, get_oid

from dace.util import get_obj, getSite, copy
from dace.descriptors import (
    CompositeMultipleProperty,
    SharedUniqueProperty,
    SharedMultipleProperty)
from pontus.widget import (
    RichTextWidget, AjaxSelect2Widget,
    Length, SequenceWidget, Select2Widget)
from pontus.file import ObjectData, File, Object as ObjectType
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
    ExaminableEntity,
    Node,
    Emojiable,
    SignalableEntity,
    Debatable,
    Tokenable)
from novaideo.views.widget import SimpleMappingtWidget
from novaideo.content import get_file_widget
from novaideo.utilities.util import (
    connect, disconnect, get_files_data)


OPINIONS = OrderedDict([
    ('favorable', _('Positive')),
    ('to_study', _('To be re-worked upon')),
    ('unfavorable', _('Negative'))
])


@colander.deferred
def challenge_choice(node, kw):
    request = node.bindings['request']
    root = getSite()
    values = [('', _('- Select -'))]

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
    return AjaxSelect2Widget(
        values=values,
        ajax_url=ajax_url,
        ajax_item_template="related_item_template",
        title_getter=title_getter,
        multiple=False,
        page_limit=20,
        add_clear=True,
        item_css_class='challenge-input')


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
        add_clear=True,
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
        title=_("Connect to the files of the workspace")
        )

    attached_files = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            ObjectData(File),
            name=_("File"),
            widget=get_file_widget()
            ),
        widget=SequenceWidget(
            add_subitem_text_template=_('Upload a new file'),
            item_css_class='files-block'),
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

    challenge = colander.SchemaNode(
        ObjectType(),
        widget=challenge_choice,
        missing=None,
        title=_("Challenge (optional)"),
        description=_("You can select and/or modify the challenge associated to this proposal. "
                      "For an open proposal, do not select anything in the « Challenge » field.")
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
               ExaminableEntity,
               Node,
               Emojiable,
               SignalableEntity,
               Debatable,
               Tokenable):
    """Proposal class"""

    type_title = _('Proposal')
    icon = 'icon novaideo-icon icon-proposal'
    templates = {'default': 'novaideo:views/templates/proposal_result.pt',
                 'small': 'novaideo:views/templates/small_proposal_result.pt',
                 'popover': 'novaideo:views/templates/proposal_popover.pt',
                 'bloc': 'novaideo:views/templates/proposal_bloc.pt'}
    template = 'novaideo:views/templates/proposal_list_element.pt'
    name = renamer()
    author = SharedUniqueProperty('author')
    organization = SharedUniqueProperty('organization')
    working_group = SharedUniqueProperty('working_group', 'proposal')
    amendments = CompositeMultipleProperty('amendments', 'proposal')
    corrections = CompositeMultipleProperty('corrections', 'proposal')
    attached_files = SharedMultipleProperty('attached_files')
    challenge = SharedUniqueProperty('challenge', 'proposals')
    opinions_base = OPINIONS

    def __init__(self, **kwargs):
        super(Proposal, self).__init__(**kwargs)
        self.set_data(kwargs)
        self._amendments_counter = 1
        self.addtoproperty('channels', Channel())

    @property
    def related_ideas(self):
        return [idea[0] for idea in self.get_related_contents(
            CorrelationType.solid, ['related_ideas'])]

    @property
    def related_contents(self):
        return [content[0] for content in self.all_related_contents]

    @property
    def is_published(self):
        return 'published' in self.state

    @property
    def authors(self):
        return self.working_group.members

    @property
    def workspace(self):
        working_group = self.working_group
        if working_group:
            return working_group.workspace

        if self.current_version is not self:
            return getattr(self.current_version, 'workspace', None)

        return None

    def __setattr__(self, name, value):
        super(Proposal, self).__setattr__(name, value)
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
        return get_files_data(self.attached_files)

    def set_related_ideas(self, relatedideas, user):
        current_related_ideas = self.related_ideas
        related_ideas_to_add = [i for i in relatedideas
                                if i not in current_related_ideas]
        related_ideas_to_del = [i for i in current_related_ideas
                                if i not in relatedideas and
                                i not in related_ideas_to_add]
        connect(self,
                related_ideas_to_add,
                {'comment': _('Add related ideas'),
                 'type': _('Edit the proposal')},
                user,
                ['related_proposals', 'related_ideas'],
                CorrelationType.solid,
                True)
        disconnect(self,
                   related_ideas_to_del,
                   'related_ideas',
                   CorrelationType.solid)

    def get_version(self, user, parent):
        old_version = self.version
        copy_of_proposal = copy(
            self, parent,
            omit=('len_selections', 'graph'),
            roles=True)
        if old_version:
            copy_of_proposal.setproperty('version', old_version)

        copy_of_proposal.init_graph()
        copy_of_proposal.state = PersistentList(['version', 'archived'])
        copy_of_proposal.setproperty('author', self.author)
        copy_of_proposal.setproperty('originalentity', self.originalentity)
        for amendment in self.amendments:
            copy_of_proposal.addtoproperty('amendments', amendment)

        for correction in self.corrections:
            copy_of_proposal.addtoproperty('corrections', correction)

        for file_ in self.attached_files:
            copy_of_proposal.addtoproperty('attached_files', file_)

        copy_of_proposal.set_related_ideas(
            self.related_ideas, user)
        copy_of_proposal.reindex()
        return copy_of_proposal

    def get_token(self, user):
        tokens = [t for t in getattr(user, 'tokens', []) if
                  not t.proposal or t.proposal is self]
        proposal_tokens = [t for t in tokens if t.proposal is self]
        if proposal_tokens:
            return proposal_tokens[0]

        return tokens[-1] if tokens else None

    def remove_tokens(self):
        tokens = [t for t in self.tokens if not t.proposal]
        proposal_tokens = [t for t in self.tokens if t.proposal]
        for token in list(tokens):
            token.owner.addtoproperty('tokens', token)

        for proposal_token in list(proposal_tokens):
            proposal_token.owner.delfromproperty('tokens_ref', proposal_token)
            self.__delitem__(proposal_token.__name__)

        members = self.working_group.members
        for member in members:
            to_remove = [t for t in member.tokens
                         if t.proposal is self]
            if to_remove:
                token = to_remove[0]
                token.owner.delfromproperty('tokens_ref', token)

    def get_node_descriminator(self):
        return 'proposal'
