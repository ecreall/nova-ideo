# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
"""
This module represent the Idea management process definition 
powered by the dace engine. This process is unique, which means that 
this process is instantiated only once.
"""
from dace.processdefinition.processdef import ProcessDefinition
from dace.processdefinition.activitydef import ActivityDefinition
from dace.processdefinition.gatewaydef import (
    ExclusiveGatewayDefinition,
    ParallelGatewayDefinition)
from dace.processdefinition.transitiondef import TransitionDefinition
from dace.processdefinition.eventdef import (
    StartEventDefinition,
    EndEventDefinition)
from dace.objectofcollaboration.services.processdef_container import (
  process_definition)
from pontus.core import VisualisableElement

from .behaviors import (
    CreateIdea,
    DuplicateIdea,
    DelIdea,
    EditIdea,
    PublishIdea,
    RecuperateIdea,
    AbandonIdea,
    CommentIdea,
    PresentIdea,
    Associate,
    SeeIdea,
    CompareIdea)
from novaideo import _


@process_definition(name='ideamanagement', id='ideamanagement')
class IdeaManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(IdeaManagement, self).__init__(**kwargs)
        self.title = _('Ideas management')
        self.description = _('Ideas management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                #egs = ExclusiveGatewayDefinition(),
                creat = ActivityDefinition(contexts=[CreateIdea],
                                       description=_("Create an idea"),
                                       title=_("Create an idea"),
                                       groups=[_('Add')]),
                duplicate = ActivityDefinition(contexts=[DuplicateIdea],
                                       description=_("Duplicate this idea"),
                                       title=_("Duplicate"),
                                       groups=[]),
                delidea = ActivityDefinition(contexts=[DelIdea],
                                       description=_("Delete the idea"),
                                       title=_("Delete"),
                                       groups=[]),
                edit = ActivityDefinition(contexts=[EditIdea],
                                       description=_("Edit the idea"),
                                       title=_("Edit"),
                                       groups=[]),
                publish = ActivityDefinition(contexts=[PublishIdea],
                                       description=_("Publish the idea"),
                                       title=_("Publish"),
                                       groups=[]),
                recuperate = ActivityDefinition(contexts=[RecuperateIdea],
                                       description=_("Recuperate the idea"),
                                       title=_("Recuperate"),
                                       groups=[]),
                abandon = ActivityDefinition(contexts=[AbandonIdea],
                                       description=_("Archive the idea"),
                                       title=_("Archive"),
                                       groups=[]),
                present = ActivityDefinition(contexts=[PresentIdea],
                                       description=_("Submit the idea to others"),
                                       title=_("Submit to others"),
                                       groups=[]),
                comment = ActivityDefinition(contexts=[CommentIdea],
                                       description=_("Discuss the idea"),
                                       title=_("Discuss"),
                                       groups=[]),
                associate = ActivityDefinition(contexts=[Associate],
                                       description=_("Associate the idea"),
                                       title=_("Associate"),
                                       groups=[]),
                see = ActivityDefinition(contexts=[SeeIdea],
                                       description=_("Details"),
                                       title=_("Details"),
                                       groups=[]),
                compare = ActivityDefinition(contexts=[CompareIdea],
                                       description=_("Compare versions"),
                                       title=_("Compare"),
                                       groups=[]),
                pg = ParallelGatewayDefinition(),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'creat'),
                TransitionDefinition('pg', 'duplicate'),
                TransitionDefinition('pg', 'edit'),
                TransitionDefinition('pg', 'publish'),
                TransitionDefinition('pg', 'delidea'),
                TransitionDefinition('pg', 'abandon'),
                TransitionDefinition('pg', 'recuperate'),
                TransitionDefinition('pg', 'comment'),
                TransitionDefinition('pg', 'present'),
                TransitionDefinition('pg', 'associate'),
                TransitionDefinition('pg', 'see'),
                TransitionDefinition('pg', 'compare'),
                TransitionDefinition('creat', 'eg'),
                TransitionDefinition('duplicate', 'eg'),
                TransitionDefinition('recuperate', 'eg'),
                TransitionDefinition('abandon', 'eg'),
                TransitionDefinition('publish', 'eg'),
                TransitionDefinition('delidea', 'eg'),
                TransitionDefinition('edit', 'eg'),
                TransitionDefinition('comment', 'eg'),
                TransitionDefinition('present', 'eg'),
                TransitionDefinition('associate', 'eg'),
                TransitionDefinition('see', 'eg'),
                TransitionDefinition('compare', 'eg'),
                TransitionDefinition('eg', 'end'),
        )
