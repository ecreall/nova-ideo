import datetime
import deform
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView
from pontus.view import BasicView, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI

from novaideo.content.processes.correlation_management.behaviors import  CommentCorrelation
from novaideo.content.comment import CommentSchema, Comment
from novaideo.content.correlation import Correlation
from novaideo import _
from ..idea_management.comment_idea import CommentsView



class CommentsCorrelationView(CommentsView):
    validators = []
    viewid = 'commentscorrelation'


class CommentCorrelationFormView(FormView):

    title = _('Comment form')
    schema = select(CommentSchema(factory=Comment, editable=True),['intention', 'comment'])
    behaviors = [CommentCorrelation]
    formid = 'formcommentcorrelation'
    name='commentcorrelationform'

    def before_update(self):
        formwidget = deform.widget.FormWidget(css_class='commentform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget
        view_name = self.request.view_name
        if self.request.view_name == 'dace-ui-api-view':
            view_name = 'commentcorrelation'

        formwidget.ajax_url = self.request.resource_url(self.context, '@@'+view_name)


@view_config(
    name='commentcorrelation',
    context=Correlation,
    renderer='pontus:templates/view.pt',
    )
class CommentCorrelationView(MultipleView):
    title = _('Comment')
    name='commentcorrelation'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    #item_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    views = (CommentCorrelationFormView, CommentsCorrelationView)
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/comment.js']}


DEFAULTMAPPING_ACTIONS_VIEWS.update({CommentCorrelation: CommentCorrelationView})
