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

from dace.objectofcollaboration.principal.util import get_current
from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite
from dace.processinstance.core import Behavior
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, Schema
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.file import Object as ObjectType
from pontus.widget import AjaxSelect2Widget

from novaideo.content.idea import IdeaSchema, Idea
from novaideo.content.processes.proposal_management.behaviors import (
    CreateProposal)
from novaideo.content.proposal import ProposalSchema, Proposal
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.utilities.util import to_localized_time
from novaideo.views.widget import SimpleMappingtWidget
from novaideo import _, log


def add_file_data(file_):
    if file_ and hasattr(file_, 'get_data'):
        return file_.get_data(None)

    return None


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
        time = to_localized_time(
            datetime.datetime.now(
                tz=self.request.get_time_zone),
            translate=True)
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
        result = {}
        target = None
        try:
            editform = self.parent.parent.validated_children[0]
            target = editform.viewid + '_' + editform.formid
        except Exception:
            pass

        ideas = []
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


def ideas_choice(context, request):
    values = []
    ajax_url = request.resource_url(context,
                                    '@@novaideoapi',
                                    query={'op': 'find_ideas'})

    def title_getter(oid):
        try:
            obj = get_obj(int(oid), None)
            if obj:
                return obj.title
            else:
                return oid
        except Exception as e:
            log.warning(e)
            return oid

    return AjaxSelect2Widget(
        values=values,
        ajax_url=ajax_url,
        multiple=True,
        title_getter=title_getter,
        )


class CreateProposalFormView(FormView):

    title = _('Create a proposal')
    schema = select(ProposalSchema(factory=Proposal, editable=True,
                               omit=['related_ideas', 'add_files']),
                    ['challenge',
                     'title',
                     'description',
                     'keywords',
                     'text',
                     'related_ideas',
                     ('add_files', ['attached_files'])])
    behaviors = [CreateProposal, Cancel]
    formid = 'formcreateproposal'
    name = 'createproposal'

    def before_update(self):
        ideas_widget = ideas_choice(self.context, self.request)
        ideas_widget.item_css_class = 'hide-bloc'
        ideas_widget.css_class = 'controlled-items'
        self.schema.get('related_ideas').widget = ideas_widget


@view_config(
    name='createproposal',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CreateProposalView(MultipleView):
    title = _('Create a proposal')
    name = 'createproposal'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/ideas_management.js']}
    views = (CreateProposalFormView, IdeaManagementView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({CreateProposal: CreateProposalView})