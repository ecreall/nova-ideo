# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform
import datetime
import pytz
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid import renderers
from substanced.util import get_oid

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite
from dace.processinstance.core import Behavior
from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, Schema
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.file import Object as ObjectType
from pontus.widget import AjaxSelect2Widget

from novaideo.content.processes.work_mode_processes.\
    wiki_work_mode_process.behaviors import (
        CorrectProposal)
from novaideo.content.proposal import ProposalSchema, Proposal
from novaideo.content.idea import IdeaSchema, Idea
from novaideo import _
from novaideo.core import can_access
from novaideo.views.widget import SimpleMappingtWidget
from novaideo.views.proposal_management.create_proposal import ideas_choice
from novaideo.utilities.util import to_localized_time


@colander.deferred
def idea_choice(node, kw):
    request = node.bindings['request']
    root = getSite()
    values = []
    values.insert(0, ('', _('- Select -')))
    ajax_url = request.resource_url(root, '@@novaideoapi',
                                    query={'op': 'find_ideas'})
    return AjaxSelect2Widget(
        values=values,
        ajax_url=ajax_url,
        css_class="search-idea-form")


class AddIdeaSchema(Schema):

    idea = colander.SchemaNode(
        ObjectType(),
        widget=idea_choice,
        title=_('Re-use one or more existing idea(s)'),
        missing=None,
        #description=_('Choose an idea')
        )

    new_idea_choice = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(css_class="new-idea-control"),
        label=_('Add a new idea'),
        title='',
        missing=False
        )

    new_idea = select(IdeaSchema(factory=Idea,
                                 editable=True,
                                 omit=['keywords'],
                                 widget=SimpleMappingtWidget(
                                    mapping_css_class='hide-bloc new-idea-form',
                                    ajax=False)),
                    ['challenge',
                     'title',
                     'text',
                     'keywords'])


class AddIdea(Behavior):

    behavior_id = "addidea"
    title = _("Validate")
    description = _("Re-use one or more existing idea(s)")

    def start(self, context, request, appstruct, **kw):
        return {}

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

    def default_data(self):
        localizer = self.request.localizer
        user = get_current()
        time = to_localized_time(datetime.datetime.now(
            tz=pytz.UTC), translate=True)
        title = localizer.translate(_('Idea by'))+' '+\
                getattr(user, 'title', user.name)+' '+\
                localizer.translate(_('the'))+' '+\
                time
        challenge = getattr(self.context, 'challenge', '')
        if challenge and not challenge.can_add_content:
            challenge = ''

        return {'new_idea': {'title': title,
                             'challenge': challenge}}


class RelatedIdeasView(BasicView):
    title = _('Related Ideas')
    name = 'relatedideas'
    template = 'novaideo:views/proposal_management/templates/ideas_management.pt'
    idea_template = 'novaideo:views/proposal_management/templates/idea_data.pt'
    viewid = 'relatedideas'
    coordinates = 'right'

    def update(self):
        user = get_current()
        related_ideas = [i for i in self.context.related_ideas
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
    title = _('Ideas being used')
    name = 'ideasmanagementproposal'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (RelatedIdeasView, AddIdeaFormView)
    coordinates = 'right'
    css_class = 'idea-managements panel-success'


class CorrectProposalFormView(FormView):
    title = _('Edit the proposal')
    schema = select(ProposalSchema(),
                    ['title',
                     'description',
                     'keywords',
                     'text',
                     'related_ideas',
                     'add_files'
                     ])
    behaviors = [CorrectProposal, Cancel]
    formid = 'formcorrectproposal'
    name = 'correctproposalform'

    def default_data(self):
        data = self.context.get_data(self.schema)
        attached_files = self.context.attached_files
        if attached_files:
            data['add_files'] = {'ws_files': attached_files}

        return data

    def before_update(self):
        ideas_widget = ideas_choice(self.context, self.request)
        ideas_widget.item_css_class = 'hide-bloc'
        ideas_widget.css_class = 'controlled-items'
        self.schema.get('related_ideas').widget = ideas_widget


@view_config(
    name='improveproposalwiki',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CorrectProposalView(MultipleView):
    title = _('Improve the proposal')
    name = 'improveproposalwiki'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/ideas_management.js']}
    views = (CorrectProposalFormView, IdeaManagementView)
    validators = [CorrectProposal.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({CorrectProposal: CorrectProposalView})
