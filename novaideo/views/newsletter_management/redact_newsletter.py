# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.default_behavior import Cancel
from pontus.schema import select
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.\
    newsletter_management.behaviors import (
        RedactNewsletter)
from novaideo.content.newsletter import (
    NewsletterSchema, Newsletter)
from novaideo import _


class RedactNewsletterViewStudyReport(BasicView):
    title = 'Explanation'
    name = 'redacteplanation'
    template = 'novaideo:views/newsletter_management/templates/redact_explanation.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class RedactFormNewsletterView(FormView):

    title = _('Write a newsletter')
    schema = select(NewsletterSchema(factory=Newsletter, editable=True),
                    ['subject', 'content'])
    behaviors = [RedactNewsletter, Cancel]
    formid = 'formredactnewsletter'
    name = 'redactnewsletterform'

    def default_data(self):
        return self.context


@view_config(
    name='redactnewsletter',
    context=Newsletter,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class RedactNewsletterView(MultipleView):
    title = _('Write a newsletter')
    name = 'redactnewsletter'
    viewid = 'redactnewsletter'
    template = 'daceui:templates/mergedmultipleview.pt'
    views = (RedactNewsletterViewStudyReport, RedactFormNewsletterView)
    validators = [RedactNewsletter.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {RedactNewsletter: RedactNewsletterView})
