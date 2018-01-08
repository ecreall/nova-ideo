# Copyright (c) 2014 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from substanced.util import Batch

from dace.util import getSite, find_catalog
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import has_role, get_current
from pontus.view import BasicView
from pontus.util import merge_dicts
from pontus.view_operation import MultipleView

from novaideo.utilities.util import (
    render_listing_objs, render_object_evaluation_stat,
    render_object_examination_stat)
from novaideo.content.processes.organization_management.behaviors import (
    SeeOrganization)
from novaideo.content.organization import Organization
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.content.processes import get_states_mapping
from novaideo.utilities.util import (
    generate_navbars, ObjectRemovedException)
from novaideo import _
from novaideo.views.filter.sort import (
    sort_view_objects)
from novaideo.views.core import asyn_component_config
from novaideo.views.filter import (
    find_entities)


class ContentView(BasicView):
    template = 'novaideo:views/novaideo_view_manager/templates/home.pt'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    content_id = 'organization-ideas'
    isactive = False
    hasparent = True

    def update(self):
        body = ''
        result = {}
        if self.isactive or self.params('on_demand') == 'load':
            current_user = get_current()
            validated = {
                'metadata_filter':
                    {'content_types': [self.content_type],
                     'states': ['active', 'published']}
            }
            novaideo_catalog = find_catalog('novaideo')
            organizations_index = novaideo_catalog['organizations']
            query = organizations_index.any([self.context.__oid__])
            objects = find_entities(
                user=current_user,
                filters=[validated],
                add_query=query)
            sort_url = self.request.resource_url(
                self.context, '@@index',
                query={'view_content_attr': self.content_id})
            objects, sort_body = sort_view_objects(
                self, objects, [self.content_type], current_user,
                sort_url=sort_url)
            url = self.request.resource_url(
                self.context, '@@index',
                query={'view_content_attr': self.content_id})
            batch = Batch(objects,
                          self.request,
                          url=url,
                          default_size=BATCH_DEFAULT_SIZE)
            batch.target = "#results-" + self.content_type
            self.title = _(self.title, mapping={'nb': batch.seqlen})
            result_body, result = render_listing_objs(
                self.request, batch, current_user,
                display_state=getattr(self, 'display_state', True))
            values = {'bodies': result_body,
                      'batch': batch,
                      'empty_message': self.empty_message,
                      'empty_icon': self.empty_icon,
                      'sort_body': sort_body}
            body = self.content(args=values, template=self.template)['body']

        item = self.adapt_item(body, self.viewid)
        item['isactive'] = getattr(self, 'isactive', False)
        result['coordinates'] = {self.coordinates: [item]}
        return result


@asyn_component_config(
    id='organization-questions',
    on_demand=True,
    delegate='organization_see_organization')
class QuestionsView(ContentView):
    title = _('Questions')
    content_id = 'organization-questions'
    content_type = 'question'
    viewid = 'organization-questions'
    view_icon = 'icon md md-live-help'
    counter_id = 'organization-questions-counter'
    empty_message = _("No asked questions")
    empty_icon = 'icon md md-live-help'


class IdeasView(ContentView):
    title = _('Ideas')
    content_id = 'organization-ideas'
    content_type = 'idea'
    viewid = 'organization-ideas'
    view_icon = 'icon novaideo-icon icon-idea'
    counter_id = 'organization-ideas-counter'
    empty_message = _("No registered ideas")
    empty_icon = 'icon novaideo-icon icon-idea'
    isactive = True
    display_state = False


@asyn_component_config(
    id='organization-proposals',
    on_demand=True,
    delegate='organization_see_organization')
class ProposalsView(ContentView):
    title = _('Working groups')
    content_id = 'organization-proposals'
    content_type = 'proposal'
    viewid = 'organization-proposals'
    view_icon = 'icon icon novaideo-icon icon-wg'
    counter_id = 'organization-proposals-counter'
    empty_message = _("Belongs to no working group")
    empty_icon = 'icon icon novaideo-icon icon-wg'


@asyn_component_config(
    id='organization-members',
    on_demand=True,
    delegate='organization_see_organization')
class MembersView(ContentView):
    title = _('Members')
    content_id = 'organization-members'
    content_type = 'person'
    viewid = 'organization-members'
    view_icon = 'icon ion-person-stalker'
    counter_id = 'organization-members-counter'
    empty_message = _("No members")
    empty_icon = 'icon ion-person-stalker'
    display_state = False


@asyn_component_config(id='organization_see_organization')
class OrganizationContentsView(MultipleView):
    title = ''
    name = 'see-organization-contents'
    viewid = 'organization-contents'
    css_class = 'simple-bloc async-new-contents-component'
    template = 'novaideo:views/templates/multipleview.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    container_css_class = 'organization-view'
    center_tabs = True
    views = (QuestionsView, IdeasView, ProposalsView, MembersView)

    def _init_views(self, views, **kwargs):
        if self.params('load_view'):
            delegated_by = kwargs.get('delegated_by', None)
            views = [IdeasView, MembersView]
            if 'question' in self.request.content_to_manage:
                views = [QuestionsView, IdeasView, MembersView]

            if 'proposal' in self.request.content_to_manage:
                views.insert(-1, ProposalsView)

            views = tuple(views)
            view_id = self.params('view_content_id')
            if 'organization-ideas' in (delegated_by, view_id):
                views = (IdeasView, )

            if 'organization-proposals' in (delegated_by, view_id):
                views = (ProposalsView, )

            if 'organization-questions' in (delegated_by, view_id):
                views = (QuestionsView, )

            if 'organization-members' in (delegated_by, view_id):
                views = (MembersView, )

        super(OrganizationContentsView, self)._init_views(views, **kwargs)


class DetailsView(BasicView):
    title = ''
    name = 'seeorganizationdetails'
    behaviors = [SeeOrganization]
    template = 'novaideo:views/organization_management/templates/see_organization.pt'
    viewid = 'seeorganizationdetails'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'

    def update(self):
        self.execute(None)
        try:
            navbars = generate_navbars(self.request, self.context)
        except ObjectRemovedException:
            return HTTPFound(self.request.resource_url(getSite(), ''))

        organization = self.context
        current_user = get_current()
        evaluation_chart = render_object_evaluation_stat(self.context, self.request)
        examination_chart = render_object_examination_stat(self.context, self.request)
        values = {
            'organization': organization,
            'state': get_states_mapping(
                current_user, organization,
                getattr(organization, 'state_or_none', [None])[0]),
            'navbar_body': navbars['navbar_body'],
            'actions_bodies': navbars['body_actions'],
            'footer_body': navbars['footer_body'],
            'is_portal_manager': has_role(role=('PortalManager',)),
            'evaluation_chart': evaluation_chart,
            'examination_chart': examination_chart,
        }
        result = {}
        result = merge_dicts(navbars['resources'], result, ('css_links', 'js_links'))
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = navbars['messages']
        item['isactive'] = navbars['isactive']
        result['coordinates'] = {self.coordinates: [item]}
        return result


@view_config(
    name='index',
    context=Organization,
    renderer='pontus:templates/views_templates/grid.pt',
    )
@view_config(
    name='',
    context=Organization,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeOrganizationView(MultipleView):
    title = ''
    name = 'seeorganization'
    template = 'novaideo:views/templates/entity_multipleview.pt'
    viewid = 'seeorganization'
    css_class = 'panel-transparent'
    views = (DetailsView, OrganizationContentsView)
    validators = [SeeOrganization.get_validator()]
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/analytics.js']}


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeOrganization: SeeOrganizationView})
