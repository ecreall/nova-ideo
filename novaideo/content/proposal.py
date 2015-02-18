# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from collections import OrderedDict
from webob.multidict import MultiDict
from persistent.list import PersistentList
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import getSite
from dace.objectofcollaboration.principal.util import get_current
from dace.descriptors import (
    CompositeMultipleProperty,
    SharedUniqueProperty)
from pontus.widget import RichTextWidget, Select2Widget, Length
from pontus.core import VisualisableElementSchema

from .interface import IProposal
from novaideo.content.correlation import CorrelationType
from novaideo.core import Commentable, can_access
from novaideo import _
from novaideo.views.widget import LimitedTextAreaWidget
from novaideo.core import (
    SearchableEntity,
    SearchableEntitySchema,
    CorrelableEntity,
    DuplicableEntity,
    VersionableEntity,
    PresentableEntity)


OPINIONS = OrderedDict([
            ('favorable', _('Favorable')),
            ('to_study', _('To study')),
            ('unfavorable', _('Unfavorable'))
           ])


@colander.deferred
def ideas_choice(node, kw):
    root = getSite()
    user = get_current()
    values = [(i, i.title) for i in root.ideas \
              if can_access(user, i) and not('archived' in i.state)]
    return Select2Widget(values=values, multiple=True)


def context_is_a_proposal(context, request):
    return request.registry.content.istype(context, 'proposal')



class ProposalSchema(VisualisableElementSchema, SearchableEntitySchema):
    """Schema for Proposal"""

    name = NameSchemaNode(
        editing=context_is_a_proposal,
        )

    description = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=300),
        widget=LimitedTextAreaWidget(rows=5, 
                                     cols=30, 
                                     limit=300),
        title=_("Abstract")
        )

    text = colander.SchemaNode(
        colander.String(),
        widget= RichTextWidget(),
        title=_("Text")
        )

    related_ideas  = colander.SchemaNode(
        colander.Set(),
        widget=ideas_choice,
        title=_('Related ideas'),
        validator = Length(_, min=1),
        default=[],
        )


@content(
    'proposal',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IProposal)
class Proposal(Commentable,
               VersionableEntity,
               SearchableEntity, 
               DuplicableEntity, 
               CorrelableEntity, 
               PresentableEntity):
    """Proposal class"""

    icon = 'novaideo:static/images/proposal_picto32.png'
    result_template = 'novaideo:views/templates/proposal_result.pt'
    template = 'novaideo:views/templates/proposal_list_element.pt'
    name = renamer()
    author = SharedUniqueProperty('author')
    working_group = SharedUniqueProperty('working_group', 'proposal')
    tokens_opposition = CompositeMultipleProperty('tokens_opposition')
    tokens_support = CompositeMultipleProperty('tokens_support')
    amendments = CompositeMultipleProperty('amendments', 'proposal')
    corrections = CompositeMultipleProperty('corrections', 'proposal')


    def __init__(self, **kwargs):
        super(Proposal, self).__init__(**kwargs)
        self.set_data(kwargs)
        # [(user_oid, date, support_type), ...], support_type = {1:support, 0:oppose, -1:withdraw}
        self._support_history = PersistentList()
        self._amendments_counter = 1

    @property
    def related_ideas(self):
        lists_targets = [(c.targets, c) for c in self.source_correlations \
                          if ((c.type==CorrelationType.solid) and \
                              ('related_ideas' in c.tags))]
        return MultiDict([(target, c) for targets, c in lists_targets \
                     for target in targets])

    @property
    def tokens(self):
        result = list(self.tokens_opposition)
        result.extend(list(self.tokens_support))
        return result

    @property
    def opinion_value(self):
        return OPINIONS.get(getattr(self, 'opinion', None), None)