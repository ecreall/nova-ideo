# -*- coding: utf8 -*-
# Copyright (c) 2016 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import Batch

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView

from novaideo.core import can_access
from novaideo.content.processes.idea_management.behaviors import (
    SeeRelatedWorkingGroups)
from novaideo.content.idea import Idea
from novaideo.utilities.util import (
    render_small_listing_objs, render_listing_objs)
from novaideo import _

BATCH_DEFAULT_SIZE = 8

WG_MESSAGES = {
    '0': _(u"""No related working group"""),
    '1': _(u"""One related working group"""),
    '*': _(u"""${nember} related working groups""")}


@view_config(
    name='relatedworkinggroups',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeRelatedWorkingGroupsView(BasicView):
    name = 'relatedworkinggroups'
    viewid = 'relatedworkinggroups'
    behaviors = [SeeRelatedWorkingGroups]
    template = 'novaideo:views/novaideo_view_manager/templates/home.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    view_icon = 'icon icon novaideo-icon icon-wg'
    contextual_help = 'related-wg-help'
    title = _('The working groups')
    description = _('See the related working groups')

    def update(self):
        self.execute(None)
        user = get_current()
        objects = [proposal for proposal
                   in self.context.related_proposals
                   if proposal.working_group and
                   'archived' not in proposal.state and
                   'censored' not in proposal.state and
                   can_access(user, proposal)]
        objects = sorted(
            objects,
            key=lambda e: getattr(e, 'modified_at'),
            reverse=True)
        url = self.request.resource_url(self.context, self.name)
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_idea_working_groups" + str(self.context.__oid__)
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(WG_MESSAGES[index], mapping={'nember': len_result})
        result = {}
        # if included in another view
        if self.parent or self.request.view_name == self.name:
            result_body, result = render_listing_objs(
                self.request, batch, user)
        else:
            result_body = render_small_listing_objs(
                self.request, batch, user)

        values = {
            'bodies': result_body,
            'batch': batch,
            'empty_message': _("No working group created"),
            'empty_icon': 'novaideo-icon icon-wg'
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeRelatedWorkingGroups: SeeRelatedWorkingGroupsView})
