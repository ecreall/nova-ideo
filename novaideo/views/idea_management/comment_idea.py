# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
import deform
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from substanced.util import Batch

from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.util import merge_dicts
from daceui.interfaces import IDaceUIAPI

from novaideo.content.processes.idea_management.behaviors import CommentIdea
from novaideo.content.comment import CommentSchema, Comment
from novaideo.content.idea import Idea
from novaideo import _


COMMENT_LEVEL = 2

BATCH_DEFAULT_SIZE = 20


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

    def _rendre_comments(self, comments, current_user, origin=False, batch=None):
        all_comments = []
        dace_ui_api = get_current_registry().getUtility(
            IDaceUIAPI, 'dace_ui_api')
        comments_actions = dace_ui_api.get_actions(
            comments, self.request,
            'commentmanagement', 'respond')
        action_updated, messages, \
            resources, actions = dace_ui_api.update_actions(
                self.request, comments_actions)
        actions = dict([(a['context'], a) for a in actions])
        all_comments = sorted(list(actions.values()),
                              key=lambda e: e['context'].created_at)
        values = {
            'comments': all_comments,
            'current_user': current_user,
            'view': self,
            'origin': origin,
            'batch': batch,
            'level': COMMENT_LEVEL
        }
        body = self.content(args=values, template=self.template)['body']
        return body, resources, messages, action_updated

    def update(self):
        current_user = get_current()
        result = {}
        url = self.request.resource_url(self.context, 'comment')
        objects = sorted(getattr(self, 'comments', self.context.comments),
                         key=lambda e: e.created_at, reverse=True)
        batch = Batch(objects,
                      self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#comments_results"
        body, resources, messages, isactive = self._rendre_comments(
            batch, current_user, True, batch)
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = isactive
        result['coordinates'] = {self.coordinates: [item]}
        result.update(resources)
        result = merge_dicts(self.requirements_copy, result)
        return result


class CommentIdeaFormView(FormView):

    title = _('Discuss the idea')
    schema = select(CommentSchema(factory=Comment,
                                  editable=True,
                                  omit=('related_contents',)),
                    ['comment', 'intention', 'files', 'related_contents'])
    behaviors = [CommentIdea]
    formid = 'formcommentidea'
    name = 'commentideaform'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi', query={'op': 'comment_entity'})
        formwidget = deform.widget.FormWidget(css_class='commentform deform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


COMMENT_MESSAGE = {'0': _(u"""Pas de fils de discussion"""),
                   '1': _(u"""Fil de discussion"""),
                   '*': _(u"""Fils de discussion""")}


@view_config(
    name='comment',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CommentIdeaView(MultipleView):
    title = _('Discuss the idea')
    description = _('Discuss the idea')
    name = 'comment'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    wrapper_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    views = (CommentsView, CommentIdeaFormView)
    contextual_help = 'comment-help'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/comment.js']}

    def get_message(self):
        lencomments = len(self.context.comments)
        index = str(lencomments)
        if lencomments > 1:
            index = '*'

        message = (_(COMMENT_MESSAGE[index]),
                   lencomments,
                   index)
        return message

    def before_update(self):
        self.viewid = 'comment'
        super(CommentIdeaView, self).before_update()


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CommentIdea: CommentIdeaView})
