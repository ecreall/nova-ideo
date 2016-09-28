# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import math
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from substanced.util import get_oid

from dace.util import getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.proposal_management.behaviors import (
    SeeWorkspace)
from novaideo.content.workspace import Workspace
from novaideo.utilities.util import (
    generate_navbars, ObjectRemovedException, render_files)


@view_config(
    name='',
    context=Workspace,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeWorkspaceView(BasicView):
    title = ''
    name = 'seeworkspace'
    behaviors = [SeeWorkspace]
    template = 'novaideo:views/proposal_management/templates/see_workspace.pt'
    file_template = 'novaideo:views/proposal_management/templates/up_file_result.pt'
    viewid = 'seeworkspace'

    def update(self):
        self.execute(None)
        try:
            navbars = generate_navbars(self.request, self.context)
        except ObjectRemovedException:
            return HTTPFound(self.request.resource_url(getSite(), ''))

        result = {}
        can_remove_file = any(a.action.node_id == 'remove_file'
                              for a in self.context.actions)
        files = self.context.files
        files_bodies = render_files(
            files, self.request, self.file_template, True)
        values = {
            'workspace': self.context,
            'files': files_bodies,
            'get_oid': get_oid,
            'can_remove_file': can_remove_file,
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
    {SeeWorkspace: SeeWorkspaceView})
