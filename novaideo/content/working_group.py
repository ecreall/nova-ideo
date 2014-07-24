import colander
from zope.interface import invariant, implementer, Interface

from substanced.content import content
from substanced.util import renamer
from substanced.property import PropertySheet
from substanced.schema import (
    NameSchemaNode
    )

from dace.objectofcollaboration.entity import Entity
from dace.objectofcollaboration.object import(
                COMPOSITE_UNIQUE,
                SHARED_UNIQUE,
                COMPOSITE_MULTIPLE,
                SHARED_MULTIPLE,
                Object)
from pontus.schema import Schema, omit
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import TableWidget, LineWidget, CheckboxChoiceWidget

from .action_proposal import ActionProposalSchema, ActionProposal
from .interface import IWorkingGroup


def context_is_a_workinggroup(context, request):
    return request.registry.content.istype(context, 'workinggroup')


class WorkingGroupSchema(VisualisableElementSchema):

    name = NameSchemaNode(
        editing=context_is_a_workinggroup,
        )

    action_proposal = omit(ActionProposalSchema(name='action proposal',
                                                factory=ActionProposal,
                                                editable=True),['_csrf_token_'])


@content(
    'workinggroup',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IWorkingGroup)
class WorkingGroup(VisualisableElement, Entity):
    name = renamer()
    template = 'pontus:templates/visualisable_templates/object.pt'
    properties_def = {'action_proposal':(COMPOSITE_UNIQUE, 'myparent', False)}

    def __init__(self, **kwargs):
        super(WorkingGroup, self).__init__(**kwargs)

    @property
    def action_proposal(self):
        return self.getproperty('action_proposal')

    def setaction_proposal(self, action_proposal):
        self.setproperty('action_proposal', action_proposal)


