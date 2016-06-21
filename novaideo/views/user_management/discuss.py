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

from novaideo.content.processes.user_management.behaviors import (
    Discuss, GeneralDiscuss)
from novaideo.content.comment import CommentSchema, Comment
from novaideo.content.interface import IPerson
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


COMMENT_LEVEL = 2

BATCH_DEFAULT_SIZE = 20


class DiscussCommentsView(BasicView):
    title = _('Messages')
    name = 'comments'
    validators = [Discuss.get_validator()]
    template = 'novaideo:views/idea_management/templates/comments.pt'
    wrapper_template = 'novaideo:views/idea_management/templates/comments_scroll.pt'
    viewid = 'comments'
    action_id = 'discuss'

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
        #TODO include all comments
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
        return self.context.get_channel(user)

    def update(self):
        current_user = get_current()
        result = {}
        url = self.request.resource_url(self.context, self.action_id)
        channel = self._get_channel(current_user)
        objects = []
        if channel:
            objects = sorted(getattr(self, 'comments', channel.comments),
                             key=lambda e: e.created_at, reverse=True)
        batch = Batch(objects,
                      self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#" + self.action_id + "_results"
        body, resources, messages, isactive = self._rendre_comments(
            batch, current_user, True, batch)
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = isactive
        result['coordinates'] = {self.coordinates: [item]}
        result.update(resources)
        result = merge_dicts(self.requirements_copy, result)
        return result


class DiscussFormView(FormView):

    title = _('Discuss the idea')
    schema = select(CommentSchema(factory=Comment,
                                  editable=True,
                                  omit=('related_contents',)),
                    ['comment', 'intention', 'files', 'related_contents'])
    behaviors = [Discuss]
    formid = 'formdiscuss'
    name = 'discussform'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi', query={'op': 'discuss_person'})
        formwidget = deform.widget.FormWidget(css_class='commentform deform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


COMMENT_MESSAGE = {'0': _(u"""Pas de fils de discussion"""),
                   '1': _(u"""Fil de discussion"""),
                   '*': _(u"""Fils de discussion""")}


@view_config(
    name='discuss',
    context=IPerson,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DiscussView(MultipleView):
    title = _('Private discuss')
    description = _('Private discuss')
    name = 'discuss'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    wrapper_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    views = (DiscussCommentsView, DiscussFormView)
    contextual_help = 'comment-help'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/comment.js']}

    def before_update(self):
        self.viewid = 'discuss'
        super(DiscussView, self).before_update()


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Discuss: DiscussView})


class GeneralCommentsView(DiscussCommentsView):
    validators = [GeneralDiscuss.get_validator()]
    action_id = 'general_discuss'

    def _get_channel(self, user):
        return self.context.channel


class GeneralDiscussFormView(DiscussFormView):

    behaviors = [GeneralDiscuss]

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi', query={'op': 'general_discuss'})
        formwidget = deform.widget.FormWidget(css_class='commentform deform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='discuss',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class GeneralDiscussView(DiscussView):
    title = _('General discuss')
    description = _('General discuss')
    views = (GeneralCommentsView, GeneralDiscussFormView)


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {GeneralDiscuss: GeneralDiscussView})
