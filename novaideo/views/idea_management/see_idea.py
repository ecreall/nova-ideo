import re
import colander
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.util import find_catalog
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite, allSubobjectsOfType
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView, ViewError, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI
from pontus.widget import CheckboxChoiceWidget, RichTextWidget
from pontus.schema import Schema
from pontus.form import FormView
from pontus.view_operation import MultipleView

from novaideo.content.processes.idea_management.behaviors import  SeeIdea
from novaideo.content.idea import Idea
from novaideo import _
from novaideo.views.novaideo_view_manager.search import SearchResultView
from .present_idea import PresentIdeaView
from .duplicate_idea import DuplicateIdeaView
from .comment_idea import CommentIdeaView
from .associate import AssociateView
from .compare_idea import CompareIdeaView



class DetailIdeaView(BasicView):
    title = _('Details')
    name = 'seeIdea'
    behaviors = [SeeIdea]
    template = 'novaideo:views/idea_management/templates/see_idea.pt'
    item_template = 'pontus:templates/subview_sample.pt'
    viewid = 'seeidea'


    def update(self):
        self.execute(None) 
        user = get_current()
        files = getattr(self.context, 'attached_files', [])
        files_urls = []
        for f in files:
            files_urls.append({'title':f.title, 'url':f.url(self.request)})

        actions = [a for a in self.context.actions if getattr(a.action, 'style', '') == 'button']
        global_actions = [a for a in actions if getattr(a.action, 'style_descriminator','') == 'global-action']
        text_actions = [a for a in  actions if getattr(a.action, 'style_descriminator','') == 'text-action']
        global_actions = sorted(global_actions, key=lambda e: getattr(e.action, 'style_order',0))
        text_actions = sorted(text_actions, key=lambda e: getattr(e.action, 'style_order',0))

        result = {}
        values = {
                'idea': self.context,
                'current_user': user,
                'files': files_urls,
                'global_actions': global_actions,
                'text_actions': text_actions,
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class SeeIdeaActionsView(MultipleView):
    title = _('actions')
    name = 'seeiactionsdea'
    template = 'novaideo:views/idea_management/templates/panel_group.pt'
    views = (AssociateView, PresentIdeaView, CommentIdeaView, CompareIdeaView)

    def _activate(self, items):
        pass


@view_config(
    name='seeidea',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class SeeIdeaView(MultipleView):
    title = _('')
    name = 'seeidea'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    views = (DetailIdeaView, SeeIdeaActionsView)
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/compare_idea.js',
                                'novaideo:static/js/comment.js']}


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeIdea:SeeIdeaView})

