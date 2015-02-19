# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from webob.multidict import MultiDict
from zope.interface import implementer

from substanced.content import content
from substanced.schema import NameSchemaNode
from substanced.util import renamer

from dace.descriptors import SharedUniqueProperty, CompositeMultipleProperty
from pontus.core import VisualisableElementSchema
from pontus.widget import (
    SequenceWidget,
    FileWidget)
from pontus.file import ObjectData, File

from .interface import Iidea
from novaideo.content.correlation import CorrelationType
from novaideo.core import Commentable
from novaideo import _
from novaideo.views.widget import LimitedTextAreaWidget
from novaideo.core import (
    VersionableEntity,
    DuplicableEntity,
    SearchableEntity,
    SearchableEntitySchema,
    CorrelableEntity,
    PresentableEntity)



def context_is_a_idea(context, request):
    return request.registry.content.istype(context, 'idea')


class IdeaSchema(VisualisableElementSchema, SearchableEntitySchema):
    """Schema for idea"""

    name = NameSchemaNode(
        editing=context_is_a_idea,
        )

    text = colander.SchemaNode(
        colander.String(),
        widget=LimitedTextAreaWidget(rows=5, 
                                     cols=30, 
                                     limit=600,
                                     alert_template='novaideo:views/templates/idea_text_alert.pt',
                                     alert_values={'limit': 600}),
        title=_("Text")
        )

    note = colander.SchemaNode(
        colander.String(),
        widget=LimitedTextAreaWidget(rows=5, 
                                     cols=30, 
                                     limit=300,
                                     alert_values={'limit': 300}),
        title=_("Note"),
        #missing=""
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

    icon = 'novaideo:static/images/idea_picto32.png'
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
        return MultiDict([(c.source, c) for c in self.target_correlations\
                if ((c.type==CorrelationType.solid) and \
                    ('related_proposals' in c.tags))])
