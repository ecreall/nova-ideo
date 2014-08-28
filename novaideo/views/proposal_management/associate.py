# -*- coding: utf8 -*-
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view_operation import MultipleView
from pontus.form import  FormView
from pontus.schema import select

from novaideo.content.processes.proposal_management.behaviors import  Associate
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.views.idea_management.associate import RelatedContentsView, AssociateView as AssociateIdeaView
from novaideo.content.correlation import CorrelationSchema, Correlation

class AssociateFormView(FormView):

    title = _('Associate')
    schema = select(CorrelationSchema(factory=Correlation, editable=True),['targets', 'intention','comment'])
    behaviors = [Associate]
    formid = 'formassociate'
    name='associateform'

    def before_update(self):
        target = self.schema.get('targets')
        target.title = _("Related contents")


@view_config(
    name='associateproposal',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class AssociateView(AssociateIdeaView):
    views = (AssociateFormView, RelatedContentsView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({Associate:AssociateView})
