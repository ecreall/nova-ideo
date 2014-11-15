# -*- coding: utf8 -*-
import colander
import deform.widget
from webob.multidict import MultiDict
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.util import getSite
from dace.descriptors import SharedUniqueProperty, CompositeMultipleProperty
from pontus.core import VisualisableElementSchema
from pontus.widget import (
    RichTextWidget,
    Select2Widget,
    SequenceWidget,
    FileWidget)
from pontus.file import ObjectData, File

from .interface import Iidea
from novaideo.content.correlation import CorrelationType
from novaideo.core import Commentable
from novaideo import _
from novaideo.core import (
    VersionableEntity,
    DuplicableEntity,
    SearchableEntity,
    SearchableEntitySchema,
    CorrelableEntity,
    PresentableEntity)


@colander.deferred
def intention_choice(node, kw):
    root = getSite()
    intentions = sorted(root.idea_intentions)
    values = [(str(i), i) for i in intentions ]
    values.insert(0, ('', _('- Select -')))
    return Select2Widget(values=values)


def context_is_a_idea(context, request):
    return request.registry.content.istype(context, 'idea')


class IdeaSchema(VisualisableElementSchema, SearchableEntitySchema):
    """Schema for idea"""

    name = NameSchemaNode(
        editing=context_is_a_idea,
        )

    description = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=300),
        widget=deform.widget.TextAreaWidget(rows=5, cols=30),
        title=_("Abstract"),
        description=_("(300 caracteres maximum)")
        )

    text = colander.SchemaNode(
        colander.String(),
        widget= RichTextWidget(),
        title=_('Text'),
        missing='',
        )

    intention = colander.SchemaNode(
        colander.String(),
        widget=intention_choice,
        title=_('Intention'),
        default=_('Improvement'),
        missing='Improvement'
        )

    attached_files = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            ObjectData(File),
            name=_("File"),
            widget=FileWidget()
            ),
        widget=SequenceWidget(add_subitem_text_template = _('Add file')),
        missing=[],
        title=_('Attached files'),
        )


@content(
    'idea',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(Iidea)
class Idea(Commentable, VersionableEntity, DuplicableEntity,
           SearchableEntity, CorrelableEntity, PresentableEntity):
    """Idea class""" 

    result_template = 'novaideo:views/templates/idea_result.pt'
    template = 'novaideo:views/templates/idea_list_element.pt'
    name = renamer()
    author = SharedUniqueProperty('author', 'ideas')
    attached_files = CompositeMultipleProperty('attached_files')

    def __init__(self, **kwargs):
        super(Idea, self).__init__(**kwargs)
        self.set_data(kwargs)

    @property
    def related_proposals(self):
        """Return all proposals that uses this idea"""
        return MultiDict([(c.source, c) for c in self.source_correlations\
                if ((c.type==CorrelationType.solid) and \
                    ('related_proposals' in c.tags))])
