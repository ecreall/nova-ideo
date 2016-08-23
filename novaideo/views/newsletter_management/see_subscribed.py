# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.\
    newsletter_management.behaviors import (
        SeeSubscribed)
from novaideo.content.newsletter import Newsletter
from novaideo import _


@view_config(
    name='seenewslettersubscribed',
    context=Newsletter,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeSubscribedView(BasicView):
    title = _('Subscribed users')
    name = 'seenewslettersubscribed'
    behaviors = [SeeSubscribed]
    template = 'novaideo:views/newsletter_management/templates/see_subscribed.pt'
    viewid = 'seenewslettersubscribed'

    def update(self):
        self.execute(None)
        result = {}
        values = {'subscribed': self.context.subscribed}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeSubscribed: SeeSubscribedView})
