import re
import colander
import datetime
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from substanced.util import Batch

from dace.util import find_catalog
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite, allSubobjectsOfType
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView, ViewError, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI
from pontus.widget import CheckboxChoiceWidget, RichTextWidget
from pontus.schema import Schema
from pontus.form import FormView

from novaideo.content.processes.novaideo_view_manager.behaviors import  SeeMySelections
from novaideo.content.novaideo_application import NovaIdeoApplicationSchema, NovaIdeoApplication
from novaideo import _
from novaideo.content.interface import Iidea, IProposal, IPerson
from novaideo.core import BATCH_DEFAULT_SIZE


@view_config(
    name='seemyselections',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class SeeMySelectionsView(BasicView):
    title = _('My selections')
    name = 'seemyselections'
    behaviors = [SeeMySelections]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seemyselections'



    def update(self):
        self.execute(None) 
        user = get_current()
        objects = [o for o in getattr(user, 'selections', []) if not('archived' in o.state)]
        objects = sorted(objects, key=lambda e: getattr(e, 'modified_at', datetime.datetime.today()), reverse=True)
        batch = Batch(objects, self.request, default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_selections"
        len_result = batch.seqlen
        result_body = []
        for o in batch:
            object_values = {'object':o, 'current_user':user}
            body = self.content(result=object_values, template=o.result_template)['body']
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


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeMySelections:SeeMySelectionsView})

