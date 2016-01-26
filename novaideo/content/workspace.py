# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from zope.interface import implementer

from substanced.content import content
from substanced.util import renamer
from substanced.schema import NameSchemaNode

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import (
    SharedUniqueProperty,
    CompositeMultipleProperty)
from pontus.widget import (
    SequenceWidget)
from pontus.file import ObjectData, File

from pontus.core import VisualisableElement, VisualisableElementSchema

from novaideo import _
from .interface import IWorkspace
from novaideo.content import get_file_widget


def context_is_a_workspace(context, request):
    return request.registry.content.istype(context, 'workspace')


class WorkspaceSchema(VisualisableElementSchema):
    """Schema for working group"""

    name = NameSchemaNode(
        editing=context_is_a_workspace,
        )

    files = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            ObjectData(File),
            name=_("File"),
            widget=get_file_widget()
            ),
        widget=SequenceWidget(
            add_subitem_text_template=_('Add file')),
        missing=[],
        title=_('Attached files'),
        )


@content(
    'workspace',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IWorkspace)
class Workspace(VisualisableElement, Entity):
    """Working group class"""

    name = renamer()
    type_title = _('Workspace')
    template = 'pontus:templates/visualisable_templates/object.pt'
    files = CompositeMultipleProperty('files')
    working_group = SharedUniqueProperty('working_group', 'workspace')

    def __init__(self, **kwargs):
        super(Workspace, self).__init__(**kwargs)
        self.set_data(kwargs)

    @property
    def proposal(self):
        return self.working_group.proposal
