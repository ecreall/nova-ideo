###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

import sys
import json
import transaction

from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource, WSGIRootResource

from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, \
    connectWS

from dace.util import get_obj

from .util import get_request, get_user
from novaideo.views.idea_management.comment_idea import (
    CommentsView)


class NovaIdeoClientProtocol(WebSocketClientProtocol):

    """
    Simple client that connects to a WebSocket server
    """

    def onOpen(self):
        pass

    def onMessage(self, payload, isBinary):
        pass


# Our WebSocket Server protocol


class NovaIdeoServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        transaction.begin()
        self.factory.register(self)
        transaction.commit()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            transaction.begin()
            events = json.loads(payload.decode('utf8'))
            self.factory.call_events_handlers(self, events)
            transaction.commit()

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        transaction.begin()
        self.factory.unregister(self)
        transaction.commit()


class NovaIdeoServerFactory(WebSocketServerFactory):

    """
    NovaIdeo server factory (based on events)
    """

    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = {}
        self.opened_channels = {}

    def call_events_handlers(self, client, events):
        request = get_request(client)
        current_user = get_user(request)
        messages = {}
        for event in events:
            event_id = event.get('event', None)
            if event_id is not None:
                operation = getattr(self, 'event_'+event_id, None)
                if operation is not None:
                    params = event.get('params', {})
                    params['request'] = request
                    params['current_user'] = current_user
                    try:
                        _messages = operation(client, **params)
                        for user, _events in _messages.items():
                            messages.setdefault(user, [])
                            messages[user].extend(_events)
                    except Exception:
                        pass

        for user, events in messages.items():
            msg = json.dumps(events)
            self.clients[user].sendMessage(msg.encode('utf8'))

    def event_channel_opened(
        self, client, channel_oid, **kwargs):
        request = kwargs.get('request')
        root = request.root
        current_user = kwargs.get('current_user')
        self.opened_channels.setdefault(
            current_user, {'opened': [], 'hidden': []})
        self.opened_channels[current_user]['opened'].append(channel_oid)
        if channel_oid in self.opened_channels[current_user]['hidden']:
            self.opened_channels[current_user]['hidden'].remove(channel_oid)

        root.opened_channels = dict(self.opened_channels)

    def event_all_channels_closed(
        self, client, **kwargs):
        request = kwargs.get('request')
        root = request.root
        current_user = kwargs.get('current_user')
        if current_user in self.opened_channels:
            self.opened_channels.pop(current_user)
            root.opened_channels = dict(self.opened_channels)

    def event_channel_hidden(
        self, client, channel_oid, **kwargs):
        request = kwargs.get('request')
        root = request.root
        current_user = kwargs.get('current_user')
        if current_user in self.opened_channels and \
           channel_oid in self.opened_channels[current_user]['opened']:
            self.opened_channels[current_user]['opened'].remove(channel_oid)
            self.opened_channels[current_user]['hidden'].append(channel_oid)
            root.opened_channels = dict(self.opened_channels)

    def event_typing_comment(
        self, client, channel_oid, **kwargs):
        request = kwargs.get('request')
        current_user = kwargs.get('current_user')
        channel = get_obj(int(channel_oid))
        messages = {}
        for user in self.clients:
            if user is not current_user:
                channels = getattr(user, 'following_channels', [])
                channels.append(request.root.channel)
                opened = self.opened_channels.get(user, {}).get('opened', [])
                hidden = self.opened_channels.get(user, {}).get('hidden', [])
                if channel in channels and \
                   (channel_oid in hidden or channel_oid in opened):
                    events = [{
                        'event': 'typing_comment',
                        'params': {
                            'channel_oid': str(channel_oid),
                            'user_oid': str(current_user.__oid__),
                            'user_name': current_user.first_name
                        }
                    }]
                    messages[user] = events

        return messages

    def event_stop_typing_comment(
        self, client, channel_oid, **kwargs):
        request = kwargs.get('request')
        current_user = kwargs.get('current_user')
        channel = get_obj(int(channel_oid))
        messages = {}
        for user in self.clients:
            if user is not current_user:
                channels = getattr(user, 'following_channels', [])
                channels.append(request.root.channel)
                opened = self.opened_channels.get(user, {}).get('opened', [])
                hidden = self.opened_channels.get(user, {}).get('hidden', [])
                if channel in channels and \
                   (channel_oid in hidden or channel_oid in opened):
                    events = [{
                        'event': 'stop_typing_comment',
                        'params': {
                            'channel_oid': str(channel_oid),
                            'user_oid': str(current_user.__oid__)
                        }
                    }]
                    messages[user] = events

        return messages

    def event_new_comment(
        self, client, context_oid,
        channel_oid, **kwargs):
        request = kwargs.get('request')
        current_user = kwargs.get('current_user')
        context = get_obj(int(context_oid))
        channel = get_obj(int(channel_oid))
        comment = channel.comments[-1]
        messages = {}
        for user in self.clients:
            if user is not current_user:
                channels = getattr(user, 'following_channels', [])
                channels.append(request.root.channel)
                opened = self.opened_channels.get(user, {}).get('opened', [])
                hidden = self.opened_channels.get(user, {}).get('hidden', [])
                if channel in channels:
                    body = ''
                    channel_opened = channel_oid in hidden or channel_oid in opened
                    if channel_opened:
                        request.user = user
                        result_view = CommentsView(context, request)
                        result_view.ignore_unread = channel_oid in opened
                        result_view.comments = [comment]
                        body = result_view.update()['coordinates'][result_view.coordinates][0]['body']

                    events = [{
                        'event': 'new_comment',
                        'params': {
                            'body': body,
                            'channel_hidden': channel_oid in hidden,
                            'user_oid': str(current_user.__oid__),
                            'channel_oid': str(channel_oid)
                        }
                    }]
                    messages[user] = events

        return messages

    def event_edit_comment(
        self, client, context_oid,
        channel_oid, comment_oid, **kwargs):
        request = kwargs.get('request')
        current_user = kwargs.get('current_user')
        context = get_obj(int(context_oid))
        comment = get_obj(int(comment_oid))
        channel = get_obj(int(channel_oid))
        messages = {}
        for user in self.clients:
            if user is not current_user:
                channels = getattr(user, 'following_channels', [])
                channels.append(request.root.channel)
                opened = self.opened_channels.get(user, {}).get('opened', [])
                hidden = self.opened_channels.get(user, {}).get('hidden', [])
                if channel in channels:
                    body = ''
                    channel_opened = channel_oid in hidden or channel_oid in opened
                    if channel_opened:
                        request.user = user
                        result_view = CommentsView(context, request)
                        result_view.ignore_unread = channel_oid in opened
                        result_view.comments = [comment]
                        body = result_view.update()['coordinates'][result_view.coordinates][0]['body']

                    events = [{
                        'event': 'edit_comment',
                        'params': {
                            'body': body,
                            'channel_hidden': channel_oid in hidden,
                            'channel_oid': str(channel_oid),
                            'comment_oid': str(comment_oid),
                            'user_oid': str(current_user.__oid__)
                        }
                    }]
                    messages[user] = events

        return messages

    def event_new_answer(
        self, client, context_oid,
        channel_oid, comment_oid,
        comment_parent_oid, **kwargs):
        request = kwargs.get('request')
        current_user = kwargs.get('current_user')
        context = get_obj(int(context_oid))
        comment = get_obj(int(comment_oid))
        channel = get_obj(int(channel_oid))
        messages = {}
        for user in self.clients:
            if user is not current_user:
                channels = getattr(user, 'following_channels', [])
                channels.append(request.root.channel)
                opened = self.opened_channels.get(user, {}).get('opened', [])
                hidden = self.opened_channels.get(user, {}).get('hidden', [])
                if channel in channels:
                    body = ''
                    channel_opened = channel_oid in hidden or channel_oid in opened
                    if channel_opened:
                        request.user = user
                        result_view = CommentsView(context, request)
                        result_view.ignore_unread = channel_oid in opened
                        result_view.comments = [comment]
                        body = result_view.update()['coordinates'][result_view.coordinates][0]['body']

                    events = [{
                        'event': 'new_answer',
                        'params': {
                            'body': body,
                            'channel_hidden': channel_oid in hidden,
                            'comment_parent_oid': str(comment_parent_oid),
                            'channel_oid': str(channel_oid),
                            'user_oid': str(current_user.__oid__)
                        }
                    }]
                    messages[user] = events

        return messages

    def event_remove_comment(
        self, client, channel_oid,
        comment_oid, **kwargs):
        request = kwargs.get('request')
        current_user = kwargs.get('current_user')
        channel = get_obj(int(channel_oid))
        messages = {}
        for user in self.clients:
            if user is not current_user:
                channels = getattr(user, 'following_channels', [])
                channels.append(request.root.channel)
                if channel in channels:
                    events = [{
                        'event': 'remove_comment',
                        'params': {
                            'channel_oid': str(channel_oid),
                            'comment_oid': str(comment_oid)
                        }
                    }]
                    messages[user] = events

        return messages

    def signal_new_connection(self, user, client):
        msg = json.dumps([{
            'event': 'connection',
            'params': {
                'id': str(user.__oid__)
            }
        }])
        self.broadcast(msg, [user])

    def signal_connected_users(self, user, client):
        events = []
        for connected_user in self.clients:
            events.append({
                'event': 'connection',
                'params': {
                    'id': str(connected_user.__oid__)
                }
            })

        msg = json.dumps(events)
        client.sendMessage(msg.encode('utf8'))

    def register(self, client, **kwargs):
        request = get_request(client)
        root = request.root
        user = get_user(request)
        if user and user not in self.clients:
            self.clients[user] = client
            self.signal_new_connection(user, client)
            self.signal_connected_users(user, client)
            root.connected_users = list(self.clients.keys())

    def signal_new_dicconnection(self, user, client, **kwargs):
        msg = json.dumps([{
            'event': 'disconnection',
            'params': {
                'id': str(user.__oid__)
            }
        }])
        self.broadcast(msg, [user])

    def unregister(self, client, **kwargs):
        request = get_request(client)
        root = request.root
        user = get_user(request)
        if user and user in self.clients:
            self.clients.pop(user)
            if user in self.opened_channels:
                self.opened_channels.pop(user)
                root.opened_channels = dict(self.opened_channels)

            self.signal_new_dicconnection(user, client)
            root.connected_users = list(self.clients.keys())

    def broadcast(self, msg, exclude=[]):
        for user in self.clients:
            if user not in exclude:
                client = self.clients[user]
                client.sendMessage(msg.encode('utf8'))


def run_ws(app):
    log.startLogging(sys.stdout)

    # create a Twisted Web resource for our WebSocket server
    ws_factory = NovaIdeoServerFactory(u"ws://127.0.0.1:8080")
    ws_factory.protocol = NovaIdeoServerProtocol
    ws_resource = WebSocketResource(ws_factory)
    # root.ws_factory = ws_factory

    # create a Twisted Web WSGI resource for our app server
    wsgi_resource = WSGIResource(reactor, reactor.getThreadPool(), app)

    # create a root resource serving everything via WSGI/Flask, but
    # the path "/ws" served by our WebSocket stuff
    rootResource = WSGIRootResource(wsgi_resource, {b'ws': ws_resource})

    factory = WebSocketClientFactory(u"ws://127.0.0.1:8080")
    factory.protocol = NovaIdeoClientProtocol
    connectWS(factory)

    # create a Twisted Web Site and run everything
    site = Site(rootResource)
    reactor.listenTCP(8080, site)
    reactor.run()
