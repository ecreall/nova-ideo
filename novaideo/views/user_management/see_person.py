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

        now = datetime.datetime.now(tz=pytz.UTC)
        objects = sorted(
            objects,
            key=lambda e: getattr(e, 'modified_at', now),
            reverse=True)
        url = self.request.resource_url(
            self.context, '@@seeperson',
            query={'view_content_attr': self.content_attr})
        batch = Batch(objects,
                      self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results"+"-"+ self.content_attr
        result_body, result = render_listing_objs(
            self.request, batch, user)
        values = {'bodies': result_body,
                  'batch': batch,
                  'empty_message': self.empty_message,
                  'empty_icon': self.empty_icon}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class IdeasView(ContentView):
    title = _('Her ideas')
    content_attr = 'ideas'
    viewid = 'person-ideas'
    view_icon = 'icon novaideo-icon icon-idea'
    empty_message = _("No registered ideas")
    empty_icon = 'icon novaideo-icon icon-idea'


class ProposalsView(ContentView):
    title = _('Her working groups')
    content_attr = 'proposals'
    viewid = 'person-proposals'
    view_icon = 'icon icon novaideo-icon icon-wg'
    empty_message = _("Not belong to any working group")
    empty_icon = 'icon icon novaideo-icon icon-wg'


class PersonContentsView(MultipleView):
    title = 'person-contents'
    name = 'see-person-contents'
    viewid = 'person-contents'
    css_class = 'simple-bloc'
    container_css_class = 'person-view'
    views = (IdeasView, ProposalsView)

    def _init_views(self, views, **kwargs):
        if self.request.is_idea_box:
            views = (IdeasView, )

        if self.params('view_content_attr') == 'ideas':
            views = (IdeasView, )

        if self.params('view_content_attr') == 'proposals':
            views = (ProposalsView, )

        super(PersonContentsView, self)._init_views(views, **kwargs)


@view_config(
    name='seeperson',
    context=Person,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeePersonView(BasicView):
    title = ''
    name = 'seeperson'
    behaviors = [SeePerson]
    template = 'novaideo:views/user_management/templates/see_person.pt'
    viewid = 'seeperson'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    css_class = 'simple-bloc user-view-index'

    def update(self):
        self.execute(None)
        try:
            navbars = generate_navbars(self.request, self.context)
        except ObjectRemovedException:
            return HTTPFound(self.request.resource_url(getSite(), ''))

        user = self.context
        current_user = get_current()
        contents = PersonContentsView(self.context, self.request).update()
        contents_body = contents['coordinates'][PersonContentsView.coordinates][0]['body']
        values = {
            'user': user,
            'contents': contents_body,
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
        result = merge_dicts(contents, result, ('css_links', 'js_links'))
        result = merge_dicts(navbars['resources'], result, ('css_links', 'js_links'))
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = navbars['messages']
        item['isactive'] = navbars['isactive']
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeePerson: SeePersonView})
