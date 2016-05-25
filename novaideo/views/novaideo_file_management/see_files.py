# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import pytz
import datetime
from pyramid.view import view_config

from substanced.util import Batch

from dace.objectofcollaboration.principal.util import (
    get_current, has_role)
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView
from pontus.util import merge_dicts

from novaideo.utilities.util import render_listing_objs
from novaideo.content.processes.novaideo_file_management.behaviors import (
    SeeFiles)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo import _


@view_config(
    name='seefiles',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeFilesView(BasicView):
    title = _('Files')
    name = 'seefiles'
    behaviors = [SeeFiles]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seefiles'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'

    def update(self):
        self.execute(None)
        objects = self.context.files
        now = datetime.datetime.now(tz=pytz.UTC)
        objects = sorted(objects, 
                         key=lambda e: getattr(e, 'modified_at', now), 
                         reverse=True)
        batch = Batch(objects, self.request, default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_files"
        len_result = batch.seqlen
        user = get_current()
        is_portalmanager = has_role(user=user, role=('PortalManager',)),
        result_body, result = render_listing_objs(
            self.request, batch, user,
            is_portalmanager=is_portalmanager
            )
        values = {
                'bodies': result_body,
                'length': len_result,
                'batch': batch,
               }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeFiles:SeeFilesView})
