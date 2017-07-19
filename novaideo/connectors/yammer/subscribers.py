# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from persistent.dict import PersistentDict

from pyramid.events import subscriber
from pyramid.threadlocal import get_current_request
import yampy

from novaideo.event import ObjectPublished


@subscriber(ObjectPublished)
def mysubscriber_object_published(event):
    content = event.object
    author = getattr(content, 'author', None)
    keywords = content.keywords
    request = get_current_request()
    root = request.root
    yammer_connectors = list(root.get_connectors('yammer'))
    yammer_connector = yammer_connectors[0] if yammer_connectors else None
    if yammer_connector and yammer_connector.enable_notifications:
        only_from_default = getattr(
            yammer_connector, 'only_from_default', False)
        default_access_token = getattr(yammer_connector, 'access_token', '')
        access_token = None
        if only_from_default and default_access_token:
            access_token = default_access_token
        else:
            access_token = getattr(
                author, 'source_data', {}).get(
                'access_token', default_access_token)

        if access_token:
            yammer = yampy.Yammer(access_token=access_token)
            # Post a new messages
            msg = '{title} \n\n {text} \n\n {url}'.format(
                title=content.title,
                text=content.text[:150]+'...',
                url=request.resource_url(content, '@@index'))
            message_data = yammer.messages.create(
                msg,
                topics=keywords)
            if isinstance(message_data, dict) and \
               message_data.get('messages', []):
                content.source_data = PersistentDict({
                    'app_name': 'yammer',
                    'id': str(message_data['messages'][0]['id'])
                })
                content.reindex()
            # msg = {
            #     "actor":{
            #         "name":author.title,
            #         "email":getattr(author, 'email', '')
            #         },
            #     "action":"create",
            #     "object": {
            #         "url":request.resource_url(content, '@@index'),
            #         "title":content.title
            #         },
            #     "type": "url"
            #     }
            # yammer.client.post('/activity', activity=msg)
