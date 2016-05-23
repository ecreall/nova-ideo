# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from dace.objectofcollaboration.principal.util import (
    get_current, has_role)
from dace.util import getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.novaideo_file_management.behaviors import (
    SeeFile)
from novaideo.core import FileEntity
from novaideo.utilities.util import generate_navbars, ObjectRemovedException
from novaideo.content.processes import get_states_mapping


@view_config(
    name='seefile',
    context=FileEntity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeFileView(BasicView):
    title = ''
    name = 'seefile'
    behaviors = [SeeFile]
    template = 'novaideo:views/novaideo_file_management/templates/see_file.pt'
    viewid = 'seefile'

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
                user, self.context, self.context.state[0]),
            'is_portalmanager': has_role(user=user, role=('PortalManager',)),
            'navbar_body': navbars['navbar_body'],
            'actions_bodies': navbars['body_actions'],
            'footer_body': navbars['footer_body']
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = navbars['messages']
        item['isactive'] = navbars['isactive']
        result.update(navbars['resources'])
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeFile: SeeFileView})
