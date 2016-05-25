# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.proposal_management.behaviors import (
    PresentProposal)
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.views.idea_management.present_idea import (
    PresentIdeaView,
    PresentIdeaSchema,
    SentToView as IdeaSentToView)


class SentToView(IdeaSentToView):
    validators = [PresentProposal.get_validator()]
    template = 'novaideo:views/proposal_management/templates/sent_to.pt'


@colander.deferred
def default_subject(node, kw):
    context = node.bindings['context']
    mail_template = node.bindings['mail_template']
    return mail_template['subject'].format(subject_title=context.title)


@colander.deferred
def default_message(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    mail_template = node.bindings['mail_template']
    localizer = request.localizer
    url = request.resource_url(context, "@@index")
    user = get_current()
    return mail_template['template'].format(
        recipient_title='',
        recipient_first_name='',
        recipient_last_name='',
        subject_url=url,
        subject_title=getattr(context, 'title', context.name),
        my_title=localizer.translate(_(getattr(user, 'user_title', ''))),
        my_first_name=getattr(user, 'first_name', user.name),
        my_last_name=getattr(user, 'last_name', ''),
        novaideo_title=request.root.title
    )


class PresentProposalSchema(PresentIdeaSchema):

    subject = colander.SchemaNode(
        colander.String(),
        default=default_subject,
        title=_('Subject'),
        )

    message = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        default=default_message,
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        )


class PresentProposalFormView(FormView):

    title = _('Submit the proposal to others')
    schema = select(PresentProposalSchema(),
                    ['members', 'subject', 'message', 'send_to_me'])
    behaviors = [PresentProposal]
    formid = 'formpresentproposalform'
    name = 'presentproposalform'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi', query={'op': 'present_entity'})
        formwidget = deform.widget.FormWidget(css_class='presentform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget

    def bind(self):
        root = self.request.root
        mail_template = root.get_mail_template('presentation_proposal')
        return {'mail_template': mail_template}


@view_config(
    name='present',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PresentProposalView(PresentIdeaView):
    title = _('Submit the proposal to others')
    description = _('Submit the proposal to others')
    name = 'present'
    views = (SentToView, PresentProposalFormView)

    def before_update(self):
        self.viewid = 'present'
        super(PresentProposalView, self).before_update()


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {PresentProposal: PresentProposalView})
