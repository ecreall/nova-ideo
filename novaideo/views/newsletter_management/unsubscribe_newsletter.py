# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.default_behavior import Cancel
from pontus.schema import select, Schema

from novaideo.content.processes.\
    newsletter_management.behaviors import (
        UnsubscribeNewsletter)
from novaideo.content.newsletter import Newsletter
from novaideo import _
from novaideo.content.person import EmailInputWidget


@colander.deferred
def email_validator(node, kw):
    context = node.bindings['context']
    if kw not in context.subscribed:
        raise colander.Invalid(node,
            _('User (${email}) not subscribed',
            mapping={'email': kw}))


class UnsubscribeSchema(Schema):

    email = colander.SchemaNode(
        colander.String(),
        widget=EmailInputWidget(),
        validator=colander.All(
            colander.Email(),
            email_validator,
            colander.Length(max=100)
            ),
        title=_('Email')
        )


@view_config(
    name='unsubscribenewsletter',
    context=Newsletter,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class UnsubscribeNewsletterView(FormView):

    title = _('Unsubscribe')
    schema = select(UnsubscribeSchema(),
                    ['email'])
    behaviors = [UnsubscribeNewsletter, Cancel]
    formid = 'formunsubscribenewsletter'
    name = 'unsubscribenewsletter'


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {UnsubscribeNewsletter: UnsubscribeNewsletterView})
