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

from novaideo.content.interface import (
    INovaIdeoApplication,
    IPerson,
    IProposal,
    Iidea)
from novaideo.views.filter import find_entities
from novaideo import _
from novaideo.utilities.util import to_localized_time
from novaideo.utilities.alerts_utility import alert


INACTIVITY_DURATION = 90


NEWSLETTER_DURATION = 15


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


class SendNewsLetter(ElementaryAction):
    context = INovaIdeoApplication
    actionType = ActionType.system
    roles_validation = system_roles_validation
    mail_template = 'novaideo:views/templates/newsletter_template.pt'

    def start(self, context, request, appstruct, **kw):
        root = request.root
        previous_date = getattr(root, 'newsletter_date', None)
        now = datetime.datetime.now(tz=pytz.UTC)
        if previous_date:
            previous_date = datetime.datetime.combine(
                (previous_date + datetime.timedelta(
                    days=NEWSLETTER_DURATION)),
                datetime.time(0, 0, 0, tzinfo=pytz.UTC))

        to_send = previous_date is None or \
            previous_date <= now
        if to_send:
            localizer = request.localizer
            mail_template = {
                'subject': _('${name}, voici des idées qui pourraient vous intéresser!'),
                'template': self.mail_template
            }
            members = context.news_letter_members
            for member in [m for m in members if getattr(m, 'email', '')]:
                name = getattr(
                    member, 'first_name', member.title)
                subject = localizer.translate(
                    _(mail_template['subject'],
                      mapping={'name': name}))
                entities = find_entities(
                    interfaces=[IProposal, Iidea],
                    metadata_filter={
                        'content_types': ['idea', 'proposal'],
                        'states': ['published'],
                        'keywords': getattr(member, 'keywords', [])})

                result = []
                for obj in entities:
                    result.append(obj)
                    if len(result) == 5:
                        break
                if result:
                    body = renderers.render(
                        mail_template['template'], {'entities': result,
                                                    'name': name}, request)
                    alert('email', [context.get_site_sender()], [member.email],
                          subject=subject, html=body)

            root.newsletter_date = now

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors
