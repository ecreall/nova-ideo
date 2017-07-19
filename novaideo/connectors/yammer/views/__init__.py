# Copyright (c) 2017 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
import yampy

from dace.objectofcollaboration.principal.util import (
    get_current)
from dace.objectofcollaboration.object import Object
from dace.util import find_catalog
from pontus.view import BasicView

from novaideo.content.interface import Iidea
from novaideo import log


def find_yammer_content(interfaces):
    novaideo_catalog = find_catalog('novaideo')
    dace_catalog = find_catalog('dace')
    identifier_index = novaideo_catalog['identifier']
    object_provides_index = dace_catalog['object_provides']
    query = object_provides_index.any([i.__identifier__ for i in interfaces]) &\
        identifier_index.any(['yammer'])
    return query.execute().all()


@view_config(name='yammerapi',
             context=Object,
             xhr=True,
             renderer='json')
class YammerAPI(BasicView):

    def __call__(self):
        operation_name = self.params('op')
        if operation_name is not None:
            operation = getattr(self, operation_name, None)
            if operation is not None:
                return operation()

        return {}

    def find_yammer_messages(self):
        root = self.request.root
        yammer_connectors = list(root.get_connectors('yammer'))
        yammer_connector = yammer_connectors[0] if yammer_connectors else None
        access_token = getattr(
            get_current(), 'source_data', {}).get(
            'access_token', None)
        if yammer_connector and access_token:
            page = self.params('page')
            limit = self.params('limit')
            try:
                yammer = yampy.Yammer(access_token=access_token)
                messages = yammer.client.get(
                    '/messages', older_than=page, threaded=True, limit=limit)
                if messages['messages']:
                    current_ideas = [i.source_data['id']
                                     for i in find_yammer_content([Iidea])]
                    entries = [{'id': e['id'],
                                'text': e['body']['plain'][:150]+'...',
                                'imported': str(e['id']) in current_ideas}
                               for e in messages['messages']]
                    return {
                        'items': entries,
                        'total_count': len(messages['messages']),
                        'has_next': messages['meta']['older_available'],
                        'next_page': messages['messages'][-1]['id']}
            except Exception as error:
                log.warning(error)

        return {'items': [], 'total_count': 0}
