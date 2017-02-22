# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from substanced.util import Batch

from dace.util import getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import has_role, get_current
from pontus.view import BasicView
from pontus.util import merge_dicts
from pontus.view_operation import MultipleView

from novaideo.utilities.util import render_listing_objs
from novaideo.content.processes.user_management.behaviors import SeePerson
from novaideo.content.person import Person
from novaideo.core import BATCH_DEFAULT_SIZE, can_access
from novaideo.content.processes import get_states_mapping
from novaideo.utilities.util import (
    generate_navbars, ObjectRemovedException)
from novaideo import _
from novaideo.views.filter.sort import (
    sort_view_objects)
from novaideo.views.core import asyn_component_config


class ContentView(BasicView):
    template = 'novaideo:views/novaideo_view_manager/templates/home.pt'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    content_attr = 'ideas'

    def update(self):
        if self.request.is_idea_box:
            self.title = ''

        user = self.context
        current_user = get_current()
        objects = []
        if current_user is user:
            objects = list(filter(lambda o: 'archived' not in o.state,
                             getattr(user, self.content_attr, [])))
        else:
            objects = list(filter(lambda o: can_access(current_user, o) and
                                       'archived' not in o.state,
                             getattr(user, self.content_attr, [])))
        sort_url = self.request.resource_url(
            self.context, '@@index',
            query={'view_content_attr': self.content_attr})
        objects, sort_body = sort_view_objects(
            self, objects, [self.content_type], user,
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
    title = _('His/her questions (${nb})')
    content_attr = 'questions'
    content_type = 'question'
    viewid = 'person-questions'
    view_icon = 'icon md md-live-help'
    counter_id = 'person-questions-counter'
    empty_message = _("No asked questions")
    empty_icon = 'icon md md-live-help'


class IdeasView(ContentView):
    title = _('His/her ideas (${nb})')
    content_attr = 'ideas'
    content_type = 'idea'
    viewid = 'person-ideas'
    view_icon = 'icon novaideo-icon icon-idea'
    counter_id = 'person-ideas-counter'
    empty_message = _("No registered ideas")
    empty_icon = 'icon novaideo-icon icon-idea'
    isactive = True


class ProposalsView(ContentView):
    title = _('His/her working groups (${nb})')
    content_attr = 'proposals'
    content_type = 'proposal'
    viewid = 'person-proposals'
    view_icon = 'icon icon novaideo-icon icon-wg'
    counter_id = 'person-proposals-counter'
    empty_message = _("Belongs to no working group")
    empty_icon = 'icon icon novaideo-icon icon-wg'


@asyn_component_config(id='person_see_person')
class PersonContentsView(MultipleView):
    title = ''
    name = 'see-person-contents'
    viewid = 'person-contents'
    css_class = 'simple-bloc'
    template = 'novaideo:views/templates/multipleview.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    container_css_class = 'person-view'
    center_tabs = True
    views = (QuestionsView, IdeasView, ProposalsView)

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

        super(PersonContentsView, self)._init_views(views, **kwargs)


class DetailsView(BasicView):
    title = ''
    name = 'seepersondetails'
    behaviors = [SeePerson]
    template = 'novaideo:views/user_management/templates/see_person.pt'
    viewid = 'seepersondetails'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'

    def update(self):
        self.execute(None)
        try:
            navbars = generate_navbars(self.request, self.context)
        except ObjectRemovedException:
            return HTTPFound(self.request.resource_url(getSite(), ''))

        user = self.context
        current_user = get_current()
        values = {
            'user': user,
            'proposals': None,
            'state': get_states_mapping(
                current_user, user,
                getattr(user, 'state_or_none', [None])[0]),
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
    context=Person,
    renderer='pontus:templates/views_templates/grid.pt',
    )
@view_config(
    name='',
    context=Person,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeePersonView(MultipleView):
    title = ''
    name = 'seeperson'
    template = 'novaideo:views/templates/entity_multipleview.pt'
    viewid = 'seeperson'
    css_class = 'simple-bloc'
    container_css_class = 'home'
    views = (DetailsView, PersonContentsView)
    validators = [SeePerson.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeePerson: SeePersonView})
