
import datetime
from pyramid.view import view_config

from substanced.util import Batch

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView

from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeMySupports)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.content.processes import get_states_mapping
from novaideo.core import BATCH_DEFAULT_SIZE


@view_config(
    name='seemysupports',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class SeeMySupportsView(BasicView):
    title = _('My supports')
    name = 'seemysupports'
    behaviors = [SeeMySupports]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seemysupports'

    def update(self):
        self.execute(None) 
        user = get_current()
        objects = [o for o in getattr(user, 'supports', []) \
                   if not('archived' in o.state)]
        objects = sorted(objects, 
                         key=lambda e: getattr(e, 'modified_at', 
                                               datetime.datetime.today()), 
                         reverse=True)
        batch = Batch(objects, self.request, default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_supports"
        len_result = batch.seqlen
        result_body = []
        for obj in batch:
            object_values = {'object': obj, 
                           'current_user': user, 
                           'state': get_states_mapping(user, obj, 
                                   getattr(obj, 'state', [None])[0])}
            body = self.content(result=object_values, 
                                template=obj.result_template)['body']
            result_body.append(body)

        result = {}
        values = {
                'bodies': result_body,
                'length': len_result,
                'batch': batch,
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeMySupports:SeeMySupportsView})

