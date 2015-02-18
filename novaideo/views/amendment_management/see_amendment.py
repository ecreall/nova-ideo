# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current, has_role
from pontus.view import BasicView
from pontus.util import merge_dicts
from pontus.view_operation import MultipleView

from novaideo.content.processes.amendment_management.behaviors import (
    SeeAmendment)
from novaideo.content.amendment import Amendment
from novaideo.content.processes import get_states_mapping
from novaideo.utilities.util import get_actions_navbar, navbar_body_getter
from novaideo import _
from .present_amendment import PresentAmendmentView
from .comment_amendment import CommentAmendmentView
from .explanation_amendment import IntentionFormView
from novaideo.utilities.text_analyzer import ITextAnalyzer


class DetailAmendmentView(BasicView):
    title = _('Details')
    name = 'seeAmendment'
    behaviors = [SeeAmendment]
    template = 'novaideo:views/amendment_management/templates/see_amendment.pt'
    wrapper_template = 'daceui:templates/simple_view_wrapper.pt'
    viewid = 'seeamendment'
    validate_behaviors = False

    def _add_requirements(self, user):
        is_owner = has_role(user=user, role=('Owner', self.context))
        if is_owner and ('explanation' in self.context.state):
            self.requirements = {'js_links': [], 'css_links': [],}
            intentionform = IntentionFormView(self.context, self.request)
            intentionformresult = intentionform()
            self.requirements['js_links'] = intentionformresult['js_links']
            self.requirements['css_links'] = intentionformresult['css_links']
            self.requirements['js_links'].append('novaideo:static/js/explanation_amendment.js')

    def update(self):
        self.execute(None)
        user = get_current()
        self._add_requirements(user)
        text_analyzer = get_current_registry().getUtility(
                                               ITextAnalyzer,
                                               'text_analyzer')
        def actions_getter():
            return [a for a in self.context.actions \
                   if getattr(a.action, 'style', '') == 'button']

        actions_navbar = get_actions_navbar(actions_getter, self.request,
                                ['global-action', 'text-action'])
        isactive = actions_navbar['modal-action']['isactive']
        messages = actions_navbar['modal-action']['messages']
        resources = actions_navbar['modal-action']['resources']
        result = {}
        textdiff = ''
        descriptiondiff = ''
        keywordsdiff = []
        proposal = self.context.proposal
        textdiff = self.context.text_diff
        soup, descriptiondiff = text_analyzer.render_html_diff(
                   '<div>'+getattr(proposal, 'description', '')+'</div>',
                   '<div>'+getattr(self.context, 'description', '')+'</div>')
        for k in proposal.keywords:
            if k in self.context.keywords:
                keywordsdiff.append({'title': k, 'state': 'nothing'})
            else:
                keywordsdiff.append({'title': k, 'state': 'del'})
                  
        [keywordsdiff.append({'title': k, 'state': 'ins'}) \
         for k in self.context.keywords if k not in proposal.keywords]
        values = {
                'amendment': self.context,
                'state': get_states_mapping(
                              user, self.context, self.context.state[0]),
                'textdiff': textdiff,
                'descriptiondiff':descriptiondiff,
                'keywordsdiff':keywordsdiff,
                'current_user': user,
                'navbar_body': navbar_body_getter(self, actions_navbar)
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = messages
        item['isactive'] = isactive
        result.update(resources)
        result['coordinates'] = {self.coordinates:[item]}
        result = merge_dicts(self.requirements_copy, result)
        return result


class SeeAmendmentActionsView(MultipleView):
    title = _('actions')
    name = 'seeiactionsamendment'
    template = 'novaideo:views/idea_management/templates/panel_group.pt'
    views = (PresentAmendmentView, CommentAmendmentView)

    def _activate(self, items):
        pass


@view_config(
    name='seeamendment',
    context=Amendment,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeAmendmentView(MultipleView):
    title = ''
    name = 'seeamendment'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    views = (DetailAmendmentView, SeeAmendmentActionsView)
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/comment.js', 
                                'novaideo:static/js/explanation_amendment.js']}
    validators = [SeeAmendment.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeAmendment:SeeAmendmentView})

