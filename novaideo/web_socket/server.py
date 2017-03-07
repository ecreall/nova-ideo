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


class BroadcastClientProtocol(WebSocketClientProtocol):

    """
    Simple client that connects to a WebSocket server, send a HELLO
    message every 2 seconds and print everything it receives.
    """

    def sendHello(self):
        self.sendMessage("Hello from Python!".encode('utf8'))

    def onOpen(self):
        self.sendHello()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            print("Text message received: {}".format(payload.decode('utf8')))


# Our WebSocket Server protocol


class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        transaction.begin()
        self.factory.register(self)

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


class BroadcastServerFactory(WebSocketServerFactory):

    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = {}
        # reactor.callLater(1, self.tick)

    def call_events_handlers(self, client, events):
        for event in events:
            event_id = event.get('event', None)
            if event_id is not None:
                operation = getattr(self, 'event_'+event_id, None)
                if operation is not None:
                    params = event.get('params', {})
                    operation(client, **params)

    def event_new_answer(self, client, context_oid, channel_oid, comment_oid):
        request = get_request(client)
        context = get_obj(int(context_oid))
        current_user = get_user(request)
        comment = get_obj(int(comment_oid))
        for user in self.clients:
            if user is not current_user:
                request.user = user
                result_view = CommentsView(context, request)
                result_view.ignore_unread = True
                result_view.comments = [comment]
                body = result_view.update()['coordinates'][result_view.coordinates][0]['body']
                events = [{
                    'event': 'new_answer',
                    'params': {
                        'body': body,
                        'channel_oid': str(channel_oid)
                    }
                }]
                msg = json.dumps(events)
                self.clients[user].sendMessage(msg.encode('utf8'))

    def event_new_comment(self, client, context_oid, channel_oid, comment_oid):
        request = get_request(client)
        context = get_obj(int(context_oid))
        current_user = get_user(request)
        channel = get_obj(int(channel_oid))
        comment = channel.comments[-1]
        for user in self.clients:
            if user is not current_user:
                request.user = user
                result_view = CommentsView(context, request)
                result_view.ignore_unread = True
                result_view.comments = [comment]
                body = result_view.update()['coordinates'][result_view.coordinates][0]['body']
                events = [{
                    'event': 'new_comment',
                    'params': {
                        'body': body,
                        'channel_oid': str(channel_oid)
                    }
                }]
                msg = json.dumps(events)
                self.clients[user].sendMessage(msg.encode('utf8'))

    def event_remove_comment(self, client, channel_oid, comment_oid):
        request = get_request(client)
        current_user = get_user(request)
        for user in self.clients:
            if user is not current_user:
                events = [{
                    'event': 'remove_comment',
                    'params': {
                        'channel_oid': str(channel_oid),
                        'comment_oid': str(comment_oid)

                    }
                }]
                msg = json.dumps(events)
                self.clients[user].sendMessage(msg.encode('utf8'))

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

    def register(self, client):
        user = get_user(get_request(client))
        if user and user not in self.clients:
            self.clients[user] = client
            self.signal_new_connection(user, client)
            self.signal_connected_users(user, client)

    def signal_new_dicconnection(self, user, client):
        msg = json.dumps([{
            'event': 'disconnection',
            'params': {
                'id': str(user.__oid__)
            }
        }])
        self.broadcast(msg, [user])

    def unregister(self, client):
        user = get_user(get_request(client))
        if user and user in self.clients:
            self.clients.pop(user)
            self.signal_new_dicconnection(user, client)

    def broadcast(self, msg, exclude=[]):
        for user in self.clients:
            if user not in exclude:
                client = self.clients[user]
                client.sendMessage(msg.encode('utf8'))


def run_ws(app):
    log.startLogging(sys.stdout)

    # create a Twisted Web resource for our WebSocket server
    wsFactory = BroadcastServerFactory(u"ws://127.0.0.1:8080")
    wsFactory.protocol = BroadcastServerProtocol
    wsResource = WebSocketResource(wsFactory)

    # create a Twisted Web WSGI resource for our app server
    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), app)

    # create a root resource serving everything via WSGI/Flask, but
    # the path "/ws" served by our WebSocket stuff
    rootResource = WSGIRootResource(wsgiResource, {b'ws': wsResource})

    factory = WebSocketClientFactory(u"ws://127.0.0.1:8080")
    factory.protocol = BroadcastClientProtocol
    connectWS(factory)

    # create a Twisted Web Site and run everything
    site = Site(rootResource)

    reactor.listenTCP(8080, site)
    reactor.run()
