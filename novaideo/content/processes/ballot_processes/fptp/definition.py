# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
"""
This module represent the FPTP election process definition
powered by the dace engine. This process is vlolatile, which means
that this process is automatically removed after the end. And is controlled,
which means that this process is not automatically instanciated.
"""

from dace.processdefinition.processdef import ProcessDefinition
from dace.processdefinition.activitydef import ActivityDefinition
from dace.processdefinition.transitiondef import TransitionDefinition
from dace.processdefinition.eventdef import (
    StartEventDefinition,
    EndEventDefinition)
from dace.objectofcollaboration.services.processdef_container import(
    process_definition)
from pontus.core import VisualisableElement

from .behaviors import Vote
from novaideo import _


@process_definition(name='fptpprocess', id='fptpprocess')
class FPTPProcess(ProcessDefinition, VisualisableElement):
    isVolatile = True
    isControlled = True
    discriminator = 'Vote process'

    def __init__(self, **kwargs):
        super(FPTPProcess, self).__init__(**kwargs)
        self.title = _('First Past The Post Process')
        self.description = _('First Past The Post Process')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                vote = ActivityDefinition(contexts=[Vote],
                                       description=_("Vote"),
                                       title=_("Vote"),
                                       groups=[]),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'vote'),
                TransitionDefinition('vote', 'end'),
        )
