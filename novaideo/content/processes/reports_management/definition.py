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
    Report,
    Ignore,
    Censor,
    Restor,
    SeeReports)
from novaideo import _


@process_definition(name='reportsmanagement', id='reportsmanagement')
class ReportsManagementProcess(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(ReportsManagementProcess, self).__init__(**kwargs)
        self.title = _('Reported content management')
        self.description = _('Reported content management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                report = ActivityDefinition(contexts=[Report],
                                       description=_("Report the content"),
                                       title=_("Report"),
                                       groups=[]),
                see_reports = ActivityDefinition(contexts=[SeeReports],
                                       description=_("See reported contents"),
                                       title=_("Reported contents"),
                                       groups=[]),
                ignore = ActivityDefinition(contexts=[Ignore],
                                       description=_("Ignore reports"),
                                       title=_("Ignore reports"),
                                       groups=[]),
                censor = ActivityDefinition(contexts=[Censor],
                                       description=_("Censor the content"),
                                       title=_("Censor the content"),
                                       groups=[]),
                restor = ActivityDefinition(contexts=[Restor],
                                       description=_("Restore the content"),
                                       title=_("Restore the content"),
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'report'),
                TransitionDefinition('report', 'eg'),
                TransitionDefinition('pg', 'see_reports'),
                TransitionDefinition('see_reports', 'eg'),
                TransitionDefinition('pg', 'ignore'),
                TransitionDefinition('ignore', 'eg'),
                TransitionDefinition('pg', 'censor'),
                TransitionDefinition('censor', 'eg'),
                TransitionDefinition('pg', 'restor'),
                TransitionDefinition('restor', 'eg'),
                TransitionDefinition('eg', 'end'),

        )
