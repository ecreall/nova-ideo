# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from persistent.dict import PersistentDict
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.schema import Schema, omit
from pontus.view import BasicView
from pontus.default_behavior import Cancel
from pontus.widget import TextInputWidget

from novaideo.content.processes.amendment_management.behaviors import (
    SubmitAmendment)
from novaideo.content.amendment import Amendment, Intention
from novaideo.views.widget import (
    DragDropSelect2Widget, 
    DragDropSequenceWidget, 
    DragDropMappingWidget)
from novaideo import _
from novaideo.utilities.text_analyzer import ITextAnalyzer
from novaideo.utilities.amendment_viewer import IAmendmentViewer



def get_default_explanations_groups(context):
    explanations = dict(context.explanations)
    groups = []
    grouped_explanations = []
    for explanation in explanations.values():
        if not(explanation['oid'] in grouped_explanations):
            group = [e for e in explanations.values() \
                     if Intention.eq(explanation['intention'], e['intention'])]
            grouped_explanations.extend([e['oid'] for e in group])
            groups.append(group)
            if len(grouped_explanations) == len(explanations):
                break

    return groups


@colander.deferred
def explanations_choice(node, kw):
    context = node.bindings['context']
    values = [(i['oid'], i['oid']) for i in context.explanations.values()]
    return DragDropSelect2Widget(values=values, multiple=True)


class ExplanationGroupSchema(Schema):

    title = colander.SchemaNode(
        colander.String(),
        missing="",
        widget=TextInputWidget(css_class="title-select-item", readonly=True)
        )

    explanations =  colander.SchemaNode(
        colander.Set(),
        widget=explanations_choice,
        missing=[],
        default=[],
        title=_('Explanations'),
        )    


@colander.deferred
def groups_widget(node, kw):
    context = node.bindings['context']
    return DragDropSequenceWidget(item_css_class="explanation-groups", 
                                  item_title_template=context.title+'-', 
                                  max_len=len(context.explanations))


class ExplanationGroupsSchema(Schema):

    groups = colander.SchemaNode(
        colander.Sequence(),
        omit(ExplanationGroupSchema(name='Amendment', 
                                    widget=DragDropMappingWidget()),
             ['_csrf_token_']),
        widget=groups_widget,
        title=_('Organize your changes in amendments')
        )

    single_amendment = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(css_class="single-amendment-control"),
        label=_('Gather changes in a single amendment'),
        title ='',
        missing=False
        )


class SubmitAmendmentViewStudyReport(BasicView):
    title = _('Alert for publication')
    name = 'alertforpublication'
    template = 'novaideo:views/amendment_management/templates/alert_amendment_submit.pt'
    readonly_explanation_template = 'novaideo:views/amendment_management/templates/readonly/submit_explanation_item.pt'

    def update(self):
        result = {}
        text_analyzer = get_current_registry().getUtility(
                                                  ITextAnalyzer,
                                                  'text_analyzer')
        amendment_viewer = get_current_registry().getUtility(
                                                   IAmendmentViewer,
                                                   'amendment_viewer')
        souptextdiff, explanations = amendment_viewer.get_explanation_diff(
                                                    self.context, self.request)
        self.context.explanations = PersistentDict(explanations)
        amendment_viewer.add_details(self.context,
                                     self.request,
                                     souptextdiff,
                                     self.readonly_explanation_template)
        explanationtext = text_analyzer.soup_to_text(souptextdiff)
        not_published_ideas = [i for i in self.context.get_used_ideas() \
                               if not('published' in i.state)]
        values = {'context': self.context,
                  'explanationtext': explanationtext,
                  'ideas': not_published_ideas}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class SubmitAmendmentView(FormView):
    title =  _('Submit')
    name = 'submitamendmentform'
    formid = 'formsubmitamendment'
    schema = ExplanationGroupsSchema()
    behaviors = [SubmitAmendment, Cancel]
    validate_behaviors = False

    def default_data(self):
        groups = get_default_explanations_groups(self.context)
        data = {'groups': []}
        i = 1
        for group in groups:
            group_data = {'title':self.context.title +'-'+str(i),
                          'explanations': [str(e['oid']) for e in group]}
            data['groups'].append(group_data)
            i += 1

        return data


@view_config(
    name='submitamendment',
    context=Amendment,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SubmitAmendmentViewMultipleView(MultipleView):
    title = _('Amendments organization')
    name = 'submitamendment'
    viewid = 'submitamendment'
    template = 'pontus.dace_ui_extension:templates/mergedmultipleview.pt'
    views = (SubmitAmendmentViewStudyReport, SubmitAmendmentView)
    behaviors = [SubmitAmendment]
    validators = [SubmitAmendment.get_validator()]
    requirements = {'css_links':['novaideo:static/css/organize_amendments.css'],
                    'js_links':['novaideo:static/js/organize_amendments.js']}


DEFAULTMAPPING_ACTIONS_VIEWS.update({SubmitAmendment:SubmitAmendmentViewMultipleView})
