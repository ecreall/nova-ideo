# -*- coding: utf8 -*-
# Copyright (c) 2016 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid import renderers

from substanced.util import Batch

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView

from novaideo.core import can_access
from novaideo.content.processes.idea_management.behaviors import (
    SeeRelatedWorkingGroups)
from novaideo.content.idea import Idea
from novaideo.utilities.util import render_small_listing_objs
from novaideo import _

BATCH_DEFAULT_SIZE = 30

WG_MESSAGES = {'0': _(u"""Pas de groupes de travail liés"""),
                     '1': _(u"""Groupe de travail lié"""),
                     '*': _(u"""Groupes de travail liés""")}


@view_config(
    name='relatedworkinggroups',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeRelatedWorkingGroupsView(BasicView):
    title = _('Working groups')
    description = _('See related working groups')
    name = 'relatedworkinggroups'
    behaviors = [SeeRelatedWorkingGroups]
    template = 'novaideo:views/novaideo_view_manager/templates/home.pt'
    wrapper_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    viewid = 'relatedworkinggroups'
    contextual_help = 'related-wg-help'

    def update(self):
        self.execute(None)
        user = get_current()
        objects = [proposal for proposal
                   in dict(self.context.related_proposals).keys()
                   if proposal.working_group and 'archived' not in proposal.state
                   and can_access(user, proposal)]
        objects = sorted(
            objects,
            key=lambda e: getattr(e, 'modified_at'),
            reverse=True)
        url = self.request.resource_url(self.context, self.name)
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_idea_working_groups"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        result_body = render_small_listing_objs(
            self.request, batch, user)
        result = {}
        self.title = _(WG_MESSAGES[index], mapping={'nember': len_result})
        message = (_(WG_MESSAGES[index]),
                   len_result,
                   index)
        self.message = message
        values = {
            'bodies': result_body,
            'batch': batch,
            'message': message,
            'empty_message': _("No working groups created"),
            'empty_icon': 'novaideo-icon icon-wg'
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result

    def get_message(self):
        return self.message


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeRelatedWorkingGroups: SeeRelatedWorkingGroupsView})
