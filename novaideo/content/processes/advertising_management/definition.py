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
    CreateWebAdvertising,
    SeeWebAdvertising,
    EditWebAdvertising,
    PublishAdvertising,
    ArchiveAdvertising,
    RemoveAdvertising,
    SeeAdvertisings
    )
from novaideo import _


@process_definition(name='advertisingmanagement',
                    id='advertisingmanagement')
class AdvertisingManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(AdvertisingManagement, self).__init__(**kwargs)
        self.title = _('Announcements management')
        self.description = _('Announcements management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                creat = ActivityDefinition(contexts=[CreateWebAdvertising],
                                       description=_("Create an announcement"),
                                       title=_("Create an announcement"),
                                       groups=[_('Add')]),
                edit = ActivityDefinition(contexts=[EditWebAdvertising],
                                       description=_("Edit the announcement"),
                                       title=_("Edit the announcement"),
                                       groups=[]),
                see = ActivityDefinition(contexts=[SeeWebAdvertising],
                                       description=_("Details"),
                                       title=_("Details"),
                                       groups=[]),
                see_all = ActivityDefinition(contexts=[SeeAdvertisings],
                                       description=_("See announcements"),
                                       title=_("Announcements"),
                                       groups=[_('See')]),
                publish = ActivityDefinition(contexts=[PublishAdvertising],
                                       description=_("Publish the announcement"),
                                       title=_("Publish"),
                                       groups=[]),
                archive = ActivityDefinition(contexts=[ArchiveAdvertising],
                                       description=_("Archive the announcement"),
                                       title=_("Archive"),
                                       groups=[]),
                remove = ActivityDefinition(contexts=[RemoveAdvertising],
                                       description=_("Remove the announcement"),
                                       title=_("Remove"),
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'creat'),
                TransitionDefinition('creat', 'eg'),
                TransitionDefinition('pg', 'see'),
                TransitionDefinition('see', 'eg'),
                TransitionDefinition('pg', 'see_all'),
                TransitionDefinition('see_all', 'eg'),
                TransitionDefinition('pg', 'edit'),
                TransitionDefinition('edit', 'eg'),
                TransitionDefinition('pg', 'publish'),
                TransitionDefinition('publish', 'eg'),
                TransitionDefinition('pg', 'archive'),
                TransitionDefinition('archive', 'eg'),
                TransitionDefinition('pg', 'remove'),
                TransitionDefinition('remove', 'eg'),
                TransitionDefinition('eg', 'end'),

        )
