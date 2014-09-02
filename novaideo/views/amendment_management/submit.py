from pyramid.view import view_config

from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.schema import select
from pontus.view import BasicView, View, merge_dicts, ViewError
from pontus.default_behavior import Cancel

from novaideo.content.processes.amendment_management.behaviors import  SubmitAmendment
from novaideo.content.amendment import Amendment
from novaideo import _



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
    behaviors = [SubmitAmendment, Cancel]
    validate_behaviors = False


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


DEFAULTMAPPING_ACTIONS_VIEWS.update({SubmitAmendment:SubmitAmendmentViewMultipleView})
