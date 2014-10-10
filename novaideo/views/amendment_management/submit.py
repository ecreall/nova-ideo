import colander
import deform
from pyramid.view import view_config

from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.schema import Schema, select, omit
from pontus.view import BasicView, View, merge_dicts, ViewError
from pontus.default_behavior import Cancel
from pontus.widget import Select2Widget, SequenceWidget, SimpleMappingWidget, TextInputWidget

from novaideo.content.processes.amendment_management.behaviors import  SubmitAmendment
from novaideo.content.amendment import Amendment, Intention
from novaideo.views.widget import DragDropSelect2Widget, DragDropSequenceWidget, DragDropMappingWidget
from novaideo import _



def get_default_explanations_groups(context):
    explanations = dict(context.explanations)
    groups = []
    grouped_explanations = []
    for explanation in explanations.values():
        if not(explanation['oid'] in grouped_explanations):
            group = [e for e in explanations.values() if Intention.eq(explanation['intention'], e['intention'])]
            grouped_explanations.extend([e['oid'] for e in group])
            groups.append(group)
            if len(grouped_explanations) == len(explanations):
                break

    return groups


@colander.deferred
def explanations_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = [e['oid'] for e in context.explanations.values()]
    values = [(i, i) for i in values]
    return DragDropSelect2Widget(values=values)


class ExplanationGroupSchema(Schema):

    title = colander.SchemaNode(
        colander.String(),
        widget=TextInputWidget(css_class="title-select-item", placeholder="New amendment title")
        )

    explanations =  colander.SchemaNode(
        colander.Set(),
        widget=explanations_choice,
        title=_('Explanations'),
        )    


class ExplanationGroupsSchema(Schema):

    groups = colander.SchemaNode(
        colander.Sequence(),
        omit(ExplanationGroupSchema(name='Amendment', widget=DragDropMappingWidget()),['_csrf_token_']),
        widget=DragDropSequenceWidget(),
        title=_('Amendments')
        )


class SubmitAmendmentViewStudyReport(BasicView):
    title = _('Alert for publication')
    name='alertforpublication'
    template ='novaideo:views/amendment_management/templates/alert_amendment_submit.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class SubmitAmendmentView(FormView):
    title =  _('Submit')
    name ='submitamendmentform'
    formid = 'formsubmitamendment'
    schema = ExplanationGroupsSchema()
    behaviors = [SubmitAmendment, Cancel]
    validate_behaviors = False

    def default_data(self):
        groups = get_default_explanations_groups(self.context)
        data = {'groups': []}
        for group in groups:
            group_data = {'title':self.context.title + '('+'-'.join([str(i['oid']) for i in group ])+')',
                          'explanations': [str(e['oid']) for e in group]}
            data['groups'].append(group_data)

        return data


@view_config(
    name='submitamendment',
    context=Amendment,
    renderer='pontus:templates/view.pt',
    )
class SubmitAmendmentViewMultipleView(MultipleView):
    title = _('Submit')
    name = 'submitamendment'
    behaviors = [SubmitAmendment]
    viewid = 'submitamendment'
    template = 'pontus.dace_ui_extension:templates/mergedmultipleview.pt'
    views = (SubmitAmendmentViewStudyReport, SubmitAmendmentView)
    validators = [SubmitAmendment.get_validator()]
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/organize_amendments.js']}


DEFAULTMAPPING_ACTIONS_VIEWS.update({SubmitAmendment:SubmitAmendmentViewMultipleView})
