#-*- coding: utf-8 -*-
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



AMENDMENTS_MESSAGES = {'0': u"""Pas d'amendements""",
                      '1': u"""Un amendement proposé""",
                      '*': u"""{lenamendments} amendements proposés"""}


@view_config(
    name='editamendments',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class SeeAmendmentsView(BasicView):
    title = _('See amendments')
    name = 'editamendments'
    description = _("See amendments")
    behaviors = [SeeAmendments]
    template = 'novaideo:views/proposal_management/templates/amendments.pt'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    viewid = 'editamendments'


    def update(self):
        self.execute(None)
        user = get_current()
        objects = [o for o in getattr( self.context, 'amendments', []) \
                  if not('archived' in o.state) and can_access(user, o)]
        objects = sorted(objects, 
                         key=lambda e: getattr(e, 'modified_at', 
                                               datetime.datetime.today()), 
                         reverse=True)
        lenamendments = len(objects)
        index = str(lenamendments)
        if lenamendments > 1:
            index = '*'

        message = (AMENDMENTS_MESSAGES[index]).format(
                                    lenamendments=lenamendments)

        result = {}
        values = {'amendments': objects,
                  'current_user': user,
                  'message': message,
                  'get_states_mapping': get_states_mapping
                   }
        self.message = message
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result

    def get_message(self):
        return self.message


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeAmendments:SeeAmendmentsView})