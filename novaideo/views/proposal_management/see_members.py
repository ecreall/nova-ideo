#-*- coding: utf-8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import pytz
import datetime
from pyramid.view import view_config
from pyramid import renderers

from substanced.util import Batch

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView

from novaideo.content.processes.proposal_management.behaviors import (
    SeeMembers)
from novaideo.content.proposal import Proposal
from novaideo.utilities.util import render_small_listing_objs
from novaideo import _


BATCH_DEFAULT_SIZE = 30

MEMBERS_MESSAGES = {
    '0': _(u"""No member"""),
    '1': _(u"""One member"""),
    '*': _(u"""${nember} members""")
}


@view_config(
    name='seeproposalmembers',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeMembersView(BasicView):
    title = _('Members')
    name = 'seeproposalmembers'
    description = _("See members")
    behaviors = [SeeMembers]
    template = 'novaideo:views/novaideo_view_manager/templates/home.pt'
    viewid = 'seeproposalmembers'

    def update(self):
        self.execute(None)
        user = get_current()
        objects = getattr(self.context.working_group, 'members', [])
        url = self.request.resource_url(self.context, self.name)
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_proposal_members" + str(self.context.__oid__)
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        result_body = render_small_listing_objs(
            self.request, batch, user)
        result = {}
        self.title = _(MEMBERS_MESSAGES[index], mapping={'nember': len_result})
        values = {
            'bodies': result_body,
            'batch': batch,
            'empty_message': _("No members"),
            'empty_icon': 'glyphicon glyphicon-user'
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
  {SeeMembers: SeeMembersView})
