# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView
from pontus.widget import Select2Widget
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.view_operation import MultipleView

from novaideo.content.processes.amendment_management.behaviors import (
    ExplanationAmendment)
from novaideo.content.amendment import Amendment, IntentionSchema, Intention
from novaideo import _


def modif_choice(context, itemid=None):
    explanations = [e['oid'] for e in context.explanations.values() \
                    if e['intention'] is not None and str(e['oid'])!=itemid]
    values = [(i, i) for i in sorted(explanations)]
    values.insert(0, ('', _('- Select -')))
    return Select2Widget(values=values, item_css_class="related-explanation")


class IntentionFormView(FormView):
    title = _('Intention')
    schema = IntentionSchema()
    formid = 'intentionamendmentform'
    name = 'intentionamendment'

    def before_update(self):
        descriminator = getattr(self, 'descriminator', 0)
        self.formid = self.formid+str(descriminator)
        relatedexplanation_node = self.schema.get('relatedexplanation').get('relatedexplanation')
        relatedexplanation_node.widget = modif_choice(self.context, 
                                                       descriminator)
        hasintention = any((v['intention'] is not None \
                            and (descriminator is not None \
                            and v['oid'] is not int(descriminator)) \
                            for v in self.context.explanations.values()))
        if not hasintention:
            self.schema.children.remove(self.schema.get('relatedexplanation'))

    def default_data(self):
        itemid = getattr(self, 'descriminator', None)
        if itemid is not None and itemid in self.context.explanations:
            intention = self.context.explanations[itemid]['intention']
            if intention is not None:
                return {'intention': Intention.get_explanation_default_data(intention)}

        return {}


class ExplanationViewStudyReport(BasicView):
    title = _('Alert for justification')
    name = 'alertforexplanation'
    template ='novaideo:views/amendment_management/templates/explanations_amendment.pt'

    def update(self):
        result = {}
        values = {}
        body = self.content(args=values, template=self.template)['body']
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
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ExplanationView(MultipleView):
    title = _('Explain my improvement')
    name = 'explanationamendment'
    behaviors = [ExplanationAmendment]
    viewid = 'explanationamendment'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
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
        form = IntentionFormView(self.context, self.request)
        form.descriminator = itemid
        result = {'body': form()['coordinates'][form.coordinates][0]['body']}
        return result

    def __call__(self):
        operation_name = self.params('op')
        if operation_name is not None:
            operation = getattr(self, operation_name, None)
            if operation is not None:
                return operation()

        return {}


DEFAULTMAPPING_ACTIONS_VIEWS.update({ExplanationAmendment:ExplanationView})