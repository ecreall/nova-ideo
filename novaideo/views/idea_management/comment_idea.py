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
from novaideo.views.filter import get_comments
from novaideo.content.idea import Idea
from novaideo.utilities.util import date_delta
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
    action_id = 'comment'

    def _datetimedelta(self, date):
        return date_delta(date)

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

    def _get_channel(self, user):
        return self.context.channel

    def update(self):
        current_user = get_current()
        result = {}
        channel = self._get_channel(current_user)
        is_selected = hasattr(self, 'comments')
        text_to_search = self.params('text')
        if not is_selected:
            filters = self.params('filters')
            filters = filters if filters else []
            if not isinstance(filters, (list, tuple)):
                filters = [filters]

            objects = get_comments(
                channel, filters, text_to_search)
        else:
            objects = sorted(
                getattr(self, 'comments', []),
                key=lambda e: e.created_at, reverse=True)

        url = self.request.resource_url(self.context, self.action_id)
        batch = Batch(objects,
                      self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#" + self.action_id + "_results"
        batch.origin_url = url
        body, resources, messages, isactive = self._rendre_comments(
            batch, current_user, True, batch)
        # if text_to_search:
        #     texts = [t for t in text_to_search.split(' ') if t]
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
    views = (CommentsView, CommentIdeaFormView)
    contextual_help = 'comment-help'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/comment.js']}

    def before_update(self):
        self.viewid = 'comment'
        super(CommentIdeaView, self).before_update()


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CommentIdea: CommentIdeaView})
