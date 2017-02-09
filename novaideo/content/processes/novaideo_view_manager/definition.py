# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

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
    Search,
    SeeMyContents,
    SeeMySelections,
    SeeMyParticipations,
    SeeMySupports,
    SeeOrderedProposal,
    SeeProposalsToModerate,
    SeeIdeasToModerate,
    SeeIdeasToExamine,
    SeeEntityHistory,
    Contact,
    SeeAlerts,
    SeeUsers,
    SeeAnalytics,
    SeeHome,
    SeeGraph,
    SeeReportedContents,
    SeeDependencies
    )
from novaideo import _


@process_definition(name='novaideoviewmanager', id='novaideoviewmanager')
class NovaIdeoViewManager(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(NovaIdeoViewManager, self).__init__(**kwargs)
        self.title = _('User access manager')
        self.description = _('User access manager')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                search = ActivityDefinition(contexts=[Search],
                                       description=_("Search"),
                                       title=_("Search"),
                                       groups=[]),
                home = ActivityDefinition(contexts=[SeeHome],
                                       description=_("Home"),
                                       title=_("Home"),
                                       groups=[]),
                mycontents = ActivityDefinition(contexts=[SeeMyContents],
                                       description=_("See my contents"),
                                       title=_("My contents"),
                                       groups=[]),
                myselections = ActivityDefinition(contexts=[SeeMySelections],
                                       description=_("See the items that I follow"),
                                       title=_("My followings"),
                                       groups=[]),
                myparticipations = ActivityDefinition(contexts=[SeeMyParticipations],
                                       description=_("See my participations"),
                                       title=_("My working groups"),
                                       groups=[]),
                mysupports = ActivityDefinition(contexts=[SeeMySupports],
                                       description=_("See my evaluations"),
                                       title=_("My evaluations"),
                                       groups=[]),
                seeorderedproposal = ActivityDefinition(contexts=[SeeOrderedProposal],
                                       description=_("Proposals to be examined"),
                                       title=_("Proposals to be examined"),
                                       groups=[_('See')]),
                seeproposalstomoderate = ActivityDefinition(contexts=[SeeProposalsToModerate],
                                       description=_("Proposals to be moderated"),
                                       title=_("Proposals to be moderated"),
                                       groups=[_('See')]),
                seeideastomoderate = ActivityDefinition(contexts=[SeeIdeasToModerate],
                                       description=_("Ideas to be moderated"),
                                       title=_("Ideas to be moderated"),
                                       groups=[_('See')]),
                seereportedcontents = ActivityDefinition(contexts=[SeeReportedContents],
                                       description=_("Reported contents"),
                                       title=_("Reported contents"),
                                       groups=[_('See')]),
                seeideastoexamine = ActivityDefinition(contexts=[SeeIdeasToExamine],
                                       description=_("Ideas to be examined"),
                                       title=_("Ideas to be examined"),
                                       groups=[_('See')]),
                seeusers = ActivityDefinition(contexts=[SeeUsers],
                                       description=_("Members"),
                                       title=_("Members"),
                                       groups=[_('See')]),
                seehistory = ActivityDefinition(contexts=[SeeEntityHistory],
                                       description=_("See the history of processes"),
                                       title=_("History of processes"),
                                       groups=[]),
                seealerts = ActivityDefinition(contexts=[SeeAlerts],
                                       description=_("See the alerts"),
                                       title=_("Alerts"),
                                       groups=[]),
                seegraph = ActivityDefinition(contexts=[SeeGraph],
                                       description=_("See the graph of dependencies"),
                                       title=_("View the graph of dependencies"),
                                       groups=[]),
                seedependencies = ActivityDefinition(contexts=[SeeDependencies],
                                       description=_("See the associations"),
                                       title=_("View associations"),
                                       groups=[]),
                seeanalytics = ActivityDefinition(contexts=[SeeAnalytics],
                                       description=_("See analytics"),
                                       title=_("Analytics"),
                                       groups=[_('See')]),
                contact = ActivityDefinition(contexts=[Contact],
                                       description=_("Contact"),
                                       title=_("Contact"),
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'search'),
                TransitionDefinition('search', 'eg'),
                TransitionDefinition('pg', 'seegraph'),
                TransitionDefinition('seegraph', 'eg'),
                TransitionDefinition('pg', 'seedependencies'),
                TransitionDefinition('seedependencies', 'eg'),
                TransitionDefinition('pg', 'home'),
                TransitionDefinition('home', 'eg'),
                TransitionDefinition('pg', 'mycontents'),
                TransitionDefinition('mycontents', 'eg'),
                TransitionDefinition('pg', 'myselections'),
                TransitionDefinition('myselections', 'eg'),
                TransitionDefinition('pg', 'myparticipations'),
                TransitionDefinition('myparticipations', 'eg'),
                TransitionDefinition('pg', 'mysupports'),
                TransitionDefinition('mysupports', 'eg'),
                TransitionDefinition('pg', 'seeorderedproposal'),
                TransitionDefinition('seeorderedproposal', 'eg'),
                TransitionDefinition('pg', 'seeideastoexamine'),
                TransitionDefinition('seeideastoexamine', 'eg'),
                TransitionDefinition('pg', 'seeusers'),
                TransitionDefinition('seeusers', 'eg'),
                TransitionDefinition('pg', 'seeideastomoderate'),
                TransitionDefinition('seeideastomoderate', 'eg'),
                TransitionDefinition('pg', 'seeproposalstomoderate'),
                TransitionDefinition('seeproposalstomoderate', 'eg'),
                TransitionDefinition('pg', 'seereportedcontents'),
                TransitionDefinition('seereportedcontents', 'eg'),
                TransitionDefinition('pg', 'seehistory'),
                TransitionDefinition('seehistory', 'eg'),
                TransitionDefinition('pg', 'contact'),
                TransitionDefinition('contact', 'eg'),
                TransitionDefinition('pg', 'seealerts'),
                TransitionDefinition('seealerts', 'eg'),
                TransitionDefinition('pg', 'seeanalytics'),
                TransitionDefinition('seeanalytics', 'eg'),
                TransitionDefinition('eg', 'end'),
        )
