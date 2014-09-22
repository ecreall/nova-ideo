# -*- coding: utf8 -*-
import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import find_entities, getSite
from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.widget import Select2Widget
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.proposal_management.behaviors import  SeeRelatedIdeas
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.core import can_access


addideas_message = {'0': u"""Pas d'idées utilisées""",
                   '1': u"""Voir l'idée utilisée""",
                   '*': u"""Voir les {len_ideas} idées utilisées"""}

@view_config(
    name='addideas',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class SeeRelatedIdeasView(BasicView):
    title = _('Related ideas')
    name = 'relatedideas'
    behaviors = [SeeRelatedIdeas]
    template = 'novaideo:views/idea_management/templates/related_contents.pt'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    viewid = 'relatedideas'


    def update(self):
        self.execute(None)
        root = getSite()
        user = get_current()
        correlations = [c for c in self.context.source_correlations if ((c.type==1) and ('related_ideas' in c.tags) and can_access(user, c))]
        related_ideas = [target for targets in correlations for target in targets]
        relatedideas = []
        len_ideas = 0       
        for c in correlations:
            targets = c.targets
            len_ideas += len(targets)
            for target in targets:
                relatedideas.append({'content':target, 'url':target.url(self.request), 'correlation': c})

        index = str(len_ideas)
        if len_ideas>1:
            index = '*'

        message = addideas_message[index].format(len_ideas=len_ideas)
        result = {}
        values = {
                'relatedcontents': relatedideas,
                'current_user': user,
                'message': message
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result

    def get_message(self):
        user = get_current()
        related_ideas = [idea for idea in self.context.related_ideas if can_access(user, idea)]
        len_ideas = len(related_ideas)
        index = str(len_ideas)
        if len_ideas>1:
            index = '*'

        message = addideas_message[index].format(len_ideas=len_ideas)
        return message


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeRelatedIdeas:SeeRelatedIdeasView})
