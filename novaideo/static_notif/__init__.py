
import os

from pyramid.response import Response
from pyramid.view import view_config

# _here = /app/location/myapp

_here = os.path.dirname(__file__)

# _icon = /app/location/myapp/static/favicon.ico

# _robots = /app/location/myapp/static/robots.txt


_robots = open(os.path.join(
               _here, 'OneSignalSDKUpdaterWorker.js')).read()
_robots_response = Response(content_type='text/plain',
                            body=_robots)

_robots2 = open(os.path.join(
               _here, 'OneSignalSDKWorker.js')).read()
_robots2_response = Response(content_type='text/plain',
                            body=_robots2)

_manifest = open(os.path.join(
               _here, 'manifest.json')).read()
_manifest_response = Response(content_type='text/plain',
                            body=_manifest)

@view_config(name='manifest.json')
def favicon_view(context, request):
    return _manifest_response

@view_config(name='OneSignalSDKUpdaterWorker.js')
def robotstxt_view(context, request):
    return _robots_response

@view_config(name='OneSignalSDKWorker.js')
def robotstxt_view2(context, request):
    return _robots2_response