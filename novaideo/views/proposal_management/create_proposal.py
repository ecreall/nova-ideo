
from pyramid.view import view_config

from dace.util import getSite, find_entities
from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.widget import Select2Widget

from novaideo.content.processes.proposal_management.behaviors import (
    CreateProposal)
from novaideo.content.proposal import ProposalSchema, Proposal
from novaideo.content.idea import Iidea
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.core import can_access
from .edit_proposal import AddIdeaFormView



class RelatedIdeasView(BasicView):
    title = _('Related Ideas')
    name = 'relatedideas'
    template = 'novaideo:views/proposal_management/templates/ideas_management.pt'
    idea_template = 'novaideo:views/proposal_management/templates/idea_data.pt'
    viewid = 'relatedideas'
    coordinates = 'right'

    def update(self):
        result = {}
        target = None
        try:
            editform = self.parent.parent.children[0]
            target = editform.viewid + '_' + editform.formid 
        except Exception:
            pass

        ideas = []
        values = {
                'items': ideas,
                'target' : target
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class IdeaManagementView(MultipleView):
    title = _('Ideas management')
    name = 'ideasmanagementproposal'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    views = (RelatedIdeasView, AddIdeaFormView)
    coordinates = 'right'
    css_class = 'panel-success'



def ideas_choice():
    user = get_current()
    ideas = find_entities([Iidea], states=('archived',), not_any=True)    
    values = [(i, i.title) for i in ideas if can_access(user, i)]
    return Select2Widget(values=values, multiple=True)


class CreateProposalFormView(FormView):

    title = _('Create a proposal')
    schema = select(ProposalSchema(factory=Proposal, editable=True,
                               omit=['keywords', 'related_ideas']),
                    ['title',
                     'description',
                     'keywords',
                     'related_ideas'])
    behaviors = [CreateProposal, Cancel]
    formid = 'formcreateproposal'
    name = 'createproposal'

    def before_update(self):
        ideas_widget = ideas_choice()
        ideas_widget.item_css_class = 'hide-bloc'
        ideas_widget.css_class = 'controlled-items'
        self.schema.get('related_ideas').widget = ideas_widget 


@view_config(
    name='createproposal',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class CreateProposalView(MultipleView):
    title = _('Create a proposal')
    name = 'createproposal'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/ideas_management.js']}
    views = (CreateProposalFormView, IdeaManagementView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({CreateProposal: CreateProposalView})