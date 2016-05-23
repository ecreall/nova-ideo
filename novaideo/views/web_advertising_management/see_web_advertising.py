# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView

from novaideo.content.processes.advertising_management.behaviors import (
    SeeWebAdvertising)
from novaideo.content.web_advertising import WebAdvertising
from novaideo.content.processes import get_states_mapping
from novaideo.utilities.util import (
    generate_navbars,
    ObjectRemovedException)


@view_config(
    name='seewebadvertising',
    context=WebAdvertising,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeWebAdvertisingView(BasicView):
    title = ''
    name = 'seewebadvertising'
    viewid = 'seewebadvertising'
    behaviors = [SeeWebAdvertising]
    template = 'novaideo:views/web_advertising_management/templates/see_web_advertising.pt'

    def update(self):
        self.execute(None)
        try:
            navbars = generate_navbars(self.request, self.context)
        except ObjectRemovedException:
            return HTTPFound(self.request.resource_url(getSite(), ''))

        result = {}
        user = get_current()
        values = {
            'object': self.context,
            'state': get_states_mapping(
                user, self.context,
                getattr(self.context, 'state_or_none', [None])[0]),
            'navbar_body': navbars['navbar_body']
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = navbars['messages']
        item['isactive'] = navbars['isactive']
        result.update(navbars['resources'])
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeWebAdvertising: SeeWebAdvertisingView})
