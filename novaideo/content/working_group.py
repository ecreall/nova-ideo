from zope.interface import implementer

from substanced.content import content
from substanced.util import renamer
from substanced.schema import NameSchemaNode

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import (
    SharedMultipleProperty, 
    SharedUniqueProperty, 
    CompositeMultipleProperty)
from pontus.core import VisualisableElement, VisualisableElementSchema

from .interface import IWorkingGroup


def context_is_a_workinggroup(context, request):
    return request.registry.content.istype(context, 'workinggroup')


class WorkingGroupSchema(VisualisableElementSchema):
    """Schema for working group"""

    name = NameSchemaNode(
        editing=context_is_a_workinggroup,
        )


@content(
    'workinggroup',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IWorkingGroup)
class WorkingGroup(VisualisableElement, Entity):
    """Working group class"""

    name = renamer()
    template = 'pontus:templates/visualisable_templates/object.pt'
    proposal = SharedUniqueProperty('proposal', 'working_group')
    members = SharedMultipleProperty('members', 'working_groups')
    wating_list = SharedMultipleProperty('wating_list')
    ballots = CompositeMultipleProperty('ballots')
