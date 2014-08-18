# -*- coding: utf8 -*-
import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import find_entities
from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.widget import Select2Widget
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.idea_management.behaviors import  AddToProposals
from novaideo.content.correlation import CorrelationSchema, Correlation
from novaideo.content.idea import Idea
from novaideo.content.interface import IProposal
from novaideo import _



@colander.deferred
def targets_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = []
    entities = getattr(get_current(), 'proposals', [])
    values = [(i, i.title) for i in entities]
    values = sorted(values, key=lambda p: p[1])
    return Select2Widget(values=values, multiple=True)


class RelatedProposalsView(BasicView):
    title = _('Related proposals')
    name = 'relatedproposals'
    template = 'novaideo:views/idea_management/templates/related_contents.pt'
    item_template = 'pontus:templates/subview_sample.pt'
    viewid = 'relatedproposals'


    def update(self):
        user = get_current()
        correlations = [c for c in self.context.source_correlations if ((c.type==1) and ('related_proposals' in c.tags))] # TODO (if c.source.actions) replace by an other test
        relatedproposals = []
        for c in correlations:
            proposals = c.targets
            for proposal in proposals:
                relatedproposals.append({'content':proposal, 'url':proposal.url(self.request), 'correlation': c})

        len_proposals = len(relatedproposals)
        message = ''
        if len_proposals>1:
            message = u"""Voir les {len} propositions utilisant l'idée""".format(len=len_proposals)
        elif len_proposals == 0:
            message = u"""Pas de propositions utilisant l'idée"""
        else:   
            message = u"""Voir la proposition utilisant l'idée"""

        result = {}
        values = {
                'relatedcontents': relatedproposals,
                'current_user': user,
                'message': message
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class AddToProposalsFormView(FormView):

    title = _('Add to proposals form')
    schema = select(CorrelationSchema(),['targets', 'intention', 'comment'])
    behaviors = [AddToProposals]
    formid = 'formaddtoproposals'
    name='formaddtoproposals'

    def before_update(self):
        target = self.schema.get('targets')
        target.widget = targets_choice
        target.title = _("Related proposals")


@view_config(
    name='addtoproposals',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class AddToProposalsView(MultipleView):
    title = _('Add to proposals')
    name = 'addtoproposals'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    views = (AddToProposalsFormView, RelatedProposalsView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({AddToProposals:AddToProposalsView})
