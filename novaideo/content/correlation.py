# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from zope.interface import implementer
from persistent.list import PersistentList

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.objectofcollaboration.entity import Entity
from dace.util import get_obj, getSite
from dace.descriptors import (
    SharedUniqueProperty, SharedMultipleProperty,
    CompositeMultipleProperty)
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import Select2Widget, AjaxSelect2Widget
from pontus.file import Object as ObjectType

from .interface import ICorrelation
from novaideo.core import Channel, Debatable
from novaideo import _, log


class CorrelationType:
    weak = 0
    solid = 1

    @classmethod
    def type_name(cls, value):
        if value == 0:
            return 'weak'

        if value == 1:
            return 'solid'

        return None


@colander.deferred
def targets_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = []
    ajax_url = request.resource_url(context,
                                    '@@novaideoapi',
                                    query={'op': 'find_correlable_entity'})

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
def intention_choice(node, kw):
    root = getSite()
    intentions = sorted(root.correlation_intentions)
    values = [(i, i) for i in intentions]
    values.insert(0, ('', _('- Select -')))
    return Select2Widget(values=values)


def context_is_a_correlation(context, request):
    return request.registry.content.istype(context, 'correlation')


class CorrelationSchema(VisualisableElementSchema):
    """Schema for correlation"""

    name = NameSchemaNode(
        editing=context_is_a_correlation,
        )

    intention = colander.SchemaNode(
        colander.String(),
        widget=intention_choice,
        title=_('Intention'),
        )

    comment = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=500),
        widget=deform.widget.TextAreaWidget(rows=4, cols=60),
        title=_("Message")
        )

    targets = colander.SchemaNode(
        ObjectType(),
        widget=targets_choice,
        validator=colander.Length(min=1),
        title=_('Targets'),
        )


@content(
    'correlation',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(ICorrelation)
class Correlation(Debatable):
    """Correlation class"""
    name = renamer()
    source = SharedUniqueProperty('source', 'source_correlations')
    targets = SharedMultipleProperty('targets', 'target_correlations')
    context = SharedUniqueProperty('context', 'contextualized_correlations')
    author = SharedUniqueProperty('author')
    comments = CompositeMultipleProperty('comments')

    def __init__(self, **kwargs):
        super(Correlation, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.type = CorrelationType.weak
        self.tags = PersistentList()
        # self.addtoproperty('channels', Channel(title=_("General")))

    @property
    def ends(self):
        """Return the ends of the correlation"""
        result = list(self.targets)
        result .append(self.source)
        return result

    @property
    def type_name(self):
        return CorrelationType.type_name(self.type)
