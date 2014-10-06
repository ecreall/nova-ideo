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
from pontus.default_behavior import Cancel
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


def modif_choice(context, itemid=None):
    root = getSite()
    explanations = [e['oid'] for e in context.explanations.values() if e['intention'] is not None and str(e['oid'])!=itemid]
    values = [(i, i) for i in sorted(explanations)]
    values.insert(0, ('', '- Select -'))
    return Select2Widget(values=values, item_css_class="related-explanation")


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
                return {'intention':{intention['id']: explanation_intentions[intention['id']].get_explanation_default_data(intention), 
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

    form.schema.get('relatedexplanation').get('relatedexplanation').widget = modif_choice(context, descriminator)
    hasintention = any((v['intention'] is not None and (descriminator is not None and v['oid'] is not int(descriminator)) for v in context.explanations.values()))
    if not hasintention:
        form.schema.children.remove(form.schema.get('relatedexplanation'))
    return form


class ExplanationViewStudyReport(BasicView):
    title = _('Alert for explanation')
    name='alertforexplanation'
    template ='novaideo:views/amendment_management/templates/explanations_amendment.pt'

    def update(self):
        result = {}
        values = {}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class ExplanationFormView(FormView):
    title = _('Explanation')
    name = 'formexplanationamendment'
    behaviors = [ExplanationAmendment, Cancel]
    viewid = 'formexplanationamendment'
    formid = 'explanationamendmentform'


@view_config(
    name='explanationamendment',
    context=Amendment,
    renderer='pontus:templates/view.pt',
    )
class ExplanationView(MultipleView):
    title = _('Explanation')
    name = 'explanationamendment'
    behaviors = [ExplanationAmendment]
    viewid = 'explanationamendment'
    template = 'pontus.dace_ui_extension:templates/mergedmultipleview.pt'
    views = (ExplanationViewStudyReport, ExplanationFormView)
    validators = [ExplanationAmendment.get_validator()]


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

