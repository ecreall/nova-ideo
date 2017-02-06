# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.comment_management.behaviors import Edit
from novaideo.content.comment import CommentSchema, Comment
from novaideo import _


@view_config(
    name='edit',
    context=Comment,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditView(FormView):

    title = _('Edit')
    schema = select(CommentSchema(factory=Comment,
                                  editable=True,
                                  omit=('associated_contents',)),
                    ['comment', 'intention', 'files', 'associated_contents'])
    behaviors = [Edit]
    formid = 'formedit'
    name = 'edit'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/comment.js']}

    def default_data(self):
        return self.context

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Edit.node_definition.id})
        formwidget = deform.widget.FormWidget(css_class='commentform comment-inline-form edit-comment-form deform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


DEFAULTMAPPING_ACTIONS_VIEWS.update({Edit: EditView})
