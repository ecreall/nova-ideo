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
    ConfigureSite,
    ManageKeywords,
    Extract)
from novaideo import _


@process_definition(name='adminprocess',
                    id='adminprocess')
class AdminProcess(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(AdminProcess, self).__init__(**kwargs)
        self.title = _('Admin process')
        self.description = _('Admin process')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                configure_site = ActivityDefinition(contexts=[ConfigureSite],
                                       description=_("Configure the site"),
                                       title=_("Configure"),
                                       groups=[_('More')]),
                managekeywords = ActivityDefinition(contexts=[ManageKeywords],
                                       description=_("Manage keywords"),
                                       title=_("Manage keywords"),
                                       groups=[_('More')]),
                extract = ActivityDefinition(contexts=[Extract],
                                       description=_("Extract"),
                                       title=_("Extract"),
                                       groups=[_('More')]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'configure_site'),
                TransitionDefinition('configure_site', 'eg'),
                TransitionDefinition('pg', 'extract'),
                TransitionDefinition('extract', 'eg'),
                TransitionDefinition('pg', 'managekeywords'),
                TransitionDefinition('managekeywords', 'eg'),
                TransitionDefinition('eg', 'end'),
        )
