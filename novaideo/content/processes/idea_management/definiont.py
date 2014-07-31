from dace.interfaces import IProcessDefinition
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
    CreatIdea,
    DuplicatIdea,
    DelIdea,
    EditIdea,
    PublishIdea,
    RecuperateIdea,
    AbandonIdea,
    CommentIdea)
from novaideo import _


@process_definition(name='ideamanagement', id='ideamanagement')
class IdeaManagement(ProcessDefinition, VisualisableElement):

    def __init__(self, **kwargs):
        super(IdeaManagement, self).__init__(**kwargs)
        self.title = _('Ideas management')
        self.description = _('Ideas management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                egs = ExclusiveGatewayDefinition(),
                creat = ActivityDefinition(contexts=[CreatIdea],
                                       description="Creat a new idea",
                                       title="Creat idea",
                                       groups=[_('Add')]),
                duplicat = ActivityDefinition(contexts=[DuplicatIdea],
                                       description=_("Duplicat this idea"),
                                       title=_("Duplicat"),
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
                comment = ActivityDefinition(contexts=[CommentIdea],
                                       description=_("Comment the idea"),
                                       title=_("Comment"),
                                       groups=[]),
                pg = ParallelGatewayDefinition(),
                eg1 = ExclusiveGatewayDefinition(),
                eg2 = ExclusiveGatewayDefinition(),
                eg3 = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'egs'),
                TransitionDefinition('egs', 'creat'),
                TransitionDefinition('egs', 'duplicat'),
                TransitionDefinition('creat', 'eg1'),
                TransitionDefinition('duplicat', 'eg1'),
                TransitionDefinition('eg1', 'pg'),
                TransitionDefinition('pg', 'edit'),
                TransitionDefinition('pg', 'publish'),
                TransitionDefinition('pg', 'eg2'),
                TransitionDefinition('pg', 'delidea'),
                TransitionDefinition('eg2', 'abandon'),
                TransitionDefinition('abandon', 'recuperate'),
                TransitionDefinition('recuperate', 'eg2'),
                TransitionDefinition('publish', 'comment'),
                TransitionDefinition('delidea', 'eg3'),
                TransitionDefinition('edit', 'eg3'),
                TransitionDefinition('comment', 'eg3'),
                TransitionDefinition('eg3', 'end'),
        )
