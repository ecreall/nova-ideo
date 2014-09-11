from pyramid.view import view_config

from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.view_operation import CallSelectedContextsViews
from pontus.schema import select
from pontus.view import BasicView, View, merge_dicts, ViewError

from novaideo.content.processes.amendment_management.behaviors import  DuplicateAmendment
from novaideo.content.amendment import Amendment, AmendmentSchema
from novaideo import _


@view_config(
    name='duplicateamendment',
    context=Amendment,
    renderer='pontus:templates/view.pt',
    )
class DuplicateAmendmentView(FormView):
    title = _('Duplicate')
    name = 'duplicateamendment'
    schema = select(AmendmentSchema(),['title',
                                  'description',
                                  'keywords',
                                  'text'])

    behaviors = [DuplicateAmendment, Cancel]
    formid = 'formduplicateamendment'


    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update({DuplicateAmendment:DuplicateAmendmentView})
