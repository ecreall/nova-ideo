# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS

from novaideo.content.processes.amendment_management.behaviors import (
    CommentAmendment)
from novaideo.views.idea_management.comment_idea import (
    CommentIdeaView,
    CommentIdeaFormView,
    CommentsView as CommentsIdeaView)
from novaideo.content.amendment import Amendment
from novaideo import _


class CommentsView(CommentsIdeaView):
    validators = [CommentAmendment.get_validator()]


class CommentAmendmentFormView(CommentIdeaFormView):

    title = _('Discuss the amended version')
    behaviors = [CommentAmendment]
    formid = 'formcommentamendment'
    name = 'commentamendmentform'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': CommentAmendment.node_definition.id})
        formwidget = deform.widget.FormWidget(css_class='commentform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='comment',
    context=Amendment,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CommentAmendmentView(CommentIdeaView):
    title = _('Discuss the amended version')
    description = _('Discuss the amended version')
    name = 'comment'
    views = (CommentsView, CommentAmendmentFormView)

    def _init_views(self, views, **kwargs):
        if kwargs.get('only_form', False):
            views = (CommentAmendmentFormView, )

        super(CommentIdeaView, self)._init_views(views, **kwargs)


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CommentAmendment: CommentAmendmentView})
