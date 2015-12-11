# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi


from pyramid.view import view_config
from pyramid import renderers
from substanced.util import get_oid

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS

from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.file import OBJECT_OID

from novaideo.content.processes.proposal_management.behaviors import (
    EditProposal)
from novaideo.content.proposal import ProposalSchema, Proposal
from novaideo import _
from novaideo.core import can_access
from .create_proposal import ideas_choice, AddIdeaFormView



class RelatedIdeasView(BasicView):
    title = _('Related Ideas')
    name = 'relatedideas'
    template = 'novaideo:views/proposal_management/templates/ideas_management.pt'
    idea_template = 'novaideo:views/proposal_management/templates/idea_data.pt'
    viewid = 'relatedideas'
    coordinates = 'right'

    def update(self):
        user = get_current()
        related_ideas = [i for i in self.context.related_ideas.keys()
                         if can_access(user, i)]
        result = {}
        target = None
        try:
            editform = self.parent.parent.validated_children[0]
            target = editform.viewid+'_'+editform.formid
        except Exception:
            pass

        ideas = []
        for i in related_ideas:
            data = {'title': i.title,
                    'id': get_oid(i),
                    'body': renderers.render(self.idea_template,
                                             {'idea': i}, self.request)
                    }
            ideas.append(data)

        values = {
            'items': ideas,
            'target': target
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class IdeaManagementView(MultipleView):
    title = _('Used ideas')
    name = 'ideasmanagementproposal'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    views = (RelatedIdeasView, AddIdeaFormView)
    coordinates = 'right'
    css_class = 'idea-managements panel-success'


class EditProposalFormView(FormView):
    title = _('Edit the proposal')
    schema = select(ProposalSchema(factory=Proposal, editable=True,
                               omit=['related_ideas', 'add_files']),
                    ['title',
                     'description',
                     'keywords',
                     'text',
                     'related_ideas',
                     'add_files'])
    behaviors = [EditProposal, Cancel]
    formid = 'formeditproposal'
    name = 'editproposalform'

    def default_data(self):
        data = self.context.get_data(self.schema)
        attached_files = self.context.attached_files
        if attached_files:
            data['add_files'] = {'ws_files': attached_files}

        data[OBJECT_OID] = str(get_oid(self.context))
        return data

    def before_update(self):
        ideas_widget = ideas_choice(self.context, self.request)
        ideas_widget.item_css_class = 'hide-bloc'
        ideas_widget.css_class = 'controlled-items'
        self.schema.get('related_ideas').widget = ideas_widget


@view_config(
    name='editproposal',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditProposalView(MultipleView):
    title = _('Edit the proposal')
    name = 'editproposal'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/ideas_management.js']}
    views = (EditProposalFormView, IdeaManagementView)
    validators = [EditProposal.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({EditProposal: EditProposalView})
