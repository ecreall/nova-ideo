# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
import deform
from pyramid.view import view_config
from pyramid import renderers

from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view import BasicView
from pontus.view_operation import MultipleView
from pontus.default_behavior import Cancel

from novaideo.content.processes.comment_management.behaviors import Unpin
from novaideo.content.comment import Comment
from novaideo import _


class UnpinViewStudyReport(BasicView):
    title = _('Alert for deletion')
    name = 'alertfordeletion'
    template = 'novaideo:views/comment_management/templates/alert_unpin.pt'

    def update(self):
        result = {}
        user = get_current()
        values = {'object': self.context,
                  'current_user': user}
        comment_body = renderers.render(
            self.context.templates.get('default'),
            values,
            self.request)
        values = {'comment_body': comment_body}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class UnpinForm(FormView):
    title = _('Unpin comment')
    name = 'unpincommentform'
    behaviors = [Unpin, Cancel]
    viewid = 'unpincommentform'
    validate_behaviors = False

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Unpin.node_definition.id})
        formwidget = deform.widget.FormWidget(css_class='comment-un-pin-form deform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='unpincomment',
    context=Comment,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class UnpinView(MultipleView):
    title = _('Unpin comment')
    name = 'unpincomment'
    behaviors = [Unpin]
    viewid = 'unpincomment'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (UnpinViewStudyReport, UnpinForm)
    validators = [Unpin.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Unpin: UnpinView})
