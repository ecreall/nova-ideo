# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
"""
This module represent the Amendments management process definition 
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
    DelAmendment,
    EditAmendment,
    SubmitAmendment,
    CommentAmendment,
    PresentAmendment,
    Associate,
    SeeAmendment,
    DuplicateAmendment,
    ExplanationAmendment,
    ExplanationItem)
from novaideo import _


@process_definition(name='amendmentmanagement', id='amendmentmanagement')
class AmendmentManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(AmendmentManagement, self).__init__(**kwargs)
        self.title = _('Amendments management')
        self.description = _('Amendments management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                #egs = ExclusiveGatewayDefinition(),
                delamendment = ActivityDefinition(contexts=[DelAmendment],
                                       description=_("Delete the amendment"),
                                       title=_("Delete"),
                                       groups=[]),
                duplicate = ActivityDefinition(contexts=[DuplicateAmendment],
                                       description=_("Duplicate the amendment"),
                                       title=_("Duplicate"),
                                       groups=[]),
                edit = ActivityDefinition(contexts=[EditAmendment],
                                       description=_("Edit the amendment"),
                                       title=_("Edit"),
                                       groups=[]),
                explanation = ActivityDefinition(contexts=[ExplanationAmendment],
                                       description=_("Explain my improvement"),
                                       title=_("Explain my improvement"),
                                       groups=[]),
                explanationitem = ActivityDefinition(contexts=[ExplanationItem],
                                       description=_("Justification item"),
                                       title=_("Justification item"),
                                       groups=[]),
                submit = ActivityDefinition(contexts=[SubmitAmendment],
                                       description=_("Submit the amendment"),
                                       title=_("Submit"),
                                       groups=[]),
                present = ActivityDefinition(contexts=[PresentAmendment],
                                       description=_("Share the amendment to others"),
                                       title=_("Share"),
                                       groups=[]),
                comment = ActivityDefinition(contexts=[CommentAmendment],
                                       description=_("Comment the amendment"),
                                       title=_("Comment"),
                                       groups=[]),
                associate = ActivityDefinition(contexts=[Associate],
                                       description=_("Associate the amendment"),
                                       title=_("Associate"),
                                       groups=[]),
                see = ActivityDefinition(contexts=[SeeAmendment],
                                       description=_("Details"),
                                       title=_("Details"),
                                       groups=[]),
                pg = ParallelGatewayDefinition(),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'edit'),
                TransitionDefinition('pg', 'submit'),
                TransitionDefinition('pg', 'explanation'),
                TransitionDefinition('pg', 'explanationitem'),
                TransitionDefinition('pg', 'delamendment'),
                TransitionDefinition('pg', 'duplicate'),
                TransitionDefinition('pg', 'comment'),
                TransitionDefinition('pg', 'present'),
                TransitionDefinition('pg', 'associate'),
                TransitionDefinition('pg', 'see'),
                TransitionDefinition('duplicate', 'eg'),
                TransitionDefinition('submit', 'eg'),
                TransitionDefinition('delamendment', 'eg'),
                TransitionDefinition('edit', 'eg'),
                TransitionDefinition('comment', 'eg'),
                TransitionDefinition('present', 'eg'),
                TransitionDefinition('associate', 'eg'),
                TransitionDefinition('see', 'eg'),
                TransitionDefinition('eg', 'end'),
        )
