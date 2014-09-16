import datetime
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView
from pontus.view import BasicView, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI

from novaideo.content.processes.correlation_management.behaviors import  SeeCorrelation
from novaideo.content.comment import CommentSchema, Comment
from novaideo.content.correlation import Correlation
from novaideo import _
from ..idea_management.comment_idea import CommentsView
from .comment_correlation import CommentCorrelationView


class DetailCorrelation(BasicView):
    title = _('Details')
    name = 'seeCorrelation'
    behaviors = [SeeCorrelation]
    template = 'novaideo:views/correlation_management/templates/see_correlation.pt'
    item_template = 'pontus:templates/subview_sample.pt'
    viewid = 'seecorrelation'

    def update(self):
        self.execute(None) 
        result = {}
        values = {
                'correlation': self.context,
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


@view_config(
    name='seecorrelation',
    context=Correlation,
    renderer='pontus:templates/view.pt',
    )
class SeeCorrelationView(MultipleView):
    title = _('Detail')
    name='seecorrelation'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    views = (DetailCorrelation, CommentCorrelationView)
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/comment.js']}


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeCorrelation:SeeCorrelationView})
