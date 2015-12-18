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
    IAlert,
    ICommentAlert,
    IResponsAlert,
    IModerationAlert,
    IExaminationAlert,
    IWorkingGroupAlert,
    ISupportAlert,
    IContentAlert)


@implementer(IAlert)
class Alert(VisualisableElement, Entity):
    """Alert class"""
    templates = {}
    icon = 'glyphicon glyphicon-bell'
    users_to_alert = SharedMultipleProperty('users_to_alert', 'alerts')
    alerted_users = SharedMultipleProperty('alerted_users', 'old_alerts')
    subjects = SharedMultipleProperty('subjects')

    def __init__(self, **kwargs):
        super(Alert, self).__init__(**kwargs)
        self.set_data(kwargs)

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


@content(
    'commentalert',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(ICommentAlert)
class CommentAlert(Alert):
    """Alert class"""
    templates = {'default': 'novaideo:views/templates/alerts/comment_result.pt',
                 'small': 'novaideo:views/templates/alerts/small_comment_result.pt'}
    icon = 'glyphicon glyphicon-comment'


@content(
    'responsalert',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IResponsAlert)
class ResponsAlert(Alert):
    """Alert class"""
    templates = {'default': 'novaideo:views/templates/alerts/respons_result.pt',
                 'small': 'novaideo:views/templates/alerts/small_respons_result.pt'}
    icon = 'glyphicon glyphicon-share-alt'


@content(
    'moderationalert',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IModerationAlert)
class ModerationAlert(Alert):
    """Alert class"""
    templates = {'default': 'novaideo:views/templates/alerts/moderation_result.pt',
                 'small': 'novaideo:views/templates/alerts/small_moderation_result.pt'}
    icon = 'octicon octicon-check'


@content(
    'examinationalert',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IExaminationAlert)
class ExaminationAlert(Alert):
    """Alert class"""
    templates = {'default': 'novaideo:views/templates/alerts/examination_result.pt',
                 'small': 'novaideo:views/templates/alerts/small_examination_result.pt'}
    icon = 'octicon octicon-checklist'


@content(
    'wgalert',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IWorkingGroupAlert)
class WorkingGroupAlert(Alert):
    """Alert class"""
    templates = {'default': 'novaideo:views/templates/alerts/wg_alert_result.pt',
                 'small': 'novaideo:views/templates/alerts/small_wg_alert_result.pt'}
    icon = 'md md-group'

    def get_subject_state(self, subject, user):
        return get_states_mapping(user, subject,
            getattr(subject, 'state_or_none', [None])[0])


@content(
    'supportalert',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(ISupportAlert)
class SupportAlert(Alert):
    """Alert class"""
    templates = {'default': 'novaideo:views/templates/alerts/support_result.pt',
                 'small': 'novaideo:views/templates/alerts/small_support_result.pt'}
    icon = 'glyphicon glyphicon-hand-down'


@content(
    'contentalert',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IContentAlert)
class ContentAlert(Alert):
    """Alert class"""
    templates = {'default': 'novaideo:views/templates/alerts/content_result.pt',
                 'small': 'novaideo:views/templates/alerts/small_content_result.pt'}
    icon = 'glyphicon glyphicon-bookmark'
