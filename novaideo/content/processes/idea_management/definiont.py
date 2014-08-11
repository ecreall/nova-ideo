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
    CreateIdea,
    DuplicateIdea,
    DelIdea,
    EditIdea,
    PublishIdea,
    RecuperateIdea,
    AbandonIdea,
    CommentIdea,
    PresentIdea,
    Associate,
    SeeIdea)
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
                                       description="Creat a new idea",
                                       title="Creat idea",
                                       groups=[_('Add')]),
                duplicate = ActivityDefinition(contexts=[DuplicateIdea],
                                       description=_("Duplicate this idea"),
                                       title=_("Duplicate"),
                                       groups=[]),
                delidea = ActivityDefinition(contexts=[DelIdea],
                                       description=_("Delet the idea"),
                                       title=_("Delet"),
                                       groups=[]),
                edit = ActivityDefinition(contexts=[EditIdea],
                                       description=_("Edit the idea"),
                                       title=_("Edit"),
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
                                       description=_("Abandon the idea"),
                                       title=_("Abandon"),
                                       groups=[]),
                present = ActivityDefinition(contexts=[PresentIdea],
                                       description=_("Present the idea"),
                                       title=_("Present"),
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
                pg = ParallelGatewayDefinition(),
                #pg2 = ParallelGatewayDefinition(),
                #eg1 = ExclusiveGatewayDefinition(),
                #eg2 = ExclusiveGatewayDefinition(),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'creat'),
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
                TransitionDefinition('creat', 'eg'),
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
                TransitionDefinition('eg', 'end'),
        )

        #self.defineTransitions(
        #        TransitionDefinition('start', 'egs'),
        #        TransitionDefinition('egs', 'creat'),
        #        TransitionDefinition('egs', 'duplicate'),
        #        TransitionDefinition('creat', 'eg1'),
        #        TransitionDefinition('duplicate', 'eg1'),
        #        TransitionDefinition('eg1', 'pg'),
        #        TransitionDefinition('pg', 'edit'),
        #        TransitionDefinition('pg', 'publish'),
        #        TransitionDefinition('pg', 'eg2'),
        #        TransitionDefinition('pg', 'delidea'),
        #        TransitionDefinition('eg2', 'abandon'),
        #        TransitionDefinition('abandon', 'recuperate'),
        #        TransitionDefinition('recuperate', 'eg2'),
        #        TransitionDefinition('publish', 'pg2'),
        #        TransitionDefinition('pg2', 'comment'),
        #        TransitionDefinition('pg2', 'present'),
        #        TransitionDefinition('delidea', 'eg3'),
        #        TransitionDefinition('edit', 'eg3'),
        #        TransitionDefinition('comment', 'eg3'),
        #        TransitionDefinition('present', 'eg3'),
        #        TransitionDefinition('eg3', 'end'),
       # )
