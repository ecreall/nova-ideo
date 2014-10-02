import deform
from pyramid.view import view_config

from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.amendment_management.behaviors import  ExplanationItem
from novaideo.content.amendment import Amendment
from novaideo import _


@view_config(
    name='explanationitem',
    context=Amendment,
    renderer='pontus:templates/view.pt',
    )
class ExplanationItemView(BasicView):
    title = _('Explanation item')
    name = 'explanationitem'
    template = 'novaideo:views/proposal_management/templates/correction_text.pt'
    behaviors = [ExplanationItem]
    viewid = 'explanationitem'


    def update(self):
        item = self.params('item')
        import pdb; pdb.set_trace()
        #self.execute({'item':item})
        result = {}
        values = {
                'text': 'mon text'#self.context.get_adapted_text(get_current()),
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result
        

DEFAULTMAPPING_ACTIONS_VIEWS.update({ExplanationItem:ExplanationItemView})
