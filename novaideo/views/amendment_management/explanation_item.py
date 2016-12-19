# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.amendment_management.behaviors import (
    ExplanationItem)
from novaideo.content.amendment import Amendment, Intention
from novaideo import _


@view_config(
    name='explanationitem',
    context=Amendment,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ExplanationItemView(BasicView):
    title = _('Justification of the item')
    name = 'explanationitem'
    behaviors = [ExplanationItem]
    viewid = 'explanationitem'

    def update(self):
        item = self.params('item')
        intentionid = self.params('intention')
        relatedexplanation = self.params('relatedexplanation')
        intention = None
        if relatedexplanation is not None and relatedexplanation != '':
            intention = dict(self.context.explanations[relatedexplanation]['intention'])
        elif intentionid != '':
            intention = Intention.get_intention(self)

        self.execute({'item':item, 'intention':intention})
        result = {}
        body = ''
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result
        
DEFAULTMAPPING_ACTIONS_VIEWS.update({ExplanationItem:ExplanationItemView})
