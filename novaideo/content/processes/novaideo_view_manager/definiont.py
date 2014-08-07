from dace.interfaces import IProcessDefinition
from dace.processdefinition.processdef import ProcessDefinition
from dace.processdefinition.activitydef import ActivityDefinition
from dace.processdefinition.gatewaydef import (
    ExclusiveGatewayDefinition, 
    ParallelGatewayDefinition)
from dace.processdefinition.transitiondef import TransitionDefinition
from dace.processdefinition.eventdef import (
    StartEventDefinition,
    EndEventDefinition,
    IntermediateCatchEventDefinition,
    ConditionalEventDefinition,
    TimerEventDefinition)
from dace.objectofcollaboration.services.processdef_container import process_definition

from pontus.core import VisualisableElement

from .behaviors import (
    SeeIdeas,
    Search,
    SeeMyIdeas,
    SeeMycontacts,
    SeeMyProposals,
    SeeMySelections,
    SeeMyParticipations,
    SeeMySupports)
from novaideo import _


@process_definition(name='novaideoviewmanager', id='novaideoviewmanager')
class NovaIdeoViewManager(ProcessDefinition, VisualisableElement):
    isUnique = True
    isVolatile = True

    def __init__(self, **kwargs):
        super(NovaIdeoViewManager, self).__init__(**kwargs)
        self.title = _('User access manager')
        self.description = _('User access manager')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                seeideas = ActivityDefinition(contexts=[SeeIdeas],
                                       description=_("See ideas"),
                                       title=_("Ideas"),
                                       groups=[]),
                search = ActivityDefinition(contexts=[Search],
                                       description=_("Search"),
                                       title=_("Search"),
                                       groups=[]),
                myideas = ActivityDefinition(contexts=[SeeMyIdeas],
                                       description=_("See my ideas"),
                                       title=_("My ideas"),
                                       groups=[]),
                mycontacts = ActivityDefinition(contexts=[SeeMycontacts],
                                       description=_("See my contacts"),
                                       title=_("My contacts"),
                                       groups=[]),
                myproposals = ActivityDefinition(contexts=[SeeMyProposals],
                                       description=_("See my proposals"),
                                       title=_("My proposals"),
                                       groups=[]),
                myselections = ActivityDefinition(contexts=[SeeMySelections],
                                       description=_("See my selections"),
                                       title=_("My selections"),
                                       groups=[]),
                myparticipations = ActivityDefinition(contexts=[SeeMyParticipations],
                                       description=_("See my participations"),
                                       title=_("My participations"),
                                       groups=[]),
                mysupports = ActivityDefinition(contexts=[SeeMySupports],
                                       description=_("See my supports"),
                                       title=_("My supports"),
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'seeideas'),
                TransitionDefinition('seeideas', 'eg'),
                TransitionDefinition('pg', 'search'),
                TransitionDefinition('search', 'eg'),
                TransitionDefinition('pg', 'myideas'),
                TransitionDefinition('myideas', 'eg'),
                TransitionDefinition('pg', 'mycontacts'),
                TransitionDefinition('mycontacts', 'eg'),
                TransitionDefinition('pg', 'myproposals'),
                TransitionDefinition('myproposals', 'eg'),
                TransitionDefinition('pg', 'myselections'),
                TransitionDefinition('myselections', 'eg'),
                TransitionDefinition('pg', 'myparticipations'),
                TransitionDefinition('myparticipations', 'eg'),
                TransitionDefinition('pg', 'mysupports'),
                TransitionDefinition('mysupports', 'eg'),
                TransitionDefinition('eg', 'end'),

        )
