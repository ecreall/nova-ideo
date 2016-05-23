# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from substanced.util import Batch

from dace.util import getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import has_role, get_current
from pontus.view import BasicView
from pontus.util import merge_dicts

from novaideo.utilities.util import generate_listing_menu, ObjectRemovedException
from novaideo.content.processes.user_management.behaviors import SeePerson
from novaideo.content.person import Person
from novaideo.views.novaideo_view_manager.search import SearchResultView
from novaideo.core import BATCH_DEFAULT_SIZE, can_access
from novaideo.content.processes import get_states_mapping
from novaideo.utilities.util import (
    generate_navbars, ObjectRemovedException)


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

    def update(self):
        self.execute(None)
        try:
            navbars = generate_navbars(self.request, self.context)
        except ObjectRemovedException:
            return HTTPFound(self.request.resource_url(getSite(), ''))

        user = self.context
        current_user = get_current()
        objects = []
        if current_user is user:
            objects = list(filter(lambda o: 'archived' not in o.state,
                             getattr(user, 'contents', [])))
        else:
            objects = list(filter(lambda o: can_access(current_user, o) and
                                       'archived' not in o.state,
                             getattr(user, 'contents', [])))
        batch = Batch(objects, self.request, default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_contents"
        len_result = batch.seqlen
        resources = {'css_links': [], 'js_links': []}
        result_body = []
        for obj in batch:
            try:
                menu = generate_listing_menu(
                    self.request, obj,
                    template='novaideo:views/templates/listing_object_actions.pt')
            except ObjectRemovedException:
                continue

            resources = merge_dicts(menu['resources'], resources)
            object_values = {'object': obj,
                             'current_user': current_user,
                             'menu_body': menu['menu_body'],
                             'state': get_states_mapping(
                                  current_user, obj,
                                  getattr(obj, 'state_or_none', [None])[0])
                             }
            body = self.content(
                args=object_values,
                template=obj.templates.get('default'))['body']
            result_body.append(body)

        values = {
            'bodies': result_body,
            'length': len_result,
            'batch': batch
        }
        contents_body = self.content(
            args=values,
            template=SearchResultView.template)['body']
        values = {
            'user': user,
            'len_contents': len_result,
            'contents': (result_body and contents_body) or None,
            'proposals': None,
            'state': get_states_mapping(
                current_user, user,
                getattr(user, 'state_or_none', [None])[0]),
            'navbar_body': navbars['navbar_body'],
            'actions_bodies': navbars['body_actions'],
            'footer_body': navbars['footer_body'],
            'is_portal_manager': has_role(role=('PortalManager',))
        }
        resources = merge_dicts(navbars['resources'], resources)
        result = resources
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = navbars['messages']
        item['isactive'] = navbars['isactive']
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeePerson: SeePersonView})
