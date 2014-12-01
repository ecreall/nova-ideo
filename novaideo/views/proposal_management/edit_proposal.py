# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid import renderers
from substanced.util import get_oid

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite, find_entities
from dace.processinstance.core import  Behavior
from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, Schema
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.file import Object as ObjectType
from pontus.widget import Select2Widget

from novaideo.content.processes.proposal_management.behaviors import (
    EditProposal)
from novaideo.content.proposal import ProposalSchema, Proposal
from novaideo.content.idea import IdeaSchema, Idea, Iidea
from novaideo import _
from novaideo.core import can_access
from novaideo.views.widget import Select2WidgetSearch, SimpleMappingtWidget


@colander.deferred
def idea_choice(node, kw):
    request = node.bindings['request']
    root = getSite()
    user = get_current()
    ideas = list(user.ideas)
    ideas.extend([ i for i in user.selections \
                   if isinstance(i, Idea) and can_access(user, i)])
    ideas = set(ideas) 
    values = [(i, i.title) for i in ideas if not('archived' in i.state)]
    values.insert(0, ('', _('- Select -')))
    return Select2WidgetSearch(values=values, item_css_class='search-idea-form',
                                url=request.resource_url(root, '@@search', 
                                            query={'op':'toselect', 
                                                     'content_types':['Idea']}))


class AddIdeaSchema(Schema):

    idea = colander.SchemaNode(
        ObjectType(),
        widget=idea_choice,
        title=_('Use an idea'),
        missing=None,
        description=_('Choose an idea')
        )

    new_idea_choice = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(css_class="new-idea-control"),
        label=_('Add a new idea'),
        title ='',
        missing=False
        )

    new_idea = select(IdeaSchema(factory=Idea, 
                                 editable=True,
                                 omit=['keywords'], 
                                 widget=SimpleMappingtWidget(
                                         mapping_css_class='hide-bloc new-idea-form',
                                        ajax=False)),
                    ['title',
                     'text',
                     'keywords'])


class AddIdea(Behavior):

    behavior_id = "addidea"
    title = _("Validate")
    description = _("Use an idea")

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class AddIdeaFormView(FormView):

    title = _('Add a new idea')
    schema = AddIdeaSchema()
    formid = 'formaddidea'
    behaviors = [AddIdea]
    name = 'addideaform'
    coordinates = 'right'

    def before_update(self):
        root = getSite()
        formwidget = deform.widget.FormWidget(css_class='add-idea-form')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        formwidget.ajax_url = self.request.resource_url(root, 
                                           '@@ideasmanagement')
        self.schema.widget = formwidget
        self.schema.widget.ajax_button = _('Validate')
        self.schema.get('new_idea').get('keywords').default = []


class RelatedIdeasView(BasicView):
    title = _('Related Ideas')
    name = 'relatedideas'
    template = 'novaideo:views/proposal_management/templates/ideas_management.pt'
    idea_template = 'novaideo:views/proposal_management/templates/idea_data.pt'
    viewid = 'relatedideas'
    coordinates = 'right'

    def update(self):
        user = get_current()
        related_ideas = [i for i in self.context.related_ideas.keys() \
                         if can_access(user, i)]
        result = {}
        target = None
        try:
            editform = self.parent.parent.children[0]
            target = editform.viewid+'_'+editform.formid 
        except Exception:
            pass

        ideas = []
        for i in related_ideas:
            data = {'title': i.title,
                    'id': get_oid(i),
                    'body': renderers.render(self.idea_template, 
                                             {'idea':i}, self.request)
                    }
            ideas.append(data)

        values = {
                'items': ideas,
                'target' : target
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class IdeaManagementView(MultipleView):
    title = _('Used ideas')
    name = 'ideasmanagementproposal'
    template = 'pontus.dace_ui_extension:templates/simple_mergedmultipleview.pt'
    views = (RelatedIdeasView, AddIdeaFormView)
    coordinates = 'right'
    css_class = 'idea-managements panel-success'


def ideas_choice():
    user = get_current()
    ideas = find_entities([Iidea], states=('archived',), not_any=True) 
    values = [(i, i.title) for i in ideas if can_access(user, i)]
    return Select2Widget(values=values, multiple=True)


class EditProposalFormView(FormView):
    title = _('Edit')
    schema = select(ProposalSchema(factory=Proposal, editable=True,
                               omit=['keywords', 'related_ideas']),
                    ['title',
                     'description',
                     'keywords',
                     'text',
                     'related_ideas'])
    behaviors = [EditProposal, Cancel]
    formid = 'formeditproposal'
    name = 'editproposalform'

    def default_data(self):
        return self.context

    def before_update(self):
        ideas_widget = ideas_choice()
        ideas_widget.item_css_class = 'hide-bloc'
        ideas_widget.css_class = 'controlled-items'
        self.schema.get('related_ideas').widget = ideas_widget


@view_config(
    name='editproposal',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditProposalView(MultipleView):
    title = _('Edit')
    name = 'editproposal'
    template = 'pontus.dace_ui_extension:templates/simple_mergedmultipleview.pt'
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/ideas_management.js']}
    views = (EditProposalFormView, IdeaManagementView)
    validators = [EditProposal.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({EditProposal: EditProposalView})
