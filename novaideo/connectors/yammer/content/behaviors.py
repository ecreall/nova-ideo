# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the
Idea management process definition.
"""
import transaction
import datetime
import pytz
from persistent.list import PersistentList
from persistent.dict import PersistentDict

from pyramid.security import remember
from pyramid.httpexceptions import HTTPFound

from substanced.util import get_oid
from substanced.event import LoggedIn
from substanced.util import find_service

from dace.processinstance.activity import InfiniteCardinality
from dace.interfaces import IEntity
from dace.objectofcollaboration.principal.util import (
    has_role,
    has_any_roles,
    grant_roles)
from dace.util import name_chooser, find_catalog, getSite
from dace.processinstance.core import PROCESS_HISTORY_KEY

from novaideo import _, my_locale_negotiator
from novaideo.content.interface import IPerson, INovaIdeoApplication
from novaideo.content.processes import global_user_processsecurity
from novaideo.connectors.yammer import IYammerConnector


def create_user(context, request, appstruct):
    if appstruct and 'user_data' in appstruct:
        from novaideo.content.processes.user_management.behaviors import (
            initialize_tokens)
        from novaideo.content.person import Person
        source_data = appstruct.get('source_data', {})
        data = appstruct.get('user_data', {})
        root = getSite()
        locale = my_locale_negotiator(request)
        data['locale'] = locale
        person = Person(**data)
        person.source_data = PersistentDict(source_data)
        principals = find_service(root, 'principals')
        name = person.first_name + ' ' + person.last_name
        users = principals['users']
        name = name_chooser(users, name=name)
        users[name] = person
        grant_roles(person, roles=('Member',))
        grant_roles(person, (('Owner', person),))
        person.state.append('active')
        initialize_tokens(person, root.tokens_mini)
        person.init_annotations()
        person.annotations.setdefault(
            PROCESS_HISTORY_KEY, PersistentList())
        person.reindex()
        root.addtoproperty('news_letter_members', person)
        newsletters = root.get_newsletters_automatic_registration()
        email = getattr(person, 'email', '')
        if newsletters and email:
            for newsletter in newsletters:
                newsletter.subscribe(
                    person.first_name, person.last_name, email)

        transaction.commit()
        return person

    return None


def validate_user(context, request, appstruct):
    user_id = appstruct.get('user_data', {}).get('email', None)
    novaideo_catalog = find_catalog('novaideo')
    dace_catalog = find_catalog('dace')
    identifier_index = novaideo_catalog['identifier']
    object_provides_index = dace_catalog['object_provides']
    query = object_provides_index.any([IPerson.__identifier__]) &\
        identifier_index.any([user_id])
    users = list(query.execute().all())
    user = users[0] if users else None
    if user is None:
        user = create_user(context, request, appstruct)
    else:
        user.source_data = PersistentDict(appstruct.get('source_data', {}))

    valid = user and (has_role(user=user, role=('SiteAdmin', )) or \
                      'active' in getattr(user, 'state', []))
    headers = None
    if valid:
        request.session.pop('novaideo.came_from', None)
        headers = remember(request, get_oid(user))
        request.registry.notify(
            LoggedIn(
                user.email, user,
                context, request))
        user.last_connection = datetime.datetime.now(tz=pytz.UTC)
        if hasattr(user, 'reindex'):
            user.reindex()

    return user, valid, headers


def login_roles_validation(process, context):
    return has_any_roles(roles=('Anonymous', 'Collaborator'))


def login_processsecurity_validation(process, context):
    yammer_connectors = list(getSite().get_connectors('yammer'))
    return False if not yammer_connectors else yammer_connectors[0].log_in


class LogIn(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'body-action'
    style_picto = 'icon fa fa-plug'
    style_order = 0
    template = 'novaideo:connectors/yammer/views/templates/log_in.pt'
    title = _('Log in with Yammer')
    access_controled = True
    context = INovaIdeoApplication
    roles_validation = login_roles_validation
    processsecurity_validation = login_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        user, valid, headers = validate_user(
            context, request, appstruct)
        if valid:
            came_from = appstruct.get('came_from')
            return {'headers': headers, 'came_from': came_from}

        return {'headers': None}

    def redirect(self, context, request, **kw):
        headers = kw.get('headers')
        if headers:
            came_from = kw.get('came_from')
            return {'redirect': HTTPFound(location=came_from, headers=headers),
                    'logged': True}

        root = getSite()
        return {'redirect': HTTPFound(request.resource_url(root)),
                'logged': False}


def createidea_roles_validation(process, context):
    return has_role(role=('SiteAdmin',))


def createidea_processsecurity_validation(process, context):
    yammer_connectors = list(getSite().get_connectors('yammer'))
    return not yammer_connectors and \
        global_user_processsecurity()


class CreateConnector(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'body-action'
    style_picto = 'icon fa fa-plug'
    style_order = 0
    template = 'novaideo:connectors/yammer/views/templates/create_connector.pt'
    title = _('Add a Yammer connector')
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = createidea_roles_validation
    processsecurity_validation = createidea_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        client_id = request.registry.settings['yammer.client_id']
        client_secret = request.registry.settings['yammer.client_secret']
        yammer_connector = appstruct['_object_data']
        yammer_connector.set_client_data(client_id, client_secret)
        root.addtoproperty('connectors', yammer_connector)
        root.yammer_connector = yammer_connector.__name__
        yammer_connector.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(request.root, "@@seeconnectors"))


def conf_roles_validation(process, context):
    return has_role(role=('SiteAdmin',))


def conf_processsecurity_validation(process, context):
    return global_user_processsecurity()


class Configure(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'icon glyphicon glyphicon-wrench'
    style_order = 1000
    title = _('Configure')
    submission_title = _('Save')
    context = IYammerConnector
    roles_validation = conf_roles_validation
    processsecurity_validation = conf_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(request.root, "@@seeconnectors"))


def remove_roles_validation(process, context):
    return has_role(role=('SiteAdmin',))


def remove_processsecurity_validation(process, context):
    return global_user_processsecurity()


class Remove(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'icon glyphicon glyphicon-trash'
    style_order = 1000
    title = _('Remove')
    submission_title = _('Save')
    context = IYammerConnector
    roles_validation = remove_roles_validation
    processsecurity_validation = remove_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        root.delfromproperty('connectors', context)
        if hasattr(root, 'yammer_connector'):
            del root.yammer_connector

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(request.root, "@@seeconnectors"))
