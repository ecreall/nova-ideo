# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from BTrees.OOBTree import OOBTree
from zope.interface import implementer
from pyramid import renderers

from substanced.util import get_oid
from substanced.content import content

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import SharedMultipleProperty
from pontus.core import VisualisableElement

from novaideo.content.processes import get_states_mapping
from .interface import(
    IAlert)
from novaideo.layout import GlobalLayout
from novaideo import _
from novaideo.utilities.util import html_to_text


class InternalAlertKind(object):
    """Alert's kinds"""
    comment_alert = 'comment_alert'
    content_alert = 'content_alert'
    working_group_alert = 'working_group_alert'
    moderation_alert = 'moderation_alert'
    examination_alert = 'examination_alert'
    support_alert = 'support_alert'
    admin_alert = 'admin_alert'


@content(
    'alert',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(IAlert)
class Alert(VisualisableElement, Entity):
    """Alert class"""
    users_to_alert = SharedMultipleProperty('users_to_alert')
    subjects = SharedMultipleProperty('subjects')

    def __init__(self, kind, **kwargs):
        super(Alert, self).__init__(**kwargs)
        self.set_data(kwargs)
        self.kind = kind
        self.users_toalert = OOBTree()
        self.users_toexclude = OOBTree()

    @property
    def pattern(self):
        return INTERNAL_ALERTS.get(self.kind, None)

    @property
    def templates(self):
        return self.pattern.templates

    @property
    def icon(self):
        return self.pattern.get_icon(self)

    def init_alert(self, users, subjects=[], exclude=[]):
        self.subscribe(users)
        for subject in subjects:
            self.addtoproperty('subjects', subject)

        self.exclude(exclude)

    def subscribe(self, users):
        if not isinstance(users, (list, tuple, set)):
            users = [users]

        for user in users:
            oid = get_oid(user, user)
            self.users_toalert[str(oid)] = oid

    def unsubscribe(self, user):
        key = str(get_oid(user, user))
        if key in self.users_toalert:
            self.users_toalert.pop(key)

        user.addtoproperty('old_alerts', self)
        self.reindex()

    def exclude(self, users):
        if not isinstance(users, (list, tuple, set)):
            users = [users]

        for user in users:
            oid = get_oid(user, user)
            self.users_toexclude[str(oid)] = oid

    def is_to_alert(self, user):
        key = str(get_oid(user, user))
        #TODO self not in user.old_alerts
        return key in self.users_toalert and \
            key not in self.users_toexclude

    def get_subject_state(self, subject, user, last_state=False):
        states = getattr(subject, 'state_or_none', [None])
        state = states[0]
        if last_state:
            state = states[-1]

        return get_states_mapping(
            user, subject, state)

    def render(self, template, current_user, request):
        layout_manager = getattr(request, 'layout_manager', None)
        layout = layout_manager.layout if layout_manager \
            else GlobalLayout(None, request)
        render_dict = {
            'object': self,
            'current_user': current_user,
            'layout': layout
        }
        return renderers.render(
            self.templates[template],
            render_dict,
            request)

    def is_kind_of(self, kind):
        return kind == self.kind

    def has_args(self, **kwargs):
        for key in kwargs:
            if getattr(self, key, None) != kwargs[key]:
                return False

        return True


class _CommentAlert(object):
    icon = 'glyphicon glyphicon-comment'
    templates = {
        'default': 'novaideo:views/templates/alerts/comment_result.pt',
        'small': 'novaideo:views/templates/alerts/small_comment_result.pt',
        'notification': 'novaideo:views/templates/alerts/notification_comment_result.pt'
    }

    def __call__(self, **kwargs):
        return Alert(InternalAlertKind.comment_alert, **kwargs)

    def get_icon(self, alert):
        return self.icon

    def get_notification_data(self, subject, user, request, alert):
        html_message = alert.render(
            'notification', user, request)
        message = html_to_text(html_message)
        localizer = request.localizer
        title = localizer.translate(_('New message in')) + ' ' + localizer.translate(
            subject.get_title(user))
        channel = subject
        subject = channel.get_subject(user)
        if getattr(alert, 'comment_kind', '') == 'discuss':
            subject = channel.get_subject(subject)

        return {
            'title': title,
            'message': message,
            'url': request.resource_url(subject, '@@index') + \
            '#comment-' + str(getattr(alert, 'comment_oid', 'None'))}


CommentAlert = _CommentAlert()


class _ContentAlert(object):
    icon = 'glyphicon glyphicon-bookmark'
    templates = {
        'default': 'novaideo:views/templates/alerts/content_result.pt',
        'small': 'novaideo:views/templates/alerts/small_content_result.pt',
        'notification': 'novaideo:views/templates/alerts/notification_content_result.pt',
        'nia': 'novaideo:views/templates/alerts/nia_content_result.pt'
    }

    def __call__(self, **kwargs):
        return Alert(InternalAlertKind.content_alert, **kwargs)

    def get_icon(self, alert):
        return self.icon

    def get_notification_data(self, subject, user, request, alert):
        html_message = alert.render(
            'notification', user, request)
        message = html_to_text(html_message)
        localizer = request.localizer
        return {
            'title': localizer.translate(_('Information on')) + ' ' + localizer.translate(
                subject.get_title(user)),
            'message': message,
            'url': request.resource_url(subject, '@@index')}


ContentAlert = _ContentAlert()


class _WorkingGroupAlert(object):
    icon = 'novaideo-icon icon-wg'
    templates = {
        'default': 'novaideo:views/templates/alerts/wg_alert_result.pt',
        'small': 'novaideo:views/templates/alerts/small_wg_alert_result.pt',
        'notification': 'novaideo:views/templates/alerts/notification_wg_alert_result.pt',
        'nia': 'novaideo:views/templates/alerts/nia_wg_result.pt'
        }

    def __call__(self, **kwargs):
        return Alert(InternalAlertKind.working_group_alert, **kwargs)

    def get_icon(self, alert):
        return self.icon

    def get_notification_data(self, subject, user, request, alert):
        html_message = alert.render(
            'notification', user, request)
        message = html_to_text(html_message)
        localizer = request.localizer
        return {
            'title': localizer.translate(_('New on')) + ' ' + localizer.translate(
                subject.get_title(user)),
            'message': message,
            'url': request.resource_url(subject, '@@index')}


WorkingGroupAlert = _WorkingGroupAlert()


class _ModerationAlert(object):
    icon = 'octicon octicon-check'
    templates = {
        'default': 'novaideo:views/templates/alerts/moderation_result.pt',
        'small': 'novaideo:views/templates/alerts/small_moderation_result.pt',
        'notification': 'novaideo:views/templates/alerts/notification_moderation_result.pt'
    }

    def __call__(self, **kwargs):
        return Alert(InternalAlertKind.moderation_alert, **kwargs)

    def get_icon(self, alert):
        return self.icon

    def get_notification_data(self, subject, user, request, alert):
        html_message = alert.render(
            'notification', user, request)
        message = html_to_text(html_message)
        localizer = request.localizer
        return {
            'title': localizer.translate(_('Moderation of')) + ' ' + localizer.translate(
                subject.get_title(user)),
            'message': message,
            'url': request.resource_url(subject, '@@index')}


ModerationAlert = _ModerationAlert()


class _ExaminationAlert(object):
    icon = 'octicon octicon-checklist'
    templates = {
        'default': 'novaideo:views/templates/alerts/examination_result.pt',
        'small': 'novaideo:views/templates/alerts/small_examination_result.pt',
        'notification': 'novaideo:views/templates/alerts/notification_examination_result.pt',
        'nia': 'novaideo:views/templates/alerts/nia_examination_result.pt'
    }

    def __call__(self, **kwargs):
        return Alert(InternalAlertKind.examination_alert, **kwargs)

    def get_icon(self, alert):
        return self.icon

    def get_notification_data(self, subject, user, request, alert):
        html_message = alert.render(
            'notification', user, request)
        message = html_to_text(html_message)
        localizer = request.localizer
        return {
            'title': localizer.translate(_('Examination of')) + ' ' + localizer.translate(
                subject.get_title(user)),
            'message': message,
            'url': request.resource_url(subject, '@@index')}


ExaminationAlert = _ExaminationAlert()


class _SupportAlert(object):
    icon = 'octicon octicon-triangle-up'
    templates = {
        'default': 'novaideo:views/templates/alerts/support_result.pt',
        'small': 'novaideo:views/templates/alerts/small_support_result.pt',
        'notification': 'novaideo:views/templates/alerts/notification_support_result.pt'
    }

    def __call__(self, **kwargs):
        return Alert(InternalAlertKind.support_alert, **kwargs)

    def get_icon(self, alert):
        support_kind = getattr(alert, 'support_kind', '')
        if support_kind == 'support':
            return 'octicon octicon-triangle-up'

        if support_kind == 'oppose':
            return 'octicon octicon-triangle-down'

        if support_kind == 'withdraw':
            return 'glyphicon glyphicon-remove'

        return self.icon

    def get_notification_data(self, subject, user, request, alert):
        html_message = alert.render(
            'notification', user, request)
        message = html_to_text(html_message)
        localizer = request.localizer
        return {
            'title': localizer.translate(_('Evaluation of')) + ' ' + localizer.translate(
                subject.get_title(user)),
            'message': message,
            'url': request.resource_url(subject, '@@index')}


SupportAlert = _SupportAlert()


class _AdminAlert(object):
    icon = 'glyphicon glyphicon-cog'
    templates = {
        'default': 'novaideo:views/templates/alerts/admin_result.pt',
        'small': 'novaideo:views/templates/alerts/small_admin_result.pt',
        'notification': 'novaideo:views/templates/alerts/notification_admin_result.pt'
    }

    def __call__(self, **kwargs):
        return Alert(InternalAlertKind.admin_alert, **kwargs)

    def get_icon(self, alert):
        return self.icon

    def get_notification_data(self, subject, user, request, alert):
        html_message = alert.render(
            'notification', user, request)
        message = html_to_text(html_message)
        localizer = request.localizer
        return {
            'title': localizer.translate(_('Administration')) + ': ' + localizer.translate(
                subject.get_title(user)),
            'message': message,
            'url': request.resource_url(subject, '@@index')}


AdminAlert = _AdminAlert()

INTERNAL_ALERTS = {
    InternalAlertKind.comment_alert: CommentAlert,
    InternalAlertKind.working_group_alert: WorkingGroupAlert,
    InternalAlertKind.moderation_alert: ModerationAlert,
    InternalAlertKind.examination_alert: ExaminationAlert,
    InternalAlertKind.support_alert: SupportAlert,
    InternalAlertKind.content_alert: ContentAlert,
    InternalAlertKind.admin_alert: AdminAlert,
}
