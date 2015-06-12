# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import Batch

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from dace.util import find_entities
from pontus.view import BasicView

from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeOrderedProposal)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.content.interface import IProposal
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.content.processes import get_states_mapping
from novaideo import _


CONTENTS_MESSAGES = {
        '0': _(u"""No proposal found"""),
        '1': _(u"""One proposal found"""),
        '*': _(u"""${nember} proposals found""")
        }


def sort_proposals(proposals):
    ordered_proposals = [(proposal, 
                          (len(proposal.tokens_support) - \
                           len(proposal.tokens_opposition))) \
                         for proposal in proposals]
    groups = {}
    for proposal in ordered_proposals:
        if groups.get(proposal[1], None):
            groups[proposal[1]].append(proposal)
        else:
            groups[proposal[1]] = [proposal]

    for group_key in list(groups.keys()):
        sub_proposals = list(groups[group_key]) 
        groups[group_key] = sorted(sub_proposals, 
                    key=lambda proposal: len(proposal[0].tokens_support), 
                    reverse=True)

    groups = sorted(groups.items(), key=lambda value: value[0], reverse=True)
    return [proposal[0] for sublist in groups \
           for proposal in sublist[1]]



@view_config(
    name='proposalstoexamine',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeOrderedProposalView(BasicView):
    title = _('Proposals to examine')
    name = 'proposalstoexamine'
    behaviors = [SeeOrderedProposal]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'proposalstoexamine'

    def update(self):
        self.execute(None) 
        user = get_current()
        objects = find_entities([IProposal], ['published'])
        objects = sort_proposals(objects)
        batch = Batch(objects, self.request, default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_participations"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(CONTENTS_MESSAGES[index] , 
                       mapping={'nember': len_result})
        result_body = []
        for obj in batch:
            object_values = {'object': obj, 
                           'current_user': user, 
                           'state': get_states_mapping(user, obj, 
                                   getattr(obj, 'state', [None])[0])}
            body = self.content(result=object_values, 
                                template=obj.result_template)['body']
            result_body.append(body)

        result = {}
        values = {
                'bodies': result_body,
                'length': len_result,
                'batch': batch,
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeOrderedProposal: SeeOrderedProposalView})
