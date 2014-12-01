# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
# -*- coding: utf8 -*-
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView

from novaideo.content.processes.proposal_management.behaviors import (
    SeeRelatedIdeas)
from novaideo.content.correlation import CorrelationType
from novaideo.content.proposal import Proposal
from novaideo import _


ADDIDEAS_MESSAGES = {'0': _(u"""Pas d'idées utilisées"""),
                   '1': _(u"""Une idée utilisée"""),
                   '*': _(u"""Idées utilisées""")}

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
    template = 'novaideo:views/idea_management/templates/related_contents.pt'
    wrapper_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    viewid = 'relatedideas'


    def update(self):
        self.execute(None)
        user = get_current()
        relatedideas = [{'content':target, 
                          'url':target.url(self.request),
                          'correlation': correlation} \
                        for target, correlation in \
                         self.context.related_ideas.items()]
        len_ideas = len(relatedideas)

        index = str(len_ideas)
        if len_ideas > 1:
            index = '*'

        message = (_(ADDIDEAS_MESSAGES[index]),
                   len_ideas,
                   index)
        result = {}
        values = {
                'relatedcontents': relatedideas,
                'current_user': user,
                'message': message
               }
        self.message = message
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result

    def get_message(self):
        return self.message


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeRelatedIdeas:SeeRelatedIdeasView})
