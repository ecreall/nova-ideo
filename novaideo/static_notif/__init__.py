
import os

from pyramid.response import Response
from pyramid.view import view_config

# _here = /app/location/myapp

_here = os.path.dirname(__file__)


_OneSignalSDKUpdaterWorker = open(os.path.join(
    _here, 'OneSignalSDKUpdaterWorker.js')).read()
_OneSignalSDKUpdaterWorker_response = Response(
    content_type='application/javascript',
    charset='utf8',
    body=_OneSignalSDKUpdaterWorker)

_OneSignalSDKWorker = open(os.path.join(
    _here, 'OneSignalSDKWorker.js')).read()
_OneSignalSDKWorker_response = Response(
    content_type='application/javascript',
    charset='utf8',
    body=_OneSignalSDKWorker)

_manifest = open(os.path.join(
    _here, 'manifest.json')).read()
_manifest_response = Response(
    content_type='application/json',
    charset='utf8',
    body=_manifest)


@view_config(name='manifest.json')
def favicon_view(context, request):
    return _manifest_response


@view_config(name='OneSignalSDKUpdaterWorker.js')
def OneSignalSDKUpdaterWorkerView(context, request):
    return _OneSignalSDKUpdaterWorker_response


@view_config(name='OneSignalSDKWorker.js')
def OneSignalSDKWorkerView(context, request):
    return _OneSignalSDKWorker_response
