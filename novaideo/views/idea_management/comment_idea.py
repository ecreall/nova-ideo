import datetime
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView
from pontus.view import BasicView, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI

from novaideo.content.processes.idea_management.behaviors import  CommentIdea
from novaideo.content.comment import CommentSchema, Comment
from novaideo.content.idea import Idea
from novaideo import _



class CommentsView(BasicView):
    title = _('Comments')
    name = 'comments'
    validators = [CommentIdea.get_validator()]
    template = 'novaideo:views/idea_management/templates/comments.pt'
    item_template = 'novaideo:views/idea_management/templates/comments_scroll.pt'
    viewid = 'comments'

    def _datetimedelta(self, date):
        now = datetime.datetime.now()
        delta = now - date 
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        result = {}
        if delta.days>0:
            result['days'] = delta.days

        if hours>0:
            result['hours'] = hours

        if minutes>0:
            result['minutes'] = minutes

        if seconds>0:
            result['seconds'] = seconds

        return result

    def _rendre_comments(self, comments, origin=False):
        all_messages = {}
        isactive = False
        all_resources = {}
        all_resources['js_links'] = []
        all_resources['css_links'] = []
        all_comments = []
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,'dace_ui_api')
        for comment in comments:
            comment_data = {'comment':comment}
            action_updated, messages, resources, actions = dace_ui_api._actions(self.request, comment, 'commentmanagement', 'respond')
            if action_updated and not isactive:
                isactive = True

            all_messages.update(messages)
            if resources is not None:
                if 'js_links' in resources:
                    all_resources['js_links'].extend(resources['js_links'])
                    all_resources['js_links'] = list(set(all_resources['js_links']))

                if 'css_links' in resources:
                    all_resources['css_links'].extend(resources['css_links'])
                    all_resources['css_links'] =list(set(all_resources['css_links']))

            if actions: 
                comment_data['commentaction'] = actions[0]

            all_comments.append(comment_data) 

        values = {
                'comments': all_comments,
                'view': self,
                'origin':origin
               }
        body = self.content(result=values, template=self.template)['body']
        return body, all_resources, all_messages, isactive

    def update(self):
        result = {}
        body, resources, messages, isactive =  self._rendre_comments(self.context.comments, True)
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = isactive
        result['coordinates'] = {self.coordinates:[item]}
        result.update(resources)
        result  = merge_dicts(self.requirements_copy, result)
        return result


class CommentIdeaFormView(FormView):

    title = _('Comment')
    schema = select(CommentSchema(factory=Comment, editable=True),['intention', 'comment'])
    behaviors = [CommentIdea]
    formid = 'formcommentidea'
    name='commentideaform'


@view_config(
    name='commentidea',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class CommentIdeaView(MultipleView):
    title = _('Comment')
    name='commentidea'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    views = (CommentIdeaFormView, CommentsView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({CommentIdea:CommentIdeaView})
