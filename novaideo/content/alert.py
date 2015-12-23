# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from zope.interface import implementer

from substanced.content import content

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import SharedMultipleProperty
from pontus.core import VisualisableElement

from novaideo.content.processes import get_states_mapping
from .interface import(
    IAlert)


class AlertKind(object):
    """Alert's kinds"""
    comment_alert = 'comment_alert'
    content_alert = 'content_alert'
    working_group_alert = 'working_group_alert'
    moderation_alert = 'moderation_alert'
    examination_alert = 'examination_alert'
    support_alert = 'support_alert'


@content(
    'alert',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IAlert)
class Alert(VisualisableElement, Entity):
    """Alert class"""
    templates = {
        AlertKind.comment_alert: {
            'default': 'novaideo:views/templates/alerts/comment_result.pt',
            'small': 'novaideo:views/templates/alerts/small_comment_result.pt'},
        AlertKind.content_alert: {
            'default': 'novaideo:views/templates/alerts/content_result.pt',
            'small': 'novaideo:views/templates/alerts/small_content_result.pt'
        },
        AlertKind.working_group_alert: {
            'default': 'novaideo:views/templates/alerts/wg_alert_result.pt',
            'small': 'novaideo:views/templates/alerts/small_wg_alert_result.pt'
        },
        AlertKind.moderation_alert: {
            'default': 'novaideo:views/templates/alerts/moderation_result.pt',
            'small': 'novaideo:views/templates/alerts/small_moderation_result.pt'
        },
        AlertKind.examination_alert: {
            'default': 'novaideo:views/templates/alerts/examination_result.pt',
            'small': 'novaideo:views/templates/alerts/small_examination_result.pt'
        },
        AlertKind.support_alert: {
            'default': 'novaideo:views/templates/alerts/support_result.pt',
            'small': 'novaideo:views/templates/alerts/small_support_result.pt'
        }
    }
    icon = 'glyphicon glyphicon-bell'
    users_to_alert = SharedMultipleProperty('users_to_alert', 'alerts')
    alerted_users = SharedMultipleProperty('alerted_users', 'old_alerts')
    subjects = SharedMultipleProperty('subjects')

    def __init__(self, kind, **kwargs):
        super(Alert, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.kind = kind

    def init_alert(self, users, subjects=[]):
        self.subscribe(users)
        for subject in subjects:
            self.addtoproperty('subjects', subject)

    def subscribe(self, users):
        if not isinstance(users, (list, tuple)):
            users = [users]

        for user in users:
            self.addtoproperty('users_to_alert', user)

    def unsubscribe(self, user):
        self.delfromproperty('users_to_alert', user)
        self.addtoproperty('alerted_users', user)

    def get_subject_state(self, subject, user):
        return get_states_mapping(
            user, subject,
            getattr(subject, 'state_or_none', [None])[0])

    def get_templates(self):
        return self.templates.get(self.kind, {})


class _CommentAlert(object):

    def __call__(self, **kwargs):
        return Alert(AlertKind.comment_alert, **kwargs)


CommentAlert = _CommentAlert()


class _ContentAlert(object):

    def __call__(self, **kwargs):
        return Alert(AlertKind.content_alert, **kwargs)


ContentAlert = _ContentAlert()


class _WorkingGroupAlert(object):

    def __call__(self, **kwargs):
        return Alert(AlertKind.working_group_alert, **kwargs)


WorkingGroupAlert = _WorkingGroupAlert()


class _ModerationAlert(object):

    def __call__(self, **kwargs):
        return Alert(AlertKind.moderation_alert, **kwargs)


ModerationAlert = _ModerationAlert()


class _ExaminationAlert(object):

    def __call__(self, **kwargs):
        return Alert(AlertKind.examination_alert, **kwargs)


ExaminationAlert = _ExaminationAlert()


class _SupportAlert(object):

    def __call__(self, **kwargs):
        return Alert(AlertKind.support_alert, **kwargs)


SupportAlert = _SupportAlert()
