# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound
from pyramid import renderers

from dace.util import find_catalog
from dace.objectofcollaboration.principal.util import (
    has_role, get_current)
from dace.processinstance.activity import (
    ElementaryAction,
    ActionType)
from dace.processinstance.core import ActivityExecuted

from novaideo.content.processes.\
    newsletter_management.behaviors import send_newsletter_content
from novaideo.content.interface import (
    INovaIdeoApplication,
    IPerson,
    IChallenge)
    # IProposal,
    # Iidea)
from novaideo.views.filter import find_entities
from novaideo import log
# from novaideo.utilities.util import to_localized_time
# from novaideo.utilities.alerts_utility import alert


INACTIVITY_DURATION = 90


def find_users(last_connection_index, current_date, alert):
    alert_date_min = current_date - datetime.timedelta(days=alert[0])
    query = last_connection_index.le(alert_date_min)
    if alert[1]:
        alert_date_max = current_date - datetime.timedelta(days=alert[1]-1)
        query = query & last_connection_index.ge(alert_date_max)

    users = find_entities(
        interfaces=[IPerson],
        metadata_filter={
            'states': ['active']},
        add_query=query)
    return users


def system_roles_validation(process, context):
    return has_role(role=('System', ))


class DeactivateUsers(ElementaryAction):
    context = INovaIdeoApplication
    actionType = ActionType.system
    roles_validation = system_roles_validation

    def start(self, context, request, appstruct, **kw):
        # all_deactivated = []
        # novaideo_catalog = find_catalog('novaideo')
        # last_connection_index = novaideo_catalog['last_connection']
        # current_date = datetime.datetime.combine(
        #     datetime.datetime.now(),
        #     datetime.time(0, 0, 0, tzinfo=pytz.UTC))
        # users = find_users(
        #     last_connection_index, current_date, (INACTIVITY_DURATION, None))
        # for user in users:
        #     user.state = PersistentList(['deactivated'])
        #     user.modified_at = datetime.datetime.now(tz=pytz.UTC)
        #     user.reindex()
        #     all_deactivated.append(user)

        # request.registry.notify(ActivityExecuted(
        #     self, all_deactivated, get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class ManageContents(ElementaryAction):
    context = INovaIdeoApplication
    actionType = ActionType.system
    roles_validation = system_roles_validation

    def start(self, context, request, appstruct, **kw):
        challenges = find_entities(
            interfaces=[IChallenge],
            metadata_filter={
                'states': ['pending']})
        for challenge in challenges:
            if challenge.is_expired:
                challenge.state = PersistentList(['closed', 'published'])
                challenge.reindex()

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class SendNewsLetter(ElementaryAction):
    context = INovaIdeoApplication
    actionType = ActionType.system
    roles_validation = system_roles_validation

    def start(self, context, request, appstruct, **kw):
        now = datetime.datetime.combine(
            datetime.datetime.utcnow(),
            datetime.time(23, 59, 59, tzinfo=pytz.UTC))
        automatic_newsletters = [n for n in context.newsletters
                                 if getattr(n, 'recurrence', False) and
                                 now >= n.get_sending_date() and
                                 n.validate_content()]
        for newsletter in automatic_newsletters:
            send_newsletter_content(newsletter, request)
            log.info('Send: '+newsletter.title)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors
