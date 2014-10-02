from dace.processdefinition.processdef import ProcessDefinition
from dace.processdefinition.activitydef import ActivityDefinition
from dace.processdefinition.gatewaydef import (
    ExclusiveGatewayDefinition,
    ParallelGatewayDefinition)
from dace.processdefinition.transitiondef import TransitionDefinition
from dace.processdefinition.eventdef import (
    StartEventDefinition,
    EndEventDefinition)
from dace.objectofcollaboration.services.processdef_container import process_definition
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
#    AddReplacedIdea,
 #   AddIdeaReplacement)
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
                                       description=_("Delet the amendment"),
                                       title=_("Delet"),
                                       groups=[]),
                duplicate = ActivityDefinition(contexts=[DuplicateAmendment],
                                       description=_("Duplicate the amendment"),
                                       title=_("Duplicate"),
                                       groups=[]),
                edit = ActivityDefinition(contexts=[EditAmendment],
                                       description=_("Edit the amendment"),
                                       title=_("Edit"),
                                       groups=[]),
#                add_idea_of_replacement = ActivityDefinition(contexts=[AddIdeaReplacement],
#                                       description=_("Add idea of replacement"),
##                                       title=_("Add idea of replacement"),
#                                       groups=[]),
#                add_repalced_idea = ActivityDefinition(contexts=[AddReplacedIdea],
#                                       description=_("Add replaced idea"),
#                                       title=_("Add replaced idea"),
#                                       groups=[]),
                explanation = ActivityDefinition(contexts=[ExplanationAmendment],
                                       description=_("Explanation"),
                                       title=_("Explanation"),
                                       groups=[]),
                explanationitem = ActivityDefinition(contexts=[ExplanationItem],
                                       description=_("Explanation item"),
                                       title=_("Explanation item"),
                                       groups=[]),

                submit = ActivityDefinition(contexts=[SubmitAmendment],
                                       description=_("Submit the amendment"),
                                       title=_("Submit"),
                                       groups=[]),
                present = ActivityDefinition(contexts=[PresentAmendment],
                                       description=_("Present the amendment"),
                                       title=_("Present"),
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
#                TransitionDefinition('pg', 'add_idea_of_replacement'),
#                TransitionDefinition('pg', 'add_repalced_idea'),
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
