import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView
from pontus.form import FormView
from pontus.schema import select
from pontus.default_behavior import Cancel

from novaideo.content.processes.proposal_management.behaviors import  ImproveProposal
from novaideo.content.proposal import Proposal
from novaideo.content.amendment import AmendmentSchema
from novaideo import _


@view_config(
    name='improveproposal',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class ImproveProposalView(FormView):
    title = _('Improve')
    name = 'improveproposal'
    viewid = 'improveproposal'
    formid = 'formimproveproposal'
    behaviors = [ImproveProposal, Cancel]
    schema = select(AmendmentSchema(widget=deform.widget.FormWidget(css_class='amendmentform')),['description',
                                       'keywords', 
                                       'text', 
                                       'confirmation'])
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/action_confirmation.js']}



    def default_data(self):
        return self.context


    def before_update(self):
        self.schema.widget.template = 'novaideo:views/templates/form.pt'
        self.schema.widget.to_confirm = _('Improve')
        self.schema.get('confirmation').get('replaced_idea').widget.template = 'novaideo:views/templates/mapping_col.pt'
        self.schema.get('confirmation').get('idea_of_replacement').widget.template = 'novaideo:views/templates/mapping_col.pt'


DEFAULTMAPPING_ACTIONS_VIEWS.update({ImproveProposal:ImproveProposalView})
