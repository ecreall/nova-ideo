import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView
from pontus.form import FormView
from pontus.schema import select
from pontus.default_behavior import Cancel
from pontus.view_operation import MultipleView
from pontus.file import Object as ObjectType

from novaideo.content.processes.proposal_management.behaviors import  ImproveProposal
from novaideo.content.proposal import Proposal
from novaideo.content.amendment import AmendmentSchema
from novaideo import _
from .edit_proposal import AddIdeaSchema, AddIdea, AddIdeaFormView, RelatedIdeasView, IdeaManagementView
from .create_proposal import ideas_choice


class ImproveProposalFormView(FormView):
    title = _('Improve')
    name = 'improveproposal'
    viewid = 'improveproposal'
    formid = 'formimproveproposal'
    behaviors = [ImproveProposal, Cancel]
    schema = select(AmendmentSchema(widget=deform.widget.FormWidget(css_class='amendmentform',omit=['keywords', 'related_ideas'])),
                    ['title',
                     'description',
                     'keywords', 
                     'text', 
                     'related_ideas'])
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/improve_proposal.js']}


    def default_data(self):
        return self.context


    def before_update(self):
        ideas_widget = ideas_choice()
        ideas_widget.item_css_class = 'hide-bloc'
        ideas_widget.css_class = 'controlled-items'
        self.schema.get('related_ideas').widget = ideas_widget 



@view_config(
    name='improveproposal',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class ImproveProposalView(MultipleView):
    title = _('Improve')
    name = 'improveproposal'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/ideas_management.js']}
    views = (ImproveProposalFormView, IdeaManagementView)

DEFAULTMAPPING_ACTIONS_VIEWS.update({ImproveProposal:ImproveProposalView})
