#-*- coding: utf-8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import pytz
import datetime
from pyramid.view import view_config

from substanced.util import Batch

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView

from novaideo.utilities.util import render_listing_objs
from novaideo.content.processes.proposal_management.behaviors import (
    SeeAmendments)
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.core import can_access


BATCH_DEFAULT_SIZE = 8

AMENDMENTS_MESSAGES = {
    '0': _(u"""No amended version"""),
    '1': _(u"""One amended version"""),
    '*': _(u"""${nember} amended versions""")}


@view_config(
    name='seeproposalamendments',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeAmendmentsView(BasicView):
    name = 'seeproposalamendments'
    viewid = 'seeproposalamendments'
    behaviors = [SeeAmendments]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    view_icon = 'novaideo-icon icon-amendment'
    contextual_help = 'amendments-help'
    title = _('See amended versions')
    description = _("See amended versions")

    def update(self):
        self.execute(None)
        user = get_current()
        objects = [o for o in getattr(self.context, 'amendments', [])
                   if not('archived' in o.state) and can_access(user, o)]
        now = datetime.datetime.now(tz=pytz.UTC)
        objects = sorted(objects,
                         key=lambda e: getattr(e, 'modified_at', now),
                         reverse=True)
        url = self.request.resource_url(self.context, self.name)
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_proposalamendments"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(AMENDMENTS_MESSAGES[index],
                       mapping={'nember': len_result})
        result_body, result = render_listing_objs(
            self.request, batch, user)
        values = {
            'bodies': result_body,
            'batch': batch
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeAmendments: SeeAmendmentsView})
