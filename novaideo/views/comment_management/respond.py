# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.comment_management.behaviors import  Respond
from novaideo.content.comment import CommentSchema, Comment
from novaideo import _


@view_config(
    name='respond',
    context=Comment,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class RespondView(FormView):

    title = _('Answer')
    schema = select(CommentSchema(factory=Comment,
                                  editable=True,
                                  omit=('associated_contents',)),
                    ['comment', 'intention', 'files', 'associated_contents'])
    behaviors = [Respond]
    formid = 'formrespond'
    name = 'respond'
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/comment.js']}

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Respond.node_definition.id})
        formwidget = deform.widget.FormWidget(css_class='commentform comment-inline-form respondform deform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


DEFAULTMAPPING_ACTIONS_VIEWS.update({Respond: RespondView})
