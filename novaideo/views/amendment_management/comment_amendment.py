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

    title = _('Discuss the amendment')
    behaviors = [CommentAmendment]
    formid = 'formcommentamendment'
    name = 'commentamendmentform'

    def before_update(self):
        formwidget = deform.widget.FormWidget(css_class='commentform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        view_name = self.request.view_name
        if self.request.view_name == 'dace-ui-api-view':
            view_name = 'commentamendment'

        formwidget.ajax_url = self.request.resource_url(self.context,
                                                 '@@'+view_name)
        self.schema.widget = formwidget


@view_config(
    name='commentamendment',
    context=Amendment,
    renderer='pontus:templates/view.pt',
    )
class CommentAmendmentView(CommentIdeaView):
    title = _('Discuss the amendment')
    description = _('Discuss the amendment')
    name = 'commentidea'
    views = (CommentAmendmentFormView, CommentsView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({CommentAmendment:CommentAmendmentView})
