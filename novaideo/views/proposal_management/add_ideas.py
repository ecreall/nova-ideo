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

from novaideo.content.processes.proposal_management.behaviors import  AddIdeas
from novaideo.content.correlation import CorrelationSchema, Correlation
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.core import can_access


addideas_message = {'0': u"""Pas d'idées utilisées""",
                   '1': u"""Voir l'idée utilisée""",
                   '*': u"""Voir les {len_ideas} idées utilisées"""}


@colander.deferred
def targets_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    root = getSite()
    user = get_current()
    values = []
    entities = [idea for idea in root.ideas if can_access(user, idea) and not (idea in context.related_ideas)]
    values = [(i, i.title) for i in entities]
    values = sorted(values, key=lambda p: p[1])
    return Select2Widget(values=values, multiple=True)


class RelatedIdeasView(BasicView):
    title = _('Related ideas')
    name = 'relatedideas'
    template = 'novaideo:views/idea_management/templates/related_contents.pt'
    item_template = 'pontus:templates/subview_sample.pt'
    viewid = 'relatedideas'


    def update(self):
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


class AddIdeasFormView(FormView):

    title = _('Add ideas')
    schema = select(CorrelationSchema(),['targets', 'intention', 'comment'])
    behaviors = [AddIdeas]
    formid = 'formaddtoideas'
    name='formaddtoideas'

    def before_update(self):
        target = self.schema.get('targets')
        target.widget = targets_choice
        target.title = _("Related ideas")


@view_config(
    name='addideas',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class AddIdeasView(MultipleView):
    title = _('Add ideas')
    name = 'addideas'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    views = (AddIdeasFormView, RelatedIdeasView)

    def get_message(self):
        user = get_current()
        related_ideas = [idea for idea in self.context.related_ideas if can_access(user, idea)]
        len_ideas = len(related_ideas)
        index = str(len_ideas)
        if len_ideas>1:
            index = '*'

        message = addideas_message[index].format(len_ideas=len_ideas)
        return message


DEFAULTMAPPING_ACTIONS_VIEWS.update({AddIdeas:AddIdeasView})
