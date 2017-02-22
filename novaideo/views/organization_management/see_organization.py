# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

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

from novaideo.utilities.util import render_listing_objs
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
    content_attr = 'ideas'

    def update(self):
        if self.request.is_idea_box:
            self.title = ''

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
            query={'view_content_attr': self.content_attr})
        objects, sort_body = sort_view_objects(
            self, objects, [self.content_type], current_user,
            sort_url=sort_url)
        url = self.request.resource_url(
            self.context, '@@index',
            query={'view_content_attr': self.content_attr})
        batch = Batch(objects,
                      self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results"+"-"+ self.content_attr
        self.title = _(self.title, mapping={'nb': batch.seqlen})
        result_body, result = render_listing_objs(
            self.request, batch, current_user)
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


class QuestionsView(ContentView):
    title = _('Questions (${nb})')
    content_attr = 'questions'
    content_type = 'question'
    viewid = 'organization-questions'
    view_icon = 'icon md md-live-help'
    counter_id = 'organization-questions-counter'
    empty_message = _("No asked questions")
    empty_icon = 'icon md md-live-help'


class IdeasView(ContentView):
    title = _('Ideas (${nb})')
    content_attr = 'ideas'
    content_type = 'idea'
    viewid = 'organization-ideas'
    view_icon = 'icon novaideo-icon icon-idea'
    counter_id = 'organization-ideas-counter'
    empty_message = _("No registered ideas")
    empty_icon = 'icon novaideo-icon icon-idea'


class ProposalsView(ContentView):
    title = _('Working groups (${nb})')
    content_attr = 'proposals'
    content_type = 'proposal'
    viewid = 'organization-proposals'
    view_icon = 'icon icon novaideo-icon icon-wg'
    counter_id = 'organization-proposals-counter'
    empty_message = _("Belongs to no working group")
    empty_icon = 'icon icon novaideo-icon icon-wg'


class MembersView(ContentView):
    title = _('Members (${nb})')
    content_attr = 'members'
    content_type = 'person'
    viewid = 'organization-members'
    view_icon = 'icon ion-person-stalker'
    counter_id = 'organization-members-counter'
    empty_message = _("No members")
    empty_icon = 'icon ion-person-stalker'
    isactive = True


@asyn_component_config(id='organization_see_organization')
class OrganizationContentsView(MultipleView):
    title = ''
    name = 'see-organization-contents'
    viewid = 'organization-contents'
    css_class = 'simple-bloc'
    template = 'novaideo:views/templates/multipleview.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    container_css_class = 'organization-view'
    center_tabs = True
    views = (MembersView, QuestionsView, IdeasView, ProposalsView)

    def _init_views(self, views, **kwargs):
        if self.params('load_view'):
            if self.request.is_idea_box:
                views = (IdeasView, )

            if self.params('view_content_attr') == 'ideas':
                views = (IdeasView, )

            if self.params('view_content_attr') == 'proposals':
                views = (ProposalsView, )

            if self.params('view_content_attr') == 'questions':
                views = (QuestionsView, )

            if self.params('view_content_attr') == 'members':
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
        values = {
            'organization': organization,
            'state': get_states_mapping(
                current_user, organization,
                getattr(organization, 'state_or_none', [None])[0]),
            'navbar_body': navbars['navbar_body'],
            'actions_bodies': navbars['body_actions'],
            'footer_body': navbars['footer_body'],
            'is_portal_manager': has_role(role=('PortalManager',))
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
    css_class = 'simple-bloc'
    container_css_class = 'home'
    views = (DetailsView, OrganizationContentsView)
    validators = [SeeOrganization.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeOrganization: SeeOrganizationView})
