# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.util import merge_dicts

from novaideo.content.processes.user_management.behaviors import (
    Discuss, GeneralDiscuss)
from novaideo.content.comment import CommentSchema, Comment
from novaideo.content.interface import IPerson
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.views.idea_management.comment_idea import CommentsView
from novaideo import _


class DiscussCommentsView(CommentsView):
    title = _('Messages')
    name = 'comments'
    validators = [Discuss.get_validator()]
    template = 'novaideo:views/idea_management/templates/comments.pt'
    wrapper_template = 'novaideo:views/idea_management/templates/comments_scroll.pt'
    viewid = 'comments'
    action_id = 'discuss'

    def _get_channel(self, user):
        return self.context.get_channel(user)


class DiscussFormView(FormView):

    title = _('Discuss the idea')
    schema = select(CommentSchema(factory=Comment,
                                  editable=True,
                                  omit=('associated_contents',)),
                    ['comment', 'intention', 'files', 'associated_contents'])
    behaviors = [Discuss]
    formid = 'formdiscuss'
    name = 'discussform'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Discuss.node_definition.id})
        formwidget = deform.widget.FormWidget(css_class='commentform deform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='discuss',
    context=IPerson,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DiscussView(MultipleView):
    title = _('Private discussion')
    description = _('Private discussion')
    name = 'discuss'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    css_class = 'comment-view-block'
    views = (DiscussCommentsView, DiscussFormView)
    contextual_help = 'comment-help'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/comment.js']}

    def _init_views(self, views, **kwargs):
        if kwargs.get('only_form', False):
            views = (DiscussFormView, )

        super(DiscussView, self)._init_views(views, **kwargs)

    def before_update(self):
        self.viewid = 'discuss'
        super(DiscussView, self).before_update()


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Discuss: DiscussView})


class GeneralCommentsView(DiscussCommentsView):
    validators = [GeneralDiscuss.get_validator()]
    action_id = 'discuss'

    def _get_channel(self, user):
        return self.context.channel


class GeneralDiscussFormView(DiscussFormView):

    behaviors = [GeneralDiscuss]

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': GeneralDiscuss.node_definition.id})
        formwidget = deform.widget.FormWidget(css_class='commentform deform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='discuss',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class GeneralDiscussView(DiscussView):
    title = _('General discussion')
    description = _('General discussion')
    views = (GeneralCommentsView, GeneralDiscussFormView)

    def _init_views(self, views, **kwargs):
        if kwargs.get('only_form', False):
            views = (GeneralDiscussFormView, )

        super(DiscussView, self)._init_views(views, **kwargs)


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {GeneralDiscuss: GeneralDiscussView})
