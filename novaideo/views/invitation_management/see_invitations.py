# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from substanced.util import Batch

from dace.processinstance.activity import ActionType
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView
from pontus.util import merge_dicts
from daceui.interfaces import IDaceUIAPI

from novaideo.content.processes.invitation_management.behaviors import (
    SeeInvitations)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.content.processes import get_states_mapping
from novaideo import _
from novaideo.core import can_access
from novaideo.content.interface import IInvitation
from novaideo.utilities.util import render_listing_objs
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.views.filter import find_entities


CONTENTS_MESSAGES = {
    '0': _(u"""No invitation found"""),
    '1': _(u"""One invitation found"""),
    '*': _(u"""${nember} invitations found""")
}


@view_config(
    name='seeinvitations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeInvitationsView(BasicView):
    title = _('The invitations')
    name = 'seeinvitations'
    behaviors = [SeeInvitations]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seeinvitations'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'

    def update(self):
        self.execute(None)
        user = get_current()
        objects = find_entities(
            user=user,
            interfaces=[IInvitation])
        batch = Batch(
            objects, self.request,
            default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_invitations"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(CONTENTS_MESSAGES[index],
                       mapping={'nember': len_result})
        result_body, result = render_listing_objs(
            self.request, batch, user)

        values = {
            'bodies': result_body,
            'length': len_result,
            'batch': batch,
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeInvitations: SeeInvitationsView})
