import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView

from novaideo.content.processes.amendment_management.behaviors import  EditAmendment
from novaideo.content.amendment import AmendmentSchema, Amendment
from novaideo import _
from novaideo.views.proposal_management.edit_proposal import IdeaManagementView
from novaideo.views.proposal_management.create_proposal import ideas_choice



class EditAmendmentFormView(FormView):
    title = _('Edit amendment')
    schema = select(AmendmentSchema(factory=Amendment, editable=True, omit=['keywords', 'related_ideas']),
                    ['title',
                     'description',
                     'keywords', 
                     'text', 
                     'related_ideas'])
    behaviors = [EditAmendment, Cancel]
    formid = 'formeditamendment'
    name='editamendment'

    def default_data(self):
        return self.context

    def before_update(self):
        ideas_widget = ideas_choice()
        ideas_widget.item_css_class = 'hide-bloc'
        ideas_widget.css_class = 'controlled-items'
        self.schema.get('related_ideas').widget = ideas_widget 


@view_config(
    name='editamendment',
    context=Amendment,
    renderer='pontus:templates/view.pt',
    )
class EditAmendmentView(MultipleView):
    title = _('Edit amendment')
    name = 'editamendment'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/ideas_management.js']}
    views = (EditAmendmentFormView, IdeaManagementView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({EditAmendment:EditAmendmentView})
