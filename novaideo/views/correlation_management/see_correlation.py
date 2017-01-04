# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view_operation import MultipleView
from pontus.view import BasicView

from novaideo.content.processes.correlation_management.behaviors import (
    SeeCorrelation)
from novaideo.content.correlation import Correlation
from novaideo import _
from .comment_correlation import CommentCorrelationView


class DetailCorrelation(BasicView):
    title = _('Details')
    name = 'seeCorrelation'
    behaviors = [SeeCorrelation]
    template = 'novaideo:views/correlation_management/templates/see_correlation.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    viewid = 'seecorrelation'

    def update(self):
        self.execute(None) 
        result = {}
        values = {
                'correlation': self.context,
               }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


@view_config(
    name='seecorrelation',
    context=Correlation,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeCorrelationView(MultipleView):
    title = _('Detail')
    name = 'seecorrelation'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (DetailCorrelation, CommentCorrelationView)
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/comment.js']}


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeCorrelation:SeeCorrelationView})
