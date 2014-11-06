import unittest

from pyramid import testing
from pyramid_robot.layer import Layer
from webtest import http
from substanced.db import root_factory


class BaseFunctionalTests(object):

    def setUp(self):
        import tempfile
        import os.path
        self.tmpdir = tempfile.mkdtemp()
        dbpath = os.path.join( self.tmpdir, 'test.db')
        uri = 'file://' + dbpath
        settings = {'zodbconn.uri': uri,
                    'substanced.secret': 'sosecret',
                    'substanced.initial_login': 'admin',
                    'substanced.initial_password': 'admin',
                    'novaideo.secret' : 'seekri1',
                    'novaideo.admin_email': 'admin@example.com',
                    'pyramid.includes': [
                        'substanced',
                        'pyramid_chameleon',
                        'pyramid_layout',
                        'pyramid_mailer.testing', # have to be after substanced to override the mailer
                        'pyramid_tm',
                        'dace',
                        'pontus',
        ]}

        testing.setUp()
        from novaideo import main
        self.app = app = main({}, **settings)
        self.db = app.registry._zodb_databases['']
        self.request = request = testing.DummyRequest()
        self.config = testing.setUp(registry=app.registry, request=request)
        self.registry = self.config.registry
        self.root = root_factory(request)
        request.root = self.root


    def tearDown(self):
        from dace.processinstance import event
        with event.callbacks_lock:
            for dc_or_stream in event.callbacks.values():
                if hasattr(dc_or_stream, 'close'):
                    dc_or_stream.close()
                else:
                    dc_or_stream.stop()

            event.callbacks = {}

        from dace.objectofcollaboration.system import CRAWLERS
        for crawler in CRAWLERS:
            crawler.stop()

        import shutil
        testing.tearDown()
        self.db.close()
        shutil.rmtree(self.tmpdir)


class FunctionalTests(BaseFunctionalTests, unittest.TestCase):

    def setUp(self):
        super(FunctionalTests, self).setUp()


class RobotLayer(BaseFunctionalTests, Layer):

    defaultBases = ()

    def setUp(self):
        super(RobotLayer, self).setUp()
        self.server = http.StopableWSGIServer.create(self.app, port=8080)

    def tearDown(self):
        super(RobotLayer, self).tearDown()
        self.server.shutdown()


ROBOT_LAYER = RobotLayer()
