# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import Batch

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView

from novaideo.core import can_access
from novaideo.content.processes.proposal_management.behaviors import (
    SeeRelatedIdeas)
from novaideo.content.proposal import Proposal
from novaideo.utilities.util import (
    render_listing_objs, render_small_listing_objs)
from novaideo import _

BATCH_DEFAULT_SIZE = 8

ADDIDEAS_MESSAGES = {
    '0': _(u"""No related ideas"""),
    '1': _(u"""One related idea"""),
    '*': _(u"""${nember} related ideas""")}


@view_config(
    name='addideas',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeRelatedIdeasView(BasicView):
    name = 'relatedideas'
    viewid = 'relatedideas'
    behaviors = [SeeRelatedIdeas]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    view_icon = 'novaideo-icon icon-idea'
    contextual_help = 'related-ideas-help'
    title = _('See the related ideas')
    description = _('See the related ideas')

    def update(self):
        self.execute(None)
        user = get_current()
        objects = [content for content in
                   self.context.related_ideas
                   if can_access(user, content)]
        objects = sorted(
            objects,
            key=lambda e: getattr(e, 'modified_at'),
            reverse=True)
        url = self.request.resource_url(self.context, self.name)
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_related_ideas" + str(self.context.__oid__)
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'
        result = {}
        # if included in another view
        if self.parent or self.request.view_name == self.name:
            result_body, result = render_listing_objs(
                self.request, batch, user)
        else:
            result_body = render_small_listing_objs(
                self.request, batch, user)

        self.title = _(ADDIDEAS_MESSAGES[index],
                       mapping={'nember': len_result})
        values = {
            'bodies': result_body,
            'batch': batch
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeRelatedIdeas: SeeRelatedIdeasView})
