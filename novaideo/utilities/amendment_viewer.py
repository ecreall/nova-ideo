# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from dace.util import utility
from zope.interface import Interface, implementer
from persistent.dict import PersistentDict
from pyramid.threadlocal import get_current_registry
from pyramid import renderers
from substanced.util import get_oid
from bs4 import BeautifulSoup

from daceui.interfaces import IDaceUIAPI

from novaideo.content.amendment import Intention
from novaideo.utilities.text_analyzer import ITextAnalyzer


class IAmendmentViewer(Interface):
    """Interface for AmendmentViewer
    """

    def get_explanation_diff(context, request):
        pass

    def add_actions(action, context, request, soup):
        pass

    def add_details(context, request, soup):
        pass


@utility(name='amendment_viewer')
@implementer(IAmendmentViewer)
class AmendmentViewer(object):
    """AmendmentViewer utility
    """

    explanation_template = 'novaideo:views/amendment_management/templates/explanation_item.pt'
    modal_template = 'novaideo:views/amendment_management/templates/explanation_modal_item.pt'
    readonly_explanation_template = 'novaideo:views/amendment_management/templates/readonly/explanation_item.pt'
    #readonly_modal_template = 'novaideo:views/amendment_management/templates/readonly/explanation_modal_item.pt'
    readonly_inline_template = 'novaideo:views/amendment_management/templates/readonly/explanation_inline_item.pt'

    def _add_modal(self, action, soup, tag, context, request):
        context_oid = get_oid(context)
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,
        	                                            'dace_ui_api')
        if not hasattr(action, 'explanationitemaction'):
            explanationitemnode = action.process['explanationitem']
            explanationitem_wis = [wi for wi in explanationitemnode.workitems \
                                   if wi.node is explanationitemnode]
            if explanationitem_wis:
                action.explanationitemaction = explanationitem_wis[0].actions[0]

        if hasattr(action, 'explanationitemaction'):
            values = {'url':request.resource_url(context, '@@explanationjson', 
                                             query={'op':'getform',
                                                    'itemid':tag['data-item']}),
                     'item': context.explanations[tag['data-item']],
                     }
            body = renderers.render(self.explanation_template, values, request)
            explanation_item_soup = BeautifulSoup(body)

            actionurl_update = dace_ui_api.updateaction_viewurl(request=request,
                                action_uid=str(get_oid(
                                	            action.explanationitemaction)),
                                context_uid=str(context_oid))
            values = {'url': actionurl_update,
                     'item': context.explanations[tag['data-item']],
                    }
            modal_body = renderers.render(self.modal_template, values, request)
            explanation_item_modal_soup = BeautifulSoup(modal_body)
            soup.body.append(explanation_item_modal_soup.body)
            tag.append(explanation_item_soup.body)
            tag.body.unwrap()

    def _add_modal_details(self, soup, tag, context, request, explanation_template=None):
        data = {}
        try:
            data = Intention.get_explanation_data(
            	     context.explanations[tag['data-item']]['intention'])
        except Exception:
            pass

        values = {'item': context.explanations[tag['data-item']],
                 'data': data}
        if explanation_template is None:
            explanation_template = self.readonly_explanation_template

        body = renderers.render(explanation_template,
                                values,
                                request)
        explanation_item_soup = BeautifulSoup(body)
        #readonly_modal_template,
        modal_body = renderers.render(self.readonly_inline_template,
                                      values, 
                                      request)
        explanation_item_modal_soup = BeautifulSoup(modal_body)
        soup.body.append(explanation_item_modal_soup.body)
        tag.append(explanation_item_soup.body)
        tag.body.unwrap()

    def _identify_explanations(self, context, request, soup, descriminator):
        explanation_tags = soup.find_all('span', {'id': "explanation"})
        context_oid = str(get_oid(context))
        old_explanations = dict(context.explanations)
        explanations = {}
        for explanation_tag in explanation_tags:
            explanation_tag['data-context'] = context_oid
            explanation_tag['data-item'] = str(descriminator)
            init_vote = {'oid':descriminator, 'intention':None}
            descriminator_str = str(descriminator)
            if not(descriminator_str in old_explanations): 
                explanations[descriminator_str] = PersistentDict(init_vote)
            else :
                explanations[descriminator_str] = old_explanations[descriminator_str]

            descriminator += 1
        
        context.explanations = explanations
        return explanations

    def get_explanation_diff(self, context, request):
        proposal = context.proposal
        text_analyzer = get_current_registry().getUtility(ITextAnalyzer,
        	                                              'text_analyzer')
        souptextdiff, textdiff = text_analyzer.render_html_diff(
        	                        getattr(proposal, 'text', ''),
                                    getattr(context, 'text', ''),
                                    "explanation")
        descriminator = 1
        explanations = self._identify_explanations(context, request,
                                    souptextdiff, descriminator)
        return souptextdiff, explanations

    def add_actions(self, action, context, request, soup):
        explanations_tags = soup.find_all('span', {'id':'explanation'})
        for explanation_tag in explanations_tags:
            self._add_modal(action, soup, explanation_tag, context, request)

    def add_details(self, context, request, soup, explanation_template=None):
        explanations_tags = soup.find_all('span', {'id':'explanation'})
        for explanation_tag in explanations_tags:
            self._add_modal_details(soup, explanation_tag, context,
                                    request, explanation_template)