import re
import colander
from pyramid.view import view_config

from dace.util import find_catalog
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite, allSubobjectsOfType
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView, ViewError, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI
from pontus.widget import CheckboxChoiceWidget, RichTextWidget, Select2Widget, SimpleMappingWidget
from pontus.schema import Schema, omit
from pontus.form import FormView
from pontus.view_operation import MultipleView

from novaideo.content.processes.amendment_management.behaviors import  ExplanationAmendment
from novaideo.content.amendment import Amendment, IntentionSchema, explanation_intentions
from novaideo import _
from novaideo.views.novaideo_view_manager.search import SearchResultView
from novaideo.ips.htmldiff import htmldiff
from .present_amendment import PresentAmendmentView
from .comment_amendment import CommentAmendmentView
from .associate import AssociateView


def modif_choice(context):
    root = getSite()
    explanations = [e['oid'] for e in context.explanations.values() if e['intention'] is not None]
    values = [(i, i) for i in explanations]
    values.insert(0, ('', '- Select -'))
    return Select2Widget(values=values)


class IntentionFormView(FormView):
    title = _('Intention')
    schema = IntentionSchema()
    formid = 'intentionamendmentform'
    name='intentionamendment'

    def default_data(self):
        itemid = getattr(self, 'itemid', None)
        if itemid is not None and itemid in self.context.explanations:
            intention = self.context.explanations[itemid]['intention']
            if intention is not None:
                return {'intention':{intention['id']: explanation_intentions[intention['id']].get_explanation_data(intention), 
                                    'intention':intention['id']}}

        return {}

def get_intention_form(context, request, descriminator=None):
    form = IntentionFormView(context, request)
    intentionid = None
    if descriminator is not None:
        form.formid = form.formid+str(descriminator)
        if descriminator in context.explanations and context.explanations[descriminator]['intention'] is not None:
            intentionid = context.explanations[descriminator]['intention']['id']
            form.itemid = descriminator
    
    for (id, intention) in explanation_intentions.items():
        schemawidget = None
        if intentionid is not None and intentionid==id:
            schemawidget = SimpleMappingWidget(item_css_class=id+"-intention form-intention")
        else:
            schemawidget = SimpleMappingWidget(item_css_class=id+"-intention form-intention hide-bloc")

        form.schema.get('intention').children.append(intention.schema(name=id, widget=schemawidget))

    form.schema.get('relatedexplanation').get('relatedexplanation').widget = modif_choice(context)
    hasintention = any((v['intention'] is not None and (descriminator is not None and v['oid'] is not int(descriminator)) for v in context.explanations.values()))
    if not hasintention:
        form.schema.children.remove(form.schema.get('relatedexplanation'))
    return form


@view_config(
    name='explanationamendment',
    context=Amendment,
    renderer='pontus:templates/view.pt',
    )
class ExplanationView(BasicView):
    title = _('Explanation')
    name = 'explanationamendment'
    behaviors = [ExplanationAmendment]
    template = 'novaideo:views/amendment_management/templates/explanations_amendment.pt'
    viewid = 'explanationamendment'
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/explanation_amendment.js']}

    def update(self):
        self.execute(None) 
        #proposal = self.context.proposal
        result = {}
        #textdiff = htmldiff.render_html_diff(getattr(proposal, 'text', ''), getattr(self.context, 'text', ''))
        
        values = {
                'amendment': self.context,
                'textdiff': self.context.textdiff,
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        intentionform = get_intention_form(self.context, self.request)
        intentionformresult = intentionform() 
        result['js_links'] = intentionformresult['js_links']
        result['css_links'] = intentionformresult['css_links']
        result = merge_dicts(self.requirements_copy, result)
        result['coordinates'] = {self.coordinates:[item]}
        return result


@view_config(name='explanationjson',
             context=Amendment,
             xhr=True,
             renderer='json')
class ExplanationView_Json(BasicView):

    def getform(self):
        result = {}
        itemid = self.params('itemid')
        item = self.context.explanations[itemid]
        #if item['intention'] is None:
        form = get_intention_form(self.context, self.request, itemid)
        result = {'body':form()['coordinates'][form.coordinates][0]['body']}

        return result

    def __call__(self):
        operation_name = self.params('op')
        if operation_name is not None:
            operation = getattr(self, operation_name, None)
            if operation is not None:
                return operation()

        return {}


DEFAULTMAPPING_ACTIONS_VIEWS.update({ExplanationAmendment:ExplanationView})

