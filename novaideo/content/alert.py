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

from .interface import(
    IAlert,
    ICommentAlert,
    IResponsAlert)


@implementer(IAlert)
class Alert(VisualisableElement, Entity):
    """Alert class"""
    templates = {}
    icon = 'glyphicon glyphicon-bell'
    users_to_alert = SharedMultipleProperty('users_to_alert', 'alerts')
    alerted_users = SharedMultipleProperty('alerted_users', 'old_alerts')
    subjects = SharedMultipleProperty('subjects')

    def subscribe(self, user):
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

