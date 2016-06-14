# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
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
from novaideo.content.processes.proposal_management.behaviors import (
    SeeRelatedIdeas)
from novaideo.content.proposal import Proposal
from novaideo.utilities.util import render_small_listing_objs
from novaideo import _

BATCH_DEFAULT_SIZE = 30

ADDIDEAS_MESSAGES = {'0': _(u"""Pas d'idées liées"""),
                     '1': _(u"""Idée liée"""),
                     '*': _(u"""Idées liées""")}


@view_config(
    name='addideas',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeRelatedIdeasView(BasicView):
    title = _('See related ideas')
    description = _('See related ideas')
    name = 'relatedideas'
    behaviors = [SeeRelatedIdeas]
    # template = 'novaideo:views/idea_management/templates/related_contents.pt'
    template = 'novaideo:views/novaideo_view_manager/templates/home.pt'
    wrapper_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    viewid = 'relatedideas'
    contextual_help = 'related-ideas-help'

    def update(self):
        self.execute(None)
        user = get_current()
        objects = [content for content, correlation in
                   self.context.related_ideas.items()
                   if can_access(user, content)]
        objects = sorted(
            objects,
            key=lambda e: getattr(e, 'modified_at'),
            reverse=True)
        url = self.request.resource_url(self.context, self.name)
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_related_ideas"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        result_body = render_small_listing_objs(
            self.request, batch, user)
        result = {}
        self.title = _(ADDIDEAS_MESSAGES[index], mapping={'nember': len_result})
        message = (_(ADDIDEAS_MESSAGES[index]),
                   len_result,
                   index)
        self.message = message
        values = {'bodies': result_body,
                  'batch': batch,
                  'message': message
                   }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result




        # self.execute(None)
        # user = get_current()
        # relatedideas = [{'content': target,
        #                  'url': target.url,
        #                  'correlation': correlation}
        #                 for target, correlation in
        #                 self.context.related_ideas.items()]
        # len_ideas = len(relatedideas)

        # index = str(len_ideas)
        # if len_ideas > 1:
        #     index = '*'

        # message = (_(ADDIDEAS_MESSAGES[index]),
        #            len_ideas,
        #            index)
        # result = {}
        # values = {
        #     'relatedcontents': relatedideas,
        #     'current_user': user,
        #     'message': message
        # }
        # self.message = message
        # body = self.content(args=values, template=self.template)['body']
        # item = self.adapt_item(body, self.viewid)
        # result['coordinates'] = {self.coordinates: [item]}
        # return result

    def get_message(self):
        return self.message


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeRelatedIdeas: SeeRelatedIdeasView})
