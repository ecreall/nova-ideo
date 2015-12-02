# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
import deform
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.util import merge_dicts
from daceui.interfaces import IDaceUIAPI

from novaideo.content.processes.idea_management.behaviors import  CommentIdea
from novaideo.content.comment import CommentSchema, Comment
from novaideo.content.idea import Idea
from novaideo import _


COMMENT_LEVEL = 2


class CommentsView(BasicView):
    title = _('Messages')
    name = 'comments'
    validators = [CommentIdea.get_validator()]
    template = 'novaideo:views/idea_management/templates/comments.pt'
    wrapper_template = 'novaideo:views/idea_management/templates/comments_scroll.pt'
    viewid = 'comments'

    def _datetimedelta(self, date):
        now = datetime.datetime.now(tz=pytz.UTC)
        delta = now - date
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        result = {}
        if delta.days > 0:
            result['days'] = delta.days

        if hours > 0:
            result['hours'] = hours

        if minutes > 0:
            result['minutes'] = minutes

        if seconds > 0:
            result['seconds'] = seconds

        return result

    def _rendre_comments(self, comments, origin=False):
        all_comments = []
        dace_ui_api = get_current_registry().getUtility(
                                               IDaceUIAPI,'dace_ui_api')
        comments_actions = dace_ui_api.get_actions(comments, self.request,
                                                'commentmanagement', 'respond')
        action_updated, messages, \
        resources, actions = dace_ui_api.update_actions(self.request,
                                                        comments_actions)
        actions = dict([(a['context'], a) for a in actions])
        all_comments = sorted(list(actions.values()), 
                              key=lambda e: e['context'].created_at)
        values = {
                'comments': all_comments,
                'view': self,
                'origin':origin,
                'level': COMMENT_LEVEL
               }
        body = self.content(args=values, template=self.template)['body']
        return body, resources, messages, action_updated

    def update(self):
        result = {}
        body, resources, messages, isactive =  self._rendre_comments(
                                          self.context.comments, True)
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = isactive
        result['coordinates'] = {self.coordinates:[item]}
        result.update(resources)
        result  = merge_dicts(self.requirements_copy, result)
        return result


class CommentIdeaFormView(FormView):

    title = _('Discuss the idea')
    schema = select(CommentSchema(factory=Comment, 
                                  editable=True, 
                                  omit=('related_contents',)),
                    ['intention', 'comment', 'related_contents'])
    behaviors = [CommentIdea]
    formid = 'formcommentidea'
    name = 'commentideaform'

    def before_update(self):
        formwidget = deform.widget.FormWidget(css_class='commentform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        view_name = self.request.view_name
        if self.request.view_name == 'dace-ui-api-view':
            view_name = 'commentidea'

        formwidget.ajax_url = self.request.resource_url(self.context, 
                                                        '@@'+view_name)
        self.schema.widget = formwidget


COMMENT_MESSAGE = {'0': _(u"""Pas de fils de discussion"""),
                      '1': _(u"""Fil de discussion"""),
                      '*': _(u"""Fils de discussion""")} 

@view_config(
    name='commentidea',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CommentIdeaView(MultipleView):
    title = _('Discuss the idea')
    description = _('Discuss the idea')
    name = 'commentidea'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    wrapper_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    views = (CommentIdeaFormView, CommentsView)
    contextual_help = 'comment-help'

    def get_message(self):
        lencomments = len(self.context.comments)
        index = str(lencomments)
        if lencomments > 1:
            index = '*'

        message = (_(COMMENT_MESSAGE[index]),
                   lencomments,
                   index)
        return message


DEFAULTMAPPING_ACTIONS_VIEWS.update({CommentIdea:CommentIdeaView})
