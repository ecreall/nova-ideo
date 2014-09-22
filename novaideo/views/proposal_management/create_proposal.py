import deform 
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, Schema

from novaideo.content.processes.proposal_management.behaviors import  CreateProposal
from novaideo.content.proposal import ProposalSchema, RelatedIdeasSchema, Proposal
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


class CreateProposalSchema(Schema):

    related_ideas  = RelatedIdeasSchema(widget=deform.widget.MappingWidget(mapping_css_class='form-idea-select'))

    proposal = select(ProposalSchema(factory=Proposal, 
                                     editable=True, 
                                     widget=deform.widget.MappingWidget(mapping_css_class='form-proposal-confirmation'),
                                     omit=['keywords']),
                     ['title', 'description', 'keywords'])


@view_config(
    name='createproposal',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class CreateProposalView(FormView):

    title = _('Create a proposal')
    schema = CreateProposalSchema()
    behaviors = [CreateProposal, Cancel]
    formid = 'formcreateproposal'
    name='createproposal'
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/creat_proposal.js']}



    def before_update(self):
        self.schema.get('related_ideas').widget.template = 'novaideo:views/templates/mapping_simple.pt'
        self.schema.get('proposal').widget.template = 'novaideo:views/templates/mapping_simple.pt'


DEFAULTMAPPING_ACTIONS_VIEWS.update({CreateProposal: CreateProposalView})
