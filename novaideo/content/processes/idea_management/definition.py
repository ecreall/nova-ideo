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
    CrateAndPublish,
    CrateAndPublishAsProposal,
    SeeRelatedWorkingGroups,
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
    CompareIdea,
    PublishIdeaModeration,
    SubmitIdea,
    ArchiveIdea,
    OpposeIdea,
    SupportIdea,
    WithdrawToken,
    MakeOpinion)
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
                creatandpublish = ActivityDefinition(contexts=[CrateAndPublish],
                                       description=_("Create an idea"),
                                       title=_("Create an idea"),
                                       groups=[]),
                creatandpublishasproposal = ActivityDefinition(contexts=[CrateAndPublishAsProposal],
                                       description=_("Create a working group"),
                                       title=_("Create a working group"),
                                       groups=[]),
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
                submit = ActivityDefinition(contexts=[SubmitIdea],
                                       description=_("Submit the idea"),
                                       title=_("Submit for publishing"),
                                       groups=[]),
                publish_moderation = ActivityDefinition(contexts=[PublishIdeaModeration],
                                       description=_("Publish the idea"),
                                       title=_("Publish"),
                                       groups=[]),
                archive = ActivityDefinition(contexts=[ArchiveIdea],
                                       description=_("Archive the idea"),
                                       title=_("Archive"),
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
                                       description=_("Share the idea to others"),
                                       title=_("Share"),
                                       groups=[]),
                comment = ActivityDefinition(contexts=[CommentIdea],
                                       description=_("Comment the idea"),
                                       title=_("Comment"),
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
                support = ActivityDefinition(contexts=[SupportIdea],
                                       description=_("Support the idea"),
                                       title=_("Support"),
                                       groups=[]),
                oppose = ActivityDefinition(contexts=[OpposeIdea],
                                       description=_("To oppose an idea"),
                                       title=_("Oppose"),
                                       groups=[]),
                withdraw_token = ActivityDefinition(contexts=[WithdrawToken],
                                       description=_("Withdraw token from idea"),
                                       title=_("Withdraw my token"),
                                       groups=[]),
                makeitsopinion = ActivityDefinition(contexts=[MakeOpinion],
                                       description=_("Make its opinion"),
                                       title=_("Make its opinion"),
                                       groups=[]),
                seeworkinggroups = ActivityDefinition(contexts=[SeeRelatedWorkingGroups],
                                       description=_("See related working groups"),
                                       title=_("Working groups"),
                                       groups=[]),
                pg = ParallelGatewayDefinition(),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'creat'),
                TransitionDefinition('pg', 'creatandpublish'),
                TransitionDefinition('pg', 'seeworkinggroups'),
                TransitionDefinition('pg', 'creatandpublishasproposal'),
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
                TransitionDefinition('pg', 'publish_moderation'),
                TransitionDefinition('pg', 'submit'),
                TransitionDefinition('pg', 'archive'),
                TransitionDefinition('pg', 'makeitsopinion'),
                TransitionDefinition('makeitsopinion', 'eg'),
                TransitionDefinition('pg', 'support'),
                TransitionDefinition('support', 'eg'),
                TransitionDefinition('pg', 'oppose'),
                TransitionDefinition('oppose', 'eg'),
                TransitionDefinition('pg', 'withdraw_token'),
                TransitionDefinition('withdraw_token', 'eg'),
                TransitionDefinition('creat', 'eg'),
                TransitionDefinition('creatandpublish', 'eg'),
                TransitionDefinition('creatandpublishasproposal', 'eg'),
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
                TransitionDefinition('submit', 'eg'),
                TransitionDefinition('publish_moderation', 'eg'),
                TransitionDefinition('archive', 'eg'),
                TransitionDefinition('seeworkinggroups', 'eg'),
                TransitionDefinition('eg', 'end'),
        )
