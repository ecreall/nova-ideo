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
    CreateNewsletter,
    SeeNewsletter,
    EditNewsletter,
    SendNewsletter,
    RemoveNewsletter,
    SubscribeNewsletter,
    UnsubscribeNewsletter,
    UserUnsubscribeNewsletter,
    SeeNewsletters,
    RedactNewsletter,
    SeeSubscribed,
    ConfigureNewsletter,
    SeeNewsletterHistory
    )
from novaideo import _


@process_definition(name='newslettermanagement',
                    id='newslettermanagement')
class NewsletterManagement(ProcessDefinition, VisualisableElement):
    isUnique = True

    def __init__(self, **kwargs):
        super(NewsletterManagement, self).__init__(**kwargs)
        self.title = _('Newsletter management')
        self.description = _('Newsletter management')

    def _init_definition(self):
        self.defineNodes(
                start = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                creat = ActivityDefinition(contexts=[CreateNewsletter],
                                       description=_("Create a newsletter"),
                                       title=_("Create a newsletter"),
                                       groups=[_('Add')]),
                edit = ActivityDefinition(contexts=[EditNewsletter],
                                       description=_("Edit the newsletter"),
                                       title=_("Edit"),
                                       groups=[]),
                configure = ActivityDefinition(contexts=[ConfigureNewsletter],
                                       description=_("Configure the newsletter"),
                                       title=_("Configure"),
                                       groups=[]),
                redact = ActivityDefinition(contexts=[RedactNewsletter],
                                       description=_("Write the newsletter"),
                                       title=_("Write"),
                                       groups=[]),
                send = ActivityDefinition(contexts=[SendNewsletter],
                                       description=_("Send the newsletter"),
                                       title=_("Send"),
                                       groups=[]),
                remove = ActivityDefinition(contexts=[RemoveNewsletter],
                                       description=_("Remove the newsletter"),
                                       title=_("Remove"),
                                       groups=[]),
                subscribe = ActivityDefinition(contexts=[SubscribeNewsletter],
                                       description=_("Subscribe"),
                                       title=_("Newsletters"),
                                       groups=[]),
                unsubscribe = ActivityDefinition(contexts=[UserUnsubscribeNewsletter],
                                       description=_("Unsubscribe"),
                                       title=_("Unsubscribe"),
                                       groups=[]),
                unsubscribes = ActivityDefinition(contexts=[UnsubscribeNewsletter],
                                       description=_("Unsubscribe"),
                                       title=_("Unsubscribe"),
                                       groups=[]),
                see = ActivityDefinition(contexts=[SeeNewsletter],
                                       description=_("See the newsletter"),
                                       title=_("See"),
                                       groups=[]),
                seesubscribed = ActivityDefinition(contexts=[SeeSubscribed],
                                       description=_("See subscribed users"),
                                       title=_("Subscribed users"),
                                       groups=[]),
                see_all = ActivityDefinition(contexts=[SeeNewsletters],
                                       description=_("See newsletters"),
                                       title=_("Newsletters"),
                                       groups=[_('See')]),
                see_content_history = ActivityDefinition(contexts=[SeeNewsletterHistory],
                                       description=_("See content history"),
                                       title=_("Content history"),
                                       groups=[]),
                eg = ExclusiveGatewayDefinition(),
                end = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('start', 'pg'),
                TransitionDefinition('pg', 'creat'),
                TransitionDefinition('creat', 'eg'),
                TransitionDefinition('pg', 'edit'),
                TransitionDefinition('edit', 'eg'),
                TransitionDefinition('pg', 'configure'),
                TransitionDefinition('configure', 'eg'),
                TransitionDefinition('pg', 'redact'),
                TransitionDefinition('redact', 'eg'),
                TransitionDefinition('pg', 'send'),
                TransitionDefinition('send', 'eg'),
                TransitionDefinition('pg', 'remove'),
                TransitionDefinition('remove', 'eg'),
                TransitionDefinition('pg', 'subscribe'),
                TransitionDefinition('subscribe', 'eg'),
                TransitionDefinition('pg', 'unsubscribe'),
                TransitionDefinition('unsubscribe', 'eg'),
                TransitionDefinition('pg', 'unsubscribes'),
                TransitionDefinition('unsubscribes', 'eg'),
                TransitionDefinition('pg', 'see'),
                TransitionDefinition('see', 'eg'),
                TransitionDefinition('pg', 'see_all'),
                TransitionDefinition('see_all', 'eg'),
                TransitionDefinition('pg', 'seesubscribed'),
                TransitionDefinition('seesubscribed', 'eg'),
                TransitionDefinition('pg', 'see_content_history'),
                TransitionDefinition('see_content_history', 'eg'),
                TransitionDefinition('eg', 'end'),
        )
