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

from .util import get_request
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
            params = json.loads(payload.decode('utf8'))
            self.factory.call_events_handlers(self, **params)
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

    def call_events_handlers(self, client, **kwargs):
        request = get_request(client, **kwargs)
        messages = {}
        events = kwargs.get('events', [])
        for event in events:
            event_id = event.get('event', None)
            if event_id is not None:
                operation = getattr(self, 'event_'+event_id, None)
                if operation is not None:
                    params = event.get('params', {})
                    params['request'] = request
                    params['current_user'] = getattr(request.user, '__oid__', '')
                    try:
                        _messages = operation(client, **params)
                        for user, _events in _messages.items():
                            messages.setdefault(user, [])
                            messages[user].extend(_events)
                    except Exception:
                        pass

        for user, events in messages.items():
            msg = json.dumps(events)
            self.clients[user]['client'].sendMessage(msg.encode('utf8'))

    def event_channel_opened(
        self, client, channel_oid, **kwargs):
        current_user = kwargs.get('current_user')
        self.clients[current_user]['channels']['opened'].append(channel_oid)
        if channel_oid in self.clients[current_user]['channels']['hidden']:
            self.clients[current_user]['channels']['hidden'].remove(channel_oid)

    def event_all_channels_closed(
        self, client, **kwargs):
        current_user = kwargs.get('current_user')
        if current_user in self.clients:
            self.clients[current_user]['channels']['opened'] = []
            self.clients[current_user]['channels']['hidden'] = []

    def event_channel_hidden(
        self, client, channel_oid, **kwargs):
        current_user = kwargs.get('current_user')
        if current_user in self.clients and \
           channel_oid in self.clients[current_user]['channels']['opened']:
            self.clients[current_user]['channels']['opened'].remove(channel_oid)
            self.clients[current_user]['channels']['hidden'].append(channel_oid)

    def event_typing_comment(
        self, client, channel_oid, **kwargs):
        request = kwargs.get('request')
        current_user = request.user
        current_user_oid = kwargs.get('current_user')
        channel = get_obj(int(channel_oid))
        messages = {}
        for user in self.clients:
            if user != current_user_oid:
                user_obj = get_obj(user)
                channels = getattr(user_obj, 'following_channels', [])
                channels.append(request.root.channel)
                opened = self.clients[user]['channels']['opened']
                hidden = self.clients[user]['channels']['hidden']
                if channel in channels or \
                   (channel_oid in hidden or channel_oid in opened):
                    events = [{
                        'event': 'typing_comment',
                        'params': {
                            'channel_oid': str(channel_oid),
                            'user_oid': str(current_user_oid),
                            'user_name': current_user.first_name
                        }
                    }]
                    messages[user] = events

        return messages

    def event_stop_typing_comment(
        self, client, channel_oid, **kwargs):
        request = kwargs.get('request')
        current_user_oid = kwargs.get('current_user')
        channel = get_obj(int(channel_oid))
        messages = {}
        for user in self.clients:
            if user != current_user_oid:
                user_obj = get_obj(user)
                channels = getattr(user_obj, 'following_channels', [])
                channels.append(request.root.channel)
                opened = self.clients[user]['channels']['opened']
                hidden = self.clients[user]['channels']['hidden']
                if channel in channels or \
                   (channel_oid in hidden or channel_oid in opened):
                    events = [{
                        'event': 'stop_typing_comment',
                        'params': {
                            'channel_oid': str(channel_oid),
                            'user_oid': str(current_user_oid)
                        }
                    }]
                    messages[user] = events

        return messages

    def event_new_comment(
        self, client, context_oid,
        channel_oid, **kwargs):
        request = kwargs.get('request')
        current_user_oid = kwargs.get('current_user')
        context = get_obj(int(context_oid))
        channel = get_obj(int(channel_oid))
        comment = channel.comments[-1]
        messages = {}
        for user in self.clients:
            if user != current_user_oid:
                user_obj = get_obj(user)
                channels = getattr(user_obj, 'following_channels', [])
                channels.append(request.root.channel)
                opened = self.clients[user]['channels']['opened']
                hidden = self.clients[user]['channels']['hidden']
                channel_opened = channel_oid in hidden or channel_oid in opened
                if channel in channels or channel_opened:
                    body = ''
                    if channel_opened:
                        request.user = user_obj
                        result_view = CommentsView(context, request)
                        result_view.ignore_unread = channel_oid in opened
                        result_view.comments = [comment]
                        body = result_view.update()['coordinates'][result_view.coordinates][0]['body']

                    events = [{
                        'event': 'new_comment',
                        'params': {
                            'body': body,
                            'channel_hidden': channel_oid in hidden,
                            'user_oid': str(current_user_oid),
                            'channel_oid': str(channel_oid)
                        }
                    }]
                    messages[user] = events

        return messages

    def event_edit_comment(
        self, client, context_oid,
        channel_oid, comment_oid, **kwargs):
        request = kwargs.get('request')
        current_user_oid = kwargs.get('current_user')
        context = get_obj(int(context_oid))
        comment = get_obj(int(comment_oid))
        channel = get_obj(int(channel_oid))
        messages = {}
        for user in self.clients:
            if user != current_user_oid:
                user_obj = get_obj(user)
                channels = getattr(user_obj, 'following_channels', [])
                channels.append(request.root.channel)
                opened = self.clients[user]['channels']['opened']
                hidden = self.clients[user]['channels']['hidden']
                channel_opened = channel_oid in hidden or channel_oid in opened
                if channel in channels or channel_opened:
                    body = ''
                    if channel_opened:
                        request.user = user_obj
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
                            'user_oid': str(current_user_oid)
                        }
                    }]
                    messages[user] = events

        return messages

    def event_new_answer(
        self, client, context_oid,
        channel_oid, comment_oid,
        comment_parent_oid, **kwargs):
        request = kwargs.get('request')
        current_user_oid = kwargs.get('current_user')
        context = get_obj(int(context_oid))
        comment = get_obj(int(comment_oid))
        channel = get_obj(int(channel_oid))
        messages = {}
        for user in self.clients:
            if user != current_user_oid:
                user_obj = get_obj(user)
                channels = getattr(user_obj, 'following_channels', [])
                channels.append(request.root.channel)
                opened = self.clients[user]['channels']['opened']
                hidden = self.clients[user]['channels']['hidden']
                channel_opened = channel_oid in hidden or channel_oid in opened
                if channel in channels or channel_opened:
                    body = ''
                    if channel_opened:
                        request.user = user_obj
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
                            'user_oid': str(current_user_oid)
                        }
                    }]
                    messages[user] = events

        return messages

    def event_remove_comment(
        self, client, channel_oid,
        comment_oid, **kwargs):
        request = kwargs.get('request')
        current_user_oid = kwargs.get('current_user')
        channel = get_obj(int(channel_oid))
        messages = {}
        for user in self.clients:
            if user != current_user_oid:
                user_obj = get_obj(user)
                channels = getattr(user_obj, 'following_channels', [])
                channels.append(request.root.channel)
                opened = self.clients[user]['channels']['opened']
                hidden = self.clients[user]['channels']['hidden']
                channel_opened = channel_oid in hidden or channel_oid in opened
                if channel in channels or channel_opened:
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
                'id': str(user)
            }
        }])
        self.send_message(msg, exclude=[user])

    def signal_connected_users(self, user, client):
        events = []
        for connected_user in self.clients:
            events.append({
                'event': 'connection',
                'params': {
                    'id': str(connected_user)
                }
            })

        msg = json.dumps(events)
        client.sendMessage(msg.encode('utf8'))

    def register(self, client, **kwargs):
        request = get_request(client)
        user = getattr(request.user, '__oid__', '')
        if user and user not in self.clients:
            view_name = request.view_name.replace('@', '')
            context_oid = getattr(request.context, '__oid__', '')
            self.clients[user] = {
                'client': client,
                'context': context_oid,
                'view_name': view_name,
                'user_context': str(context_oid)+view_name,
                'channels': {
                    'opened': [],
                    'hidden': []
                }
            }
            self.signal_new_connection(user, client)
            self.signal_connected_users(user, client)

    def signal_new_dicconnection(self, user, client, **kwargs):
        msg = json.dumps([{
            'event': 'disconnection',
            'params': {
                'id': str(user)
            }
        }])
        self.send_message(msg, exclude=[user])

    def unregister(self, client, **kwargs):
        request = get_request(client)
        user = getattr(request.user, '__oid__', '')
        if user and user in self.clients:
            self.clients.pop(user)
            self.signal_new_dicconnection(user, client)

    def filter_users(self, users=None, filter_={}):
        """
            filter = {
               'channels': [channel, ...],
               'contexts': [(context, view_name), ...]
            }
        """
        if users is None:
            users = list(self.clients.keys())
        else:
            users = [getattr(u, '__oid__', u) for u in users]
            users = [u for u in users in u in self.clients]

        filter_.setdefault('channels', None)
        filter_.setdefault('contexts', None)
        condition = filter_.get('condition', None)
        if filter_['channels'] is None and filter_['contexts'] is None:
            return users

        if filter_['channels'] is not None:
            filter_['channels'] = [str(getattr(c, '__oid__', c)) for c in filter_['channels']]

        if filter_['contexts'] is not None:
            filter_['contexts'] = [str(getattr(c, '__oid__', c))+v.replace('@', '')
                                   for c, v in filter_['contexts']]

        return filter(lambda u: (filter_['contexts'] is None or self.clients[u]['user_context'] in filter_['contexts']) and
                     (filter_['channels'] is None or any(ch in self.clients[u]['channels']['opened'] or
                      ch in self.clients[u]['channels']['hidden']
                      for ch in filter_['channels'])) and
                     (condition is None or condition(get_obj(int(u)))), users)

    def send_message(self, msg, users=None, exclude=[], filter_={}):
        users = self.filter_users(users, filter_)
        exclude = [getattr(e, '__oid__', e) for e in exclude]
        for user in users:
            if user in self.clients and user not in exclude:
                self.clients[user]['client'].sendMessage(msg.encode('utf8'))


def run_ws(app):
    log.startLogging(sys.stdout)

    # create a Twisted Web resource for our WebSocket server
    ws_factory = NovaIdeoServerFactory(u"ws://127.0.0.1:8080")
    ws_factory.protocol = NovaIdeoServerProtocol
    ws_resource = WebSocketResource(ws_factory)

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
    reactor.ws_factory = ws_factory
    reactor.run()
