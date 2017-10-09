# -*- coding: utf8 -*-
# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.threadlocal import get_current_request, get_current_registry
from pyramid.httpexceptions import HTTPFound
from pyramid.config import Configurator

from velruse.providers.twitter import add_twitter_login
from dace.processinstance.activity import InfiniteCardinality
from dace.objectofcollaboration.principal.util import (
    has_role,
    has_any_roles)
from dace.util import getSite

from novaideo import _
from novaideo.content.interface import INovaIdeoApplication
from novaideo.content.processes import global_user_processsecurity
from novaideo.connectors.twitter import ITwitterConnector
from novaideo.connectors.core import TWITTER_CONNECTOR_ID


def login_roles_validation(process, context):
    return has_any_roles(roles=('Anonymous', 'Collaborator'))


def login_processsecurity_validation(process, context):
    twitter_connectors = list(getSite().get_connectors(TWITTER_CONNECTOR_ID))
    return False if not twitter_connectors else twitter_connectors[0].log_in


class LogIn(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'body-action'
    style_picto = 'icon fa fa-plug'
    style_order = 0
    template = 'novaideo:connectors/twitter/views/templates/log_in.pt'
    title = _('Log in with Twitter')
    access_controled = True
    context = INovaIdeoApplication
    roles_validation = login_roles_validation
    processsecurity_validation = login_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        # see Login view in core.views
        return {}


def create_roles_validation(process, context):
    return has_role(role=('SiteAdmin',))


def create_processsecurity_validation(process, context):
    request = get_current_request()
    consumer_key = request.registry.settings.get('twitter.consumer_key', None)
    consumer_secret = request.registry.settings.get('twitter.consumer_secret', None)
    if not consumer_key or not consumer_secret:
        return False

    twitter_connectors = list(getSite().get_connectors(TWITTER_CONNECTOR_ID))
    return not twitter_connectors and \
        global_user_processsecurity()


class CreateConnector(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'body-action'
    style_picto = 'icon fa fa-plug'
    style_order = 0
    template = 'novaideo:connectors/twitter/views/templates/create_connector.pt'
    title = _('Add a Twitter connector')
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = create_roles_validation
    processsecurity_validation = create_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        consumer_key = request.registry.settings['twitter.consumer_key']
        consumer_secret = request.registry.settings['twitter.consumer_secret']
        twitter_connector = appstruct['_object_data']
        twitter_connector.set_client_data(consumer_key, consumer_secret)
        root.addtoproperty('connectors', twitter_connector)
        root.twitter_connector = twitter_connector.__name__
        twitter_connector.reindex()
        name = twitter_connector.connector_id
        registry = get_current_registry()
        config = Configurator(registry=registry)
        add_twitter_login(
            config,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            login_path='/login/'+name,
            callback_path='/login/'+name+'/callback',
            name=name)
        config.commit()
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
    context = ITwitterConnector
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
    style_order = 1002
    title = _('Remove')
    submission_title = _('Continue')
    context = ITwitterConnector
    roles_validation = remove_roles_validation
    processsecurity_validation = remove_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        root.delfromproperty('connectors', context)
        if hasattr(root, 'twitter_connector'):
            del root.twitter_connector

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(request.root, "@@seeconnectors"))
