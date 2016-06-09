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


BATCH_DEFAULT_SIZE = 10

AMENDMENTS_MESSAGES = {'0': _(u"""No amended version"""),
                      '1': _(u"""Amended version"""),
                      '*': _(u"""Amended versions""")}


@view_config(
    name='seeproposalamendments',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeAmendmentsView(BasicView):
    title = _('See amended versions')
    name = 'seeproposalamendments'
    description = _("See amended versions")
    behaviors = [SeeAmendments]
    template = 'novaideo:views/proposal_management/templates/amendments.pt'
    wrapper_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    viewid = 'seeproposalamendments'
    contextual_help = 'amendments-help'

    def update(self):
        self.execute(None)
        user = get_current()
        objects = [o for o in getattr(self.context, 'amendments', [])
                   if not('archived' in o.state) and can_access(user, o)]
        now = datetime.datetime.now(tz=pytz.UTC)
        objects = sorted(objects,
                         key=lambda e: getattr(e, 'modified_at', now),
                         reverse=True)
        # lenamendments = len(objects)
        # index = str(lenamendments)
        # if lenamendments > 1:
        #     index = '*'


        url = self.request.resource_url(self.context, self.name)
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_contents"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        # self.title = self._get_title(
        #     index=index, len_result=len_result, user=user)
        # filter_data['filter_message'] = self.title
        # filter_body = self.filter_instance.get_body(filter_data)
        result_body, result = render_listing_objs(
            self.request, batch, user)
        message = (_(AMENDMENTS_MESSAGES[index]),
                   len_result,
                   index)
        values = {'bodies': result_body,
                  'batch': batch,
                  'message': message
                   }
        self.message = message
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result

    def get_message(self):
        return self.message

    def before_update(self):
        self.viewid = 'seeproposalamendments'
        super(SeeAmendmentsView, self).before_update()


DEFAULTMAPPING_ACTIONS_VIEWS.update(
  {SeeAmendments: SeeAmendmentsView})
