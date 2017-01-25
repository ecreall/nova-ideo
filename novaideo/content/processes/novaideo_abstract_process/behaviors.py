# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import pytz
import datetime
from pyramid.httpexceptions import HTTPFound
from persistent.list import PersistentList

from dace.objectofcollaboration.principal import User
from dace.objectofcollaboration.principal.util import (
    has_role,
    get_current)
from dace.processinstance.activity import InfiniteCardinality

from ..user_management.behaviors import global_user_processsecurity
from novaideo.content.interface import (
    INovaIdeoApplication, ISearchableEntity,
    IEmojiable)
from novaideo import _, nothing


def select_roles_validation(process, context):
    return has_role(role=('Member',))


def select_processsecurity_validation(process, context):
    user = get_current()
    return user is not context and \
           context not in getattr(user, 'selections', []) and \
           global_user_processsecurity()


def select_state_validation(process, context):
    return context.is_published



class SelectEntity(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'communication-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'direct'
    style_picto = 'glyphicon glyphicon-star-empty'
    style_order = 100
    isSequential = False
    context = ISearchableEntity
    roles_validation = select_roles_validation
    processsecurity_validation = select_processsecurity_validation
    state_validation = select_state_validation

    def get_title(self, context, request, nb_only=False):
        len_selections = getattr(context, 'len_selections', 0)
        if nb_only:
            return str(len_selections)

        return _("${title} (${nember})",
                 mapping={'nember': len_selections,
                          'title': request.localizer.translate(self.title)})

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        user.addtoproperty('selections', context)
        if not isinstance(context, User):
            channel = getattr(context, 'channel', None)
            if channel and user not in channel.members:
                channel.addtoproperty('members', user)

        user.reindex()
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def selecta_roles_validation(process, context):
    return has_role(role=('Anonymous',), ignore_superiors=True)


def selecta_processsecurity_validation(process, context):
    return True


class SelectEntityAnonymous(SelectEntity):
    roles_validation = selecta_roles_validation
    processsecurity_validation = selecta_processsecurity_validation
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'

    def start(self, context, request, appstruct, **kw):
        return {}


def deselect_roles_validation(process, context):
    return has_role(role=('Member',))


def deselect_processsecurity_validation(process, context):
    user = get_current()
    return (context in getattr(user, 'selections', [])) and \
           global_user_processsecurity()


class DeselectEntity(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'communication-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'direct'
    style_picto = 'glyphicon glyphicon-star'
    style_order = 101
    isSequential = False
    context = ISearchableEntity
    roles_validation = deselect_roles_validation
    processsecurity_validation = deselect_processsecurity_validation
    state_validation = select_state_validation

    def get_title(self, context, request, nb_only=False):
        len_selections = getattr(context, 'len_selections', 0)
        if nb_only:
            return str(len_selections)

        return _("${title} (${nember})",
                 mapping={'nember': len_selections,
                          'title': request.localizer.translate(self.title)})

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        user.delfromproperty('selections', context)
        if not isinstance(context, User):
            channel = getattr(context, 'channel', None)
            if channel:
                channel.delfromproperty('members', user)

        user.reindex()
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def addr_roles_validation(process, context):
    return has_role(role=('Member',))


def addr_state_validation(process, context):
    return False
    if hasattr(context, 'can_add_reaction'):
        return context.can_add_reaction(process)

    return 'published' in context.state


class AddReaction(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'communication-body-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'
    style_picto = 'novaideo-icon icon-add-emoji'
    template = 'novaideo:views/templates/actions/add_reaction_idea.pt'
    context = IEmojiable
    roles_validation = addr_roles_validation
    state_validation = addr_state_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def deadline_roles_validation(process, context):
    return has_role(role=('Examiner', ))


def adddeadline_processsecurity_validation(process, context):
    return getattr(context, 'content_to_examine', []) and\
           datetime.datetime.now(tz=pytz.UTC) >= \
           context.deadlines[-1].replace(tzinfo=pytz.UTC) and \
           global_user_processsecurity()


class AddDeadLine(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-time'
    style_order = 9
    submission_title = _('Save')
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = deadline_roles_validation
    processsecurity_validation = adddeadline_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        if hasattr(context, 'deadlines'):
            context.deadlines.append(appstruct['deadline'])
        else:
            context.deadlines = PersistentList([appstruct['deadline']])

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def editdeadline_processsecurity_validation(process, context):
    return getattr(context, 'content_to_examine', []) and\
           global_user_processsecurity() and \
           getattr(context, 'deadlines', [])


class EditDeadLine(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-time'
    style_order = 9
    submission_title = _('Save')
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = deadline_roles_validation
    processsecurity_validation = editdeadline_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        current = context.deadlines[-1]
        context.deadlines.remove(current)
        context.deadlines.append(appstruct['deadline'])
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))

#TODO behaviors
