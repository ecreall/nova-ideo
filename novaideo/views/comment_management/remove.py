# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view import BasicView
from pontus.view_operation import MultipleView
from pontus.default_behavior import Cancel

from novaideo.content.processes.comment_management.behaviors import Remove
from novaideo.content.comment import Comment
from novaideo import _


class RemoveViewStudyReport(BasicView):
    title = _('Alert for deletion')
    name = 'alertfordeletion'
    template = 'novaideo:views/comment_management/templates/alert_remove.pt'

    def update(self):
        result = {}
        values = {'comment': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class RemoveForm(FormView):
    title = _('Remove comment')
    name = 'removecommentform'
    behaviors = [Remove, Cancel]
    viewid = 'removecommentform'
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi', query={'op': 'remove_comment'})
        formwidget = deform.widget.FormWidget(css_class='comment-remove-form deform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='removecomment',
    context=Comment,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class RemoveView(MultipleView):
    title = _('Comment deletion')
    name = 'removecomment'
    behaviors = [Remove]
    viewid = 'removecomment'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    views = (RemoveViewStudyReport, RemoveForm)
    validators = [Remove.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Remove: RemoveView})
