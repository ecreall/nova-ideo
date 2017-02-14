# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
"""
This module represent the Challenge management process definition
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
    CreateChallenge,
    CrateAndPublish,
    SubmitChallenge,
    DelChallenge,
    EditChallenge,
    PublishChallenge,
    CommentChallenge,
    CommentChallengeAnonymous,
    PresentChallenge,
    PresentChallengeAnonymous,
    Associate,
    SeeChallenge,
    SeeChallenges,
    ArchiveChallenge,
    AddMembers,
    RemoveMembers,
    SeeMembers)
from novaideo import _


@process_definition(name='challengemanagement', id='challengemanagement')
class Challengemanagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(Challengemanagement, self).__init__(**kwargs)
        self.title = _('Challenges management')
        self.description = _('Challenges management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                #egs = ExclusiveGatewayDefinition(),
                creat = ActivityDefinition(contexts=[CreateChallenge],
                                       description=_("Create a challenge"),
                                       title=_("Create a challenge"),
                                       groups=[_('Add')]),
                creatandpublish = ActivityDefinition(contexts=[CrateAndPublish],
                                       description=_("Create a challenge"),
                                       title=_("Create a challenge"),
                                       groups=[]),
                submit = ActivityDefinition(contexts=[SubmitChallenge],
                                       description=_("Submit the challenge"),
                                       title=_("Submit for publication"),
                                       groups=[]),
                delchallenge = ActivityDefinition(contexts=[DelChallenge],
                                       description=_("Delete the challenge"),
                                       title=_("Delete"),
                                       groups=[]),
                edit = ActivityDefinition(contexts=[EditChallenge],
                                       description=_("Edit the challenge"),
                                       title=_("Edit"),
                                       groups=[]),
                archive = ActivityDefinition(contexts=[ArchiveChallenge],
                                       description=_("Archive the challenge"),
                                       title=_("Archive"),
                                       groups=[]),
                publish = ActivityDefinition(contexts=[PublishChallenge],
                                       description=_("Publish the challenge"),
                                       title=_("Publish"),
                                       groups=[]),
                present = ActivityDefinition(contexts=[PresentChallenge, PresentChallengeAnonymous],
                                       description=_("Share the challenge with others"),
                                       title=_("Share"),
                                       groups=[]),
                comment = ActivityDefinition(contexts=[CommentChallenge, CommentChallengeAnonymous],
                                       description=_("Comment the challenge"),
                                       title=_("Comment"),
                                       groups=[]),
                associate = ActivityDefinition(contexts=[Associate],
                                       description=_("Associate the challenge"),
                                       title=_("Associate"),
                                       groups=[]),
                see = ActivityDefinition(contexts=[SeeChallenge],
                                       description=_("Details"),
                                       title=_("Details"),
                                       groups=[]),
                seechallenges = ActivityDefinition(contexts=[SeeChallenges],
                                       description=_("The challenges"),
                                       title=_("The challenges"),
                                       groups=[_('See')]),
                add_members = ActivityDefinition(contexts=[AddMembers],
                                       description=_("Add Participants"),
                                       title=_("Add Participants"),
                                       groups=[]),
                remove_members = ActivityDefinition(contexts=[RemoveMembers],
                                       description=_("Remove Participants"),
                                       title=_("Remove Participants"),
                                       groups=[]),
                see_members = ActivityDefinition(contexts=[SeeMembers],
                                       description=_("See Participants"),
                                       title=_("See Participants"),
                                       groups=[]),
                pg = ParallelGatewayDefinition(),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'creat'),
                TransitionDefinition('pg', 'creatandpublish'),
                TransitionDefinition('pg', 'submit'),
                TransitionDefinition('pg', 'edit'),
                TransitionDefinition('pg', 'publish'),
                TransitionDefinition('pg', 'delchallenge'),
                TransitionDefinition('pg', 'comment'),
                TransitionDefinition('pg', 'present'),
                TransitionDefinition('pg', 'associate'),
                TransitionDefinition('pg', 'see'),
                TransitionDefinition('pg', 'seechallenges'),
                TransitionDefinition('pg', 'archive'),
                TransitionDefinition('pg', 'add_members'),
                TransitionDefinition('pg', 'remove_members'),
                TransitionDefinition('pg', 'see_members'),
                TransitionDefinition('creat', 'eg'),
                TransitionDefinition('creatandpublish', 'eg'),
                TransitionDefinition('submit', 'eg'),
                TransitionDefinition('publish', 'eg'),
                TransitionDefinition('delchallenge', 'eg'),
                TransitionDefinition('edit', 'eg'),
                TransitionDefinition('comment', 'eg'),
                TransitionDefinition('present', 'eg'),
                TransitionDefinition('associate', 'eg'),
                TransitionDefinition('see', 'eg'),
                TransitionDefinition('seechallenges', 'eg'),
                TransitionDefinition('archive', 'eg'),
                TransitionDefinition('add_members', 'eg'),
                TransitionDefinition('remove_members', 'eg'),
                TransitionDefinition('see_members', 'eg'),
                TransitionDefinition('eg', 'end'),
        )
