# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.proposal_management.behaviors import (
    RemoveFile)
from novaideo.content.workspace import Workspace
from novaideo import _


@view_config(
    name='removefile',
    context=Workspace,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class RemoveFileView(BasicView):
    title = _('Remove file')
    name = 'removefile'
    behaviors = [RemoveFile]
    viewid = 'removefile'

    def update(self):
        oid = self.params('oid')
        self.execute({'oid': oid})
        return HTTPFound(self.request.resource_url(self.context, "@@index"))


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {RemoveFile: RemoveFileView})
