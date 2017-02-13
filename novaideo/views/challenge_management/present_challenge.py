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

from novaideo.content.processes.challenge_management.behaviors import (
    PresentChallenge, PresentChallengeAnonymous)
from novaideo.content.challenge import Challenge
from novaideo import _
from novaideo.views.idea_management.present_idea import (
    PresentIdeaView,
    PresentIdeaSchema,
    SentToView as IdeaSentToView)
from novaideo.utilities.alerts_utility import get_user_data, get_entity_data
from novaideo.views.core import ActionAnonymousView


class SentToView(IdeaSentToView):
    validators = [PresentChallenge.get_validator()]


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
    email_data = get_user_data(get_current(request), 'my', request)
    email_data.update(get_entity_data(context, 'subject', request))
    return mail_template['template'].format(
        recipient_title='',
        recipient_first_name='',
        recipient_last_name='',
        novaideo_title=request.root.title,
        **email_data
    )


class PresentChallengeSchema(PresentIdeaSchema):

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


class PresentChallengeFormView(FormView):

    title = _('Transmit the challenge to others')
    schema = select(PresentChallengeSchema(),
                    ['members', 'subject', 'message', 'send_to_me'])
    behaviors = [PresentChallenge]
    formid = 'formpresentchallengeform'
    name = 'presentchallengeform'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': PresentChallenge.node_definition.id})
        formwidget = deform.widget.FormWidget(css_class='presentform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget

    def bind(self):
        root = self.request.root
        mail_template = root.get_mail_template('presentation_challenge')
        return {'mail_template': mail_template}


@view_config(
    name='present',
    context=Challenge,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PresentChallengeView(PresentIdeaView):
    title = _('Transmit the challenge to others')
    description = _('Transmit the challenge to others')
    name = 'present'
    views = (SentToView, PresentChallengeFormView)

    def before_update(self):
        self.viewid = 'present'
        super(PresentChallengeView, self).before_update()


@view_config(
    name='presentanonymous',
    context=Challenge,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PresentChallengeAnonymousView(ActionAnonymousView):
    behaviors = [PresentChallengeAnonymous]
    name = 'presentanonymous'


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {PresentChallengeAnonymous: PresentChallengeAnonymousView})


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {PresentChallenge: PresentChallengeView})
