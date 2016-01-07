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

from novaideo.ips.mailer import mailer_send
from novaideo.content.interface import (
    INovaIdeoApplication,
    IPerson,
    IProposal,
    Iidea)
from novaideo.views.filter import find_entities
from novaideo import _
from novaideo.utilities.util import to_localized_time


INACTIVITY_DURATION = 90

INACTIVITY_ALERTS = [45, 60, 88]


def send_alert(users, mail_template, context, request, alert):
    entities = find_entities(
        interfaces=[IProposal, Iidea],
        metadata_filter={
            'content_types': ['idea', 'proposal'],
            'states': ['published']})

    result = []
    for obj in entities:
        result.append(obj)
        if len(result) == 5:
            break

    body = renderers.render(
        mail_template['template'], {'entities': result}, request)
    subject = mail_template['subject'].format()
    for member in [m for m in users if getattr(m, 'email', '')]:
        mailer_send(
            subject=subject,
            recipients=[member.email],
            sender=context.get_site_sender(),
            html=body)


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


class Alert1Users(ElementaryAction):
    context = INovaIdeoApplication
    actionType = ActionType.system
    roles_validation = system_roles_validation
    alerts_int = (INACTIVITY_ALERTS[0], INACTIVITY_ALERTS[1])
    mail_template = 'novaideo:views/templates/alert_deactiveted.pt'

    def start(self, context, request, appstruct, **kw):
        localizer = request.localizer
        mail_template = {
            'subject': localizer.translate(_('Contenus inactivity')),
            'template': self.mail_template
        }
        novaideo_catalog = find_catalog('novaideo')
        last_connection_index = novaideo_catalog['last_connection']
        current_date = datetime.datetime.combine(
            datetime.datetime.now(),
            datetime.time(0, 0, 0, tzinfo=pytz.UTC))
        users = find_users(
            last_connection_index, current_date, self.alerts_int)
        send_alert(users, mail_template, context, request, self.alerts_int)
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class Alert2Users(Alert1Users):
    alerts_int = (INACTIVITY_ALERTS[1], INACTIVITY_ALERTS[2])


class Alert3Users(Alert1Users):
    alerts_int = (INACTIVITY_ALERTS[2], INACTIVITY_DURATION)


#TODO behaviors
