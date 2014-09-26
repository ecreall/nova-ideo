from pyramid.view import view_config

from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.view_operation import CallSelectedContextsViews
from pontus.schema import select
from pontus.view import BasicView, View, merge_dicts, ViewError
from pontus.view_operation import MultipleView

from novaideo.content.processes.amendment_management.behaviors import  DuplicateAmendment
from novaideo.content.amendment import Amendment, AmendmentSchema
from novaideo import _
from novaideo.views.proposal_management.edit_proposal import IdeaManagementView
from novaideo.views.proposal_management.create_proposal import ideas_choice


class DuplicateAmendmentFormView(FormView):
    title = _('Duplicate')
    name = 'duplicateamendment'
    schema = select(AmendmentSchema(), ['title',
                     'description',
                     'keywords',
                     'text',
                     'related_ideas'])

    behaviors = [DuplicateAmendment, Cancel]
    formid = 'formduplicateamendment'


    def default_data(self):
        return self.context

    def before_update(self):
        ideas_widget = ideas_choice()
        ideas_widget.item_css_class = 'hide-bloc'
        ideas_widget.css_class = 'controlled-items'
        self.schema.get('related_ideas').widget = ideas_widget 


@view_config(
    name='duplicateamendment',
    context=Amendment,
    renderer='pontus:templates/view.pt',
    )
class DuplicateAmendmentView(MultipleView):
    title = _('Duplicate')
    name = 'duplicateamendment'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/ideas_management.js']}
    views = (DuplicateAmendmentFormView, IdeaManagementView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({DuplicateAmendment:DuplicateAmendmentView})
