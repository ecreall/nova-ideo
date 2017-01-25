# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
"""
This module represent the Question management process definition
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
    AskQuestion,
    DelQuestion,
    EditQuestion,
    CommentQuestion,
    CommentQuestionAnonymous,
    AnswerQuestion,
    AnswerQuestionAnonymous,
    PresentQuestion,
    PresentQuestionAnonymous,
    Associate,
    SeeQuestion,
    ArchiveQuestion,
    OpposeQuestion,
    OpposeQuestionAnonymous,
    SupportQuestion,
    SupportQuestionAnonymous,
    WithdrawToken,
    Close,
    # Answer
    DelAnswer,
    EditAnswer,
    CommentAnswer,
    PresentAnswer,
    CommentAnswerAnonymous,
    PresentAnswerAnonymous,
    AssociateAnswer,
    ArchiveAnswer,
    OpposeAnswer,
    OpposeAnswerAnonymous,
    SupportAnswer,
    SupportAnswerAnonymous,
    WithdrawTokenAnswer,
    SeeAnswer,
    ValidateAnswer,
    TransformToIdea)
from novaideo import _


@process_definition(name='questionmanagement', id='questionmanagement')
class QuestionManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(QuestionManagement, self).__init__(**kwargs)
        self.title = _('Questions management')
        self.description = _('Questions management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                #egs = ExclusiveGatewayDefinition(),
                creat = ActivityDefinition(contexts=[AskQuestion],
                                       description=_("Ask a question"),
                                       title=_("Ask a question"),
                                       groups=[_('Add')]),
                delquestion = ActivityDefinition(contexts=[DelQuestion],
                                       description=_("Delete the question"),
                                       title=_("Delete"),
                                       groups=[]),
                edit = ActivityDefinition(contexts=[EditQuestion],
                                       description=_("Edit the question"),
                                       title=_("Edit"),
                                       groups=[]),
                archive = ActivityDefinition(contexts=[ArchiveQuestion],
                                       description=_("Archive the question"),
                                       title=_("Archive"),
                                       groups=[]),
                present = ActivityDefinition(contexts=[PresentQuestion, PresentQuestionAnonymous],
                                       description=_("Share the question with others"),
                                       title=_("Share"),
                                       groups=[]),
                comment = ActivityDefinition(contexts=[CommentQuestion, CommentQuestionAnonymous],
                                       description=_("Comment the question"),
                                       title=_("Comment"),
                                       groups=[]),
                answer = ActivityDefinition(contexts=[AnswerQuestion, AnswerQuestionAnonymous],
                                       description=_("Answer the question"),
                                       title=_("Answer"),
                                       groups=[]),
                associate = ActivityDefinition(contexts=[Associate],
                                       description=_("Associate the question"),
                                       title=_("Associate"),
                                       groups=[]),
                see = ActivityDefinition(contexts=[SeeQuestion],
                                       description=_("Details"),
                                       title=_("Details"),
                                       groups=[]),
                support = ActivityDefinition(contexts=[SupportQuestion, SupportQuestionAnonymous],
                                       description=_("This question is useful"),
                                       title=_("This question is useful"),
                                       groups=[]),
                oppose = ActivityDefinition(contexts=[OpposeQuestion, OpposeQuestionAnonymous],
                                       description=_("This question is not useful"),
                                       title=_("This question is not useful"),
                                       groups=[]),
                withdraw_token = ActivityDefinition(contexts=[WithdrawToken],
                                       description=_("Withdraw my opinion"),
                                       title=_("Withdraw my opinion"),
                                       groups=[]),
                close = ActivityDefinition(contexts=[Close],
                                       description=_("Close the question"),
                                       title=_("Close"),
                                       groups=[]),
                pg = ParallelGatewayDefinition(),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'creat'),
                TransitionDefinition('pg', 'edit'),
                TransitionDefinition('pg', 'delquestion'),
                TransitionDefinition('pg', 'comment'),
                TransitionDefinition('pg', 'answer'),
                TransitionDefinition('pg', 'present'),
                TransitionDefinition('pg', 'associate'),
                TransitionDefinition('pg', 'see'),
                TransitionDefinition('pg', 'archive'),
                TransitionDefinition('pg', 'support'),
                TransitionDefinition('pg', 'close'),
                TransitionDefinition('support', 'eg'),
                TransitionDefinition('pg', 'oppose'),
                TransitionDefinition('oppose', 'eg'),
                TransitionDefinition('pg', 'withdraw_token'),
                TransitionDefinition('withdraw_token', 'eg'),
                TransitionDefinition('creat', 'eg'),
                TransitionDefinition('delquestion', 'eg'),
                TransitionDefinition('edit', 'eg'),
                TransitionDefinition('comment', 'eg'),
                TransitionDefinition('answer', 'eg'),
                TransitionDefinition('present', 'eg'),
                TransitionDefinition('associate', 'eg'),
                TransitionDefinition('see', 'eg'),
                TransitionDefinition('archive', 'eg'),
                TransitionDefinition('close', 'eg'),
                TransitionDefinition('eg', 'end'),
        )


@process_definition(name='answermanagement', id='answermanagement')
class AnswerManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(AnswerManagement, self).__init__(**kwargs)
        self.title = _('Answers management')
        self.description = _('Answers management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                #egs = ExclusiveGatewayDefinition(),
                delanswer = ActivityDefinition(contexts=[DelAnswer],
                                       description=_("Delete the answer"),
                                       title=_("Delete"),
                                       groups=[]),
                edit = ActivityDefinition(contexts=[EditAnswer],
                                       description=_("Edit the answer"),
                                       title=_("Edit"),
                                       groups=[]),
                archive = ActivityDefinition(contexts=[ArchiveAnswer],
                                       description=_("Archive the answer"),
                                       title=_("Archive"),
                                       groups=[]),
                present = ActivityDefinition(contexts=[PresentAnswer, PresentAnswerAnonymous],
                                       description=_("Share the answer with others"),
                                       title=_("Share"),
                                       groups=[]),
                comment = ActivityDefinition(contexts=[CommentAnswer, CommentAnswerAnonymous],
                                       description=_("Comment the answer"),
                                       title=_("Comment"),
                                       groups=[]),
                associate = ActivityDefinition(contexts=[AssociateAnswer],
                                       description=_("Associate the answer"),
                                       title=_("Associate"),
                                       groups=[]),
                see = ActivityDefinition(contexts=[SeeAnswer],
                                       description=_("Details"),
                                       title=_("Details"),
                                       groups=[]),
                support = ActivityDefinition(contexts=[SupportAnswer, SupportAnswerAnonymous],
                                       description=_("This answer is useful"),
                                       title=_("This answer is useful"),
                                       groups=[]),
                oppose = ActivityDefinition(contexts=[OpposeAnswer, OpposeAnswerAnonymous],
                                       description=_("This answer is not useful"),
                                       title=_("This answer is not useful"),
                                       groups=[]),
                withdraw_token = ActivityDefinition(contexts=[WithdrawTokenAnswer],
                                       description=_("Withdraw my opinion"),
                                       title=_("Withdraw my opinion"),
                                       groups=[]),
                validate = ActivityDefinition(contexts=[ValidateAnswer],
                                       description=_("Validate th answer"),
                                       title=_("Validate"),
                                       groups=[]),
                transformtoidea = ActivityDefinition(contexts=[TransformToIdea],
                                       description=_("Transform the answer into an idea"),
                                       title=_("Transform into an idea"),
                                       groups=[]),
                pg = ParallelGatewayDefinition(),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'edit'),
                TransitionDefinition('pg', 'delanswer'),
                TransitionDefinition('pg', 'comment'),
                TransitionDefinition('pg', 'present'),
                TransitionDefinition('pg', 'associate'),
                TransitionDefinition('pg', 'see'),
                TransitionDefinition('pg', 'archive'),
                TransitionDefinition('pg', 'support'),
                TransitionDefinition('pg', 'validate'),
                TransitionDefinition('pg', 'transformtoidea'),
                TransitionDefinition('support', 'eg'),
                TransitionDefinition('pg', 'oppose'),
                TransitionDefinition('oppose', 'eg'),
                TransitionDefinition('pg', 'withdraw_token'),
                TransitionDefinition('withdraw_token', 'eg'),
                TransitionDefinition('delanswer', 'eg'),
                TransitionDefinition('edit', 'eg'),
                TransitionDefinition('comment', 'eg'),
                TransitionDefinition('present', 'eg'),
                TransitionDefinition('associate', 'eg'),
                TransitionDefinition('see', 'eg'),
                TransitionDefinition('archive', 'eg'),
                TransitionDefinition('validate', 'eg'),
                TransitionDefinition('transformtoidea', 'eg'),
                TransitionDefinition('eg', 'end'),
        )
