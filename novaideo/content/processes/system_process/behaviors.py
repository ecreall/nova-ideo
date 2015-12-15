# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound

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
    IPerson)
from novaideo.views.filter import find_entities
from novaideo import _
from novaideo.utilities.util import to_localized_time


INACTIVITY_DURATION = 90

INACTIVITY_ALERT = 45

INACTIVITY_LASTALERT = 1


def system_roles_validation(process, context):
    return has_role(role=('System', ))


class DeactivateUsers(ElementaryAction):
    context = INovaIdeoApplication
    actionType = ActionType.system
    roles_validation = system_roles_validation

    def send_alert(self, users, mail_template, context, request, localizer):
        subject = mail_template['subject'].format()
        for member in [m for m in users if getattr(m, 'email', '')]:
            last_connection = to_localized_time(
                getattr(member, 'last_connection'), request,
                format_id='defined_literal', ignore_month=True,
                ignore_year=True, translate=True)
            message = mail_template['template'].format(
                recipient_title=localizer.translate(
                    _(getattr(member, 'user_title', ''))),
                recipient_first_name=getattr(member, 'first_name', member.name),
                recipient_last_name=getattr(member, 'last_name', ''),
                novaideo_title=context.title,
                last_connection=last_connection.lower()
            )
            mailer_send(
                subject=subject,
                recipients=[member.email],
                sender=context.get_site_sender(),
                body=message)

    def start(self, context, request, appstruct, **kw):
        all_deactivated = []
        mail_template = context.get_mail_template('inactivity_users')
        localizer = request.localizer
        inactivity_duration = datetime.timedelta(days=INACTIVITY_DURATION)
        inactivity_alert = datetime.timedelta(days=INACTIVITY_ALERT)
        inactivity_lastalert = datetime.timedelta(days=INACTIVITY_LASTALERT)
        novaideo_catalog = find_catalog('novaideo')
        last_connection_index = novaideo_catalog['last_connection']
        current_date = datetime.datetime.combine(
            datetime.datetime.now(),
            datetime.time(0, 0, 0, tzinfo=pytz.UTC))
        inactivity_date = current_date - inactivity_duration
        query = last_connection_index.lt(inactivity_date)
        users = find_entities(
            interfaces=[IPerson],
            metadata_filter={
                'states': ['active']},
            add_query=query)
        for user in users:
            user.state = PersistentList(['deactivated'])
            user.modified_at = datetime.datetime.now(tz=pytz.UTC)
            user.reindex()
            all_deactivated.append(user)

        # First alert
        alert_date = current_date - inactivity_alert
        query = last_connection_index.lt(alert_date)
        users = find_entities(
            interfaces=[IPerson],
            metadata_filter={
                'states': ['active']},
            add_query=query)

        self.send_alert(users, mail_template, context, request, localizer)
        # Last alert
        alert_date = current_date - inactivity_lastalert
        query = last_connection_index.lt(alert_date)
        users = find_entities(
            interfaces=[IPerson],
            metadata_filter={
                'states': ['active']},
            add_query=query)
        self.send_alert(users, mail_template, context, request, localizer)
        request.registry.notify(ActivityExecuted(
            self, all_deactivated, get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#TODO behaviors
