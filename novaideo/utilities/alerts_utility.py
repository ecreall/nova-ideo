# -*- coding: utf8 -*-
# Copyright (c) 2015 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import json
import requests
from urllib.request import urlopen

from pyramid.threadlocal import get_current_request

from dace.objectofcollaboration.principal.util import get_current

from novaideo.ips.mailer import mailer_send
# from novaideo.content.resources import (
#     arango_server, create_collection)
from novaideo.content.alert import INTERNAL_ALERTS
from novaideo import log
from .util import html_to_text


SLACK_CHANNELS = {
    'questionnaire': {'url': 'https://hooks.slack.com/services/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',
                      'name': 'questionnaires'},
    'improve': {'url': 'https://hooks.slack.com/services/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',
                'name': 'ameliorations'},
    'lac_contact': {'url': 'https://hooks.slack.com/services/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',
                    'name': 'lac_contact'},
}


def alert_slack(senders=[], recipients=[], **kwargs):
    """
        recipients: ['improve', 'questionnaire']
    """
    for recipient in recipients:
        channel_data = SLACK_CHANNELS[recipient]
        kwargs['channel'] = "#" + channel_data['name']
        kwargs['username'] = 'webhookbot'
        kwargs = 'payload=' + json.dumps(kwargs)
        url = channel_data['url']
        urlopen(url, kwargs.encode())


# def alert_arango(senders=[], recipients=[], **kwargs):
#     """
#         recipients: ['creationculturelle.improve']
#     """
#     for recipient in recipients:
#         recipient_parts = recipient.split('.')
#         db_id = recipient_parts[0]
#         collection_id = recipient_parts[1]
#         db = arango_server.db(db_id)
#         if db:
#             collection = create_collection(db, collection_id)
#             collection.create_document(kwargs)


def alert_email(senders=[], recipients=[], **kwargs):
    """
        recipients: ['mail@mail.com']
    """
    sender = senders[0]
    subject = kwargs.get('subject', '')
    mail = kwargs.get('body', None)
    html = kwargs.get('html', None)
    attachments = kwargs.get('attachments', [])
    if mail or html:
        mailer_send(
            subject=subject, body=mail,
            html=html, attachments=attachments,
            recipients=recipients, sender=sender)


def alert_internal(senders=[], recipients=[], **kwargs):
    """
        recipients: [user1, user2],
        kwargs: {'internal_kind': 'content_alert',...}
    """
    kind = kwargs.pop('internal_kind', None)
    alert_class = INTERNAL_ALERTS.get(kind, None)
    if alert_class:
        subjects = kwargs.pop('subjects', [])
        sender = senders[0]
        alert = alert_class(**kwargs)
        sender.addtoproperty('alerts', alert)
        alert.init_alert(recipients, subjects)
        if getattr(sender, 'activate_push_notification', False):
            app_id = getattr(sender, 'app_id')
            players_ids = [getattr(user, 'notification_ids', [])
                           for user in recipients]
            players_ids = [item for sublist in players_ids for item in sublist]
            # players_ids = ['c72acc6f-ed75-4969-ae75-b8e78fa75b9d']
            if players_ids:
                subject = subjects[0] if subjects else sender
                request = get_current_request()
                html_message = alert.render(
                    'small', get_current(request), request)
                message = html_to_text(html_message)
                header = {
                    "Content-Type": "application/json"}
                payload = {"app_id": app_id,
                           "headings": {"en": subject.title, "fr": subject.title},
                           "contents": {"en": message, "fr": message},
                           "include_player_ids": players_ids
                           }
                try:
                    requests.post(
                        "https://onesignal.com/api/v1/notifications",
                        headers=header, data=json.dumps(payload), timeout=0.1)
                except Exception:
                    pass


def alert(kind="", senders=[], recipients=[], **kwargs):
    alert_op = ALERTS.get(kind, None)
    if alert_op:
        return alert_op(senders, recipients, **kwargs)

    log.warning("Alert kind {kind} not implemented".format(kind=kind))
    return None


ALERTS = {
    'internal': alert_internal,
    'slack': alert_slack,
    # 'arango': alert_arango,
    'email': alert_email
}
