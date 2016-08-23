# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.\
    newsletter_management.behaviors import (
        SendNewsletter)
from novaideo.content.newsletter import Newsletter
from novaideo import _


@view_config(
    name='sendnewsletter',
    context=Newsletter,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SendNewsletterView(BasicView):
    title = _('Send newsletter')
    name = 'sendnewsletter'
    behaviors = [SendNewsletter]
    viewid = 'sendnewsletter'

    def update(self):
        results = self.execute(None)
        return results[0]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SendNewsletter: SendNewsletterView})
