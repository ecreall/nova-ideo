# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import (
    DEFAULTMAPPING_ACTIONS_VIEWS)

from pontus.view import BasicView

from novaideo.content.processes.\
    newsletter_management.behaviors import (
        SeeNewsletterHistory)
from novaideo.content.newsletter import Newsletter
from novaideo import _


@view_config(
    name='seenewsletterhistory',
    context=Newsletter,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeNewsletterHistoryView(BasicView):
    title = _('Content history')
    name = 'seenewsletterhistory'
    behaviors = [SeeNewsletterHistory]
    template = 'novaideo:views/newsletter_management/templates/newsletter_history.pt'
    viewid = 'seenewsletterhistory'

    def update(self):
        self.execute(None)
        result = {}
        history = getattr(self.context, 'annotations', {}).get(
            'newsletter_history', [])
        values = {'context': self.context,
                  'history': history,
                  }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeNewsletterHistory: SeeNewsletterHistoryView})
