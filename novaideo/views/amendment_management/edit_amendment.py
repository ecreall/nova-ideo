from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView

from novaideo.content.processes.amendment_management.behaviors import  EditAmendment
from novaideo.content.amendment import AmendmentSchema, Amendment
from novaideo import _


@view_config(
    name='editamendment',
    context=Amendment,
    renderer='pontus:templates/view.pt',
    )
class EditAmendmentView(FormView):

    title = _('Edit amendment')
    schema = select(AmendmentSchema(),['intention',
                                  'title',
                                  'description',
                                  'keywords',
                                  'text'])
    behaviors = [EditAmendment, Cancel]
    formid = 'formeditamendment'
    item_template = 'pontus:templates/subview_sample.pt'
    name='editamendment'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update({EditAmendment:EditAmendmentView})
