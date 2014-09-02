import re
import colander
import htmldiff
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

from novaideo.content.processes.amendment_management.behaviors import  SeeAmendment
from novaideo.content.amendment import Amendment
from novaideo import _
from novaideo.views.novaideo_view_manager.search import SearchResultView
from .present_amendment import PresentAmendmentView
from .comment_amendment import CommentAmendmentView
from .associate import AssociateView



class DetailAmendmentView(BasicView):
    title = _('Details')
    name = 'seeAmendment'
    behaviors = [SeeAmendment]
    template = 'novaideo:views/amendment_management/templates/see_amendment.pt'
    item_template = 'pontus:templates/subview_sample.pt'
    viewid = 'seeamendment'


    def update(self):
        self.execute(None) 
        user = get_current()
        actions = [a for a in self.context.actions if getattr(a.action, 'style', '') == 'button']
        actions_urls = []
        for action in actions:
            actions_urls.append({'title':action.title, 'url':action.url})

        result = {}
        textdiff = ''
        descriptiondiff = ''
        keywordsdiff = []
        proposal = self.context.proposal
        textdiff = htmldiff.render_html_diff(getattr(proposal, 'text', ''), getattr(self.context, 'text', ''))
        descriptiondiff = htmldiff.render_html_diff('<div>'+getattr(proposal, 'description', '')+'</div>', '<div>'+getattr(self.context, 'description', '')+'</div>')
        for k in proposal.keywords:
            if k in self.context.keywords:
                keywordsdiff.append({'title':k,'state':'nothing'})
            else:
                keywordsdiff.append({'title':k,'state':'del'})
                  
        [keywordsdiff.append({'title':k,'state':'ins'}) for k in self.context.keywords if k not in proposal.keywords]
        values = {
                'amendment': self.context,
                'textdiff': textdiff,
                'descriptiondiff':descriptiondiff,
                'keywordsdiff':keywordsdiff,
                'current_user': user,
                'actions': actions_urls
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class SeeAmendmentActionsView(MultipleView):
    title = _('actions')
    name = 'seeiactionsamendment'
    template = 'novaideo:views/idea_management/templates/panel_group.pt'
    views = (AssociateView, PresentAmendmentView, CommentAmendmentView)


@view_config(
    name='seeamendment',
    context=Amendment,
    renderer='pontus:templates/view.pt',
    )
class SeeAmendmentView(MultipleView):
    title = _('Details')
    name = 'seeamendment'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    views = (DetailAmendmentView, SeeAmendmentActionsView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeAmendment:SeeAmendmentView})

