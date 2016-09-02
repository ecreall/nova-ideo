# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the
Channel management process definition.
"""
from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    get_current)
from dace.processinstance.activity import InfiniteCardinality

from novaideo.content.processes import global_user_processsecurity
from novaideo.content.interface import IChannel
from novaideo import _


def subscribe_processsecurity_validation(process, context):
    user = get_current()
    return context.subject and user not in context.members and\
        not context.is_discuss() and\
        global_user_processsecurity()


class Subscribe(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_picto = 'glyphicon glyphicon-play-circle'
    style_interaction = 'ajax-action'
    style_action_class = 'subscribe-channel-action'
    style_order = 4
    submission_title = _('Continue')
    context = IChannel
    processsecurity_validation = subscribe_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        if user not in context.members:
            context.addtoproperty('members', user)

        return {}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def unsubscribe_processsecurity_validation(process, context):
    user = get_current()
    return context.subject and user in context.members and\
        not context.is_discuss() and\
        global_user_processsecurity()


class Unsubscribe(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_interaction = 'ajax-action'
    style_action_class = 'subscribe-channel-action'
    style_picto = 'glyphicon glyphicon-ban-circle'
    style_order = 3
    submission_title = _('Continue')
    context = IChannel
    processsecurity_validation = unsubscribe_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        if user in context.members:
            context.delfromproperty('members', user)

        return {}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))

#TODO behaviors
