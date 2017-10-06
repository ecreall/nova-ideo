# -*- coding: utf8 -*-
# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import io
from persistent.list import PersistentList

from pyramid.threadlocal import get_current_request
from pyramid.httpexceptions import HTTPFound

import yampy

from dace.processinstance.activity import InfiniteCardinality
from dace.objectofcollaboration.principal.util import (
    has_role,
    has_any_roles,
    grant_roles,
    get_current)
from dace.util import find_catalog, getSite, getAllBusinessAction
from pontus.file import File

from novaideo import _
from novaideo.content.interface import INovaIdeoApplication, Iidea
from novaideo.content.processes import global_user_processsecurity
from novaideo.content.idea import Idea
from novaideo.content.comment import Comment
from novaideo.connectors.core.content import get_or_create_user, validate_user
from novaideo.connectors.core import YAMMER_CONNECTOR_ID
from novaideo.connectors.yammer import IYammerConnector
from novaideo.utilities.util import html_to_text


def _get_repleis(request, messages, sourc_id, access_token):
    result = {}
    for message in messages:
        if message['replied_to_id'] == sourc_id:
            message_id = message['id']
            result[message_id] = {
                'replies': _get_repleis(
                    request, messages, message_id, access_token),
                'data': get_message_data(request, message, access_token)[0]}

    return result


def upload_files(yammer, files):
    result = []
    for file_ in files:
        try:
            buf = io.BytesIO(
                yammer.client.request(
                    'get', file_['download_url']).content)
            buf.seek(0)
            result.append(File(
                fp=buf, mimetype=file_.get('content_type', None),
                filename=file_.get('original_name', None)))
        except Exception:
            continue

    return result


def get_message_data(request, message_or_id, access_token, include_topics=False, include_replies=False):
    yammer = yampy.Yammer(access_token=access_token)
    message = {}
    message_id = None
    if isinstance(message_or_id, dict):
        message = message_or_id
        message_id = message_or_id['id']
    else:
        message_id = message_or_id
        message = yammer.messages.find(message_id=message_id)

    if message:
        # get author
        user_id = message['sender_id']
        user_info = yammer.users.find(user_id)
        user_networks = user_info.get('network_domains')
        source_data = {
            'app_name': YAMMER_CONNECTOR_ID,
            'id': user_info.get('id'),
            'network_domains': user_networks,
            'access_token': None
        }
        user_data = {
            'first_name': user_info.get('first_name'),
            'last_name': user_info.get('last_name'),
            'email': user_info.get('email')
        }
        user = get_or_create_user(request, {
            'source_data': source_data,
            'user_data': user_data,
        }, False)
        # get files
        attached_files = upload_files(yammer, message['attachments'])
        # get keywords
        keywords = []
        thread_id = message['thread_id']
        if include_topics and thread_id:
            thread = yammer.threads.find(thread_id)
            keywords = [t['name'] for t in thread['references']
                        if t['type'] == 'topic']

        # get replies
        replies_result = {}
        if include_replies and thread_id:
            replies = yammer.messages.in_thread(thread_id)
            replies_result = _get_repleis(
                request, replies['messages'], message_id, access_token)

        content_body = html_to_text(message['body']['plain'])
        return {
            'title': content_body[:50]+' ...',
            'text': content_body,
            'keywords': keywords,
            'attached_files': attached_files,
            'author': user
        }, replies_result

    return {}, {}


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


def create_roles_validation(process, context):
    return has_role(role=('SiteAdmin',))


def create_processsecurity_validation(process, context):
    request = get_current_request()
    client_id = request.registry.settings.get('yammer.client_id', None)
    if not client_id:
        return False

    yammer_connectors = list(getSite().get_connectors(YAMMER_CONNECTOR_ID))
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
    roles_validation = create_roles_validation
    processsecurity_validation = create_processsecurity_validation

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
    style_order = 1002
    title = _('Remove')
    submission_title = _('Continue')
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


def import_roles_validation(process, context):
    return has_role(role=('SiteAdmin',))


def import_processsecurity_validation(process, context):
    return global_user_processsecurity()


class Import(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'icon glyphicon glyphicon-import'
    style_order = 1001
    title = _('Import')
    submission_title = _('Continue')
    context = IYammerConnector
    roles_validation = import_roles_validation
    processsecurity_validation = import_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        novaideo_catalog = find_catalog('novaideo')
        dace_catalog = find_catalog('dace')
        identifier_index = novaideo_catalog['identifier']
        object_provides_index = dace_catalog['object_provides']
        query = object_provides_index.any([Iidea.__identifier__]) &\
            identifier_index.any([YAMMER_CONNECTOR_ID+'_'+i for i in appstruct['messages']])
        ideas = list(query.execute().all())
        current_ideas = [i.source_data[YAMMER_CONNECTOR_ID]['id'] for i in ideas]
        messages = [m for m in appstruct['messages'] if m not in current_ideas]
        if not messages:
            return {}

        root = getSite()
        yammer_connectors = list(root.get_connectors(YAMMER_CONNECTOR_ID))
        yammer_connector = yammer_connectors[0] if yammer_connectors else None
        access_token = yammer_connector.get_access_tokens(get_current()).get('access_token', None) \
            if yammer_connector else None

        def replies_to_comment(replies, source, comment_action):
            for reply in replies.values():
                comment_data = reply['data']
                comment = Comment(
                    intention=_('Remark'),
                    comment=comment_data.pop('text'),
                    files=comment_data.pop('attached_files')
                )
                if comment_action:
                    comment_action.execute(
                        source, request, {
                            '_object_data': comment,
                            'user': comment_data.pop('author'),
                            'alert': False,
                        })

                sub_replies = reply['replies']
                if sub_replies:
                    comment_actions = getAllBusinessAction(
                        comment, request,
                        process_id='commentmanagement', node_id='respond',
                        process_discriminator='Application')
                    if comment_actions:
                        replies_to_comment(
                            sub_replies, comment, comment_actions[0])

        if yammer_connector and access_token:
            for m_id in messages:
                idea_data, replies = get_message_data(
                    request, int(m_id), access_token, True, True)

                if idea_data:
                    author = idea_data.pop('author')
                    idea = Idea(**idea_data)
                    root.addtoproperty('ideas', idea)
                    if root.support_ideas:
                        idea.state = PersistentList(
                            ['submitted_support', 'published'])
                    else:
                        idea.state = PersistentList(
                            ['published', 'submitted_support'])

                    idea.init_published_at()
                    grant_roles(user=author, roles=(('Owner', idea), ))
                    idea.setproperty('author', author)
                    idea.subscribe_to_channel(author)
                    idea.format(request)
                    idea.set_source_data({
                        'app_name': YAMMER_CONNECTOR_ID,
                        'id': m_id
                    })
                    idea.reindex()
                    # add comments
                    comment_actions = getAllBusinessAction(
                        idea, request,
                        process_id='ideamanagement', node_id='comment',
                        process_discriminator='Application')
                    if comment_actions:
                        replies_to_comment(replies, idea, comment_actions[0])

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(request.root, ""))
