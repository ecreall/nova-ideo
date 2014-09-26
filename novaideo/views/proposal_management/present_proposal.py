# -*- coding: utf8 -*-
import colander
import deform
from pyramid.view import view_config
from substanced.util import find_service

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite
from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, Schema
from pontus.widget import Select2WidgetCreateSearchChoice
from pontus.view_operation import MultipleView
from pontus.view import BasicView

from novaideo.content.processes.proposal_management.behaviors import  PresentProposal
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.mail import PRESENTATION_PROPOSAL_MESSAGE, PRESENTATION_PROPOSAL_SUBJECT
from novaideo.views.idea_management.present_idea import PresentIdeaView, PresentIdeaSchema, SentToView as IdeaSentToView


class SentToView(IdeaSentToView):
    validators = [PresentProposal.get_validator()]
    template = 'novaideo:views/proposal_management/templates/sent_to.pt'


class PresentProposalSchema(PresentIdeaSchema):

    subject =  colander.SchemaNode(
        colander.String(),
        default=PRESENTATION_PROPOSAL_SUBJECT,
        title=_('Subject'),
        )

    message = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        default=PRESENTATION_PROPOSAL_MESSAGE,
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        )


class PresentProposalFormView(FormView):

    title = _('Present proposal')
    schema = select(PresentProposalSchema(), ['members', 'subject', 'message', 'send_to_me'])
    behaviors = [PresentProposal]
    formid = 'formpresentproposalform'
    name='presentproposalform'

    def before_update(self):
        formwidget = deform.widget.FormWidget(css_class='associate-form', 
                                              activable=True,
                                              button_css_class="pull-right",
                                              picto_css_class="glyphicon glyphicon-envelope",
                                              button_title="Present")
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='presentproposal',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class PresentProposalView(PresentIdeaView):
    title = _('Present the proposal')
    description = _('Present the proposal')
    name='presentproposal'
    views = (SentToView, PresentProposalFormView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({PresentProposal:PresentProposalView})
