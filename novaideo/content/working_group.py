# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from zope.interface import implementer
from persistent.list import PersistentList

from substanced.content import content
from substanced.util import renamer
from substanced.schema import NameSchemaNode

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import (
    SharedMultipleProperty,
    SharedUniqueProperty,
    CompositeMultipleProperty,
    CompositeUniqueProperty)
from dace.objectofcollaboration.principal.util import (
    revoke_roles)
from pontus.core import VisualisableElement, VisualisableElementSchema

from .interface import IWorkingGroup
from .workspace import Workspace
from novaideo.content.processes.proposal_management import WORK_MODES
from novaideo.content.processes import get_states_mapping


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
    improvement_cycle_proc = SharedUniqueProperty('improvement_cycle_proc')
    workspace = CompositeUniqueProperty('workspace', 'working_group')

    def init_workspace(self):
        self.addtoproperty('workspace', Workspace(title="Workspace"))

    @property
    def work_mode(self):
        mode_id = getattr(self, 'work_mode_id', None)
        if mode_id:
            return WORK_MODES.get(mode_id, None)

        root = self.__parent__
        if hasattr(root, 'get_work_modes') and len(root.get_work_modes()) == 1:
            return root.get_default_work_mode()

        return None

    @property
    def challenge(self):
        return getattr(self.proposal, 'challenge', None)

    def get_state(self, request, user):
        return get_states_mapping(
            user, self,
            getattr(self, 'state_or_none', [None])[0])

    def empty(self, remove_author=True):
        author = self.proposal.author
        self.state = PersistentList(['deactivated'])
        self.setproperty('wating_list', [])
        if hasattr(self, 'first_improvement_cycle'):
            del self.first_improvement_cycle

        if hasattr(self, 'first_vote'):
            del self.first_vote

        members = self.members
        if remove_author and author in members:
            members.remove(author)

        for member in members:
            self.delfromproperty('members', member)
            revoke_roles(member, (('Participant', self.proposal),))

        self.init_nonproductive_cycle()

    def inc_iteration(self):
        self.iteration = getattr(self, 'iteration', 0) + 1

    def init_nonproductive_cycle(self):
        self.nonproductive_cycle = 0

    def inc_nonproductive_cycle(self):
        self.nonproductive_cycle = getattr(self, 'nonproductive_cycle', 0) + 1
