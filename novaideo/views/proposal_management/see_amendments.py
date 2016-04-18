#-*- coding: utf-8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import pytz
import datetime
from pyramid.view import view_config


from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView

from novaideo.content.processes.proposal_management.behaviors import (
    SeeAmendments)
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.content.processes import get_states_mapping
from novaideo.core import can_access



AMENDMENTS_MESSAGES = {'0': _(u"""No amended version"""),
                      '1': _(u"""Amended version"""),
                      '*': _(u"""Amended versions""")}


@view_config(
    name='editamendments',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeAmendmentsView(BasicView):
    title = _('See amended versions')
    name = 'editamendments'
    description = _("See amended versions")
    behaviors = [SeeAmendments]
    template = 'novaideo:views/proposal_management/templates/amendments.pt'
    wrapper_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    viewid = 'editamendments'
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
        lenamendments = len(objects)
        index = str(lenamendments)
        if lenamendments > 1:
            index = '*'

        message = (_(AMENDMENTS_MESSAGES[index]),
                   lenamendments,
                   index)

        result = {}
        values = {'amendments': objects,
                  'current_user': user,
                  'message': message,
                  'get_states_mapping': get_states_mapping
                   }
        self.message = message
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result

    def get_message(self):
        return self.message

    def before_update(self):
        self.viewid = 'editamendments'


DEFAULTMAPPING_ACTIONS_VIEWS.update(
  {SeeAmendments: SeeAmendmentsView})
