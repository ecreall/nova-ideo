# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.default_behavior import Cancel
from pontus.schema import select

from novaideo.content.processes.\
    newsletter_management.behaviors import (
        EditNewsletter)
from novaideo.content.newsletter import (
    NewsletterSchema, Newsletter)
from novaideo import _


@view_config(
    name='editnewsletter',
    context=Newsletter,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditNewsletterView(FormView):

    title = _('Edit a newsletter')
    schema = select(NewsletterSchema(factory=Newsletter, editable=True),
                    ['title', 'description', 'content_template'])
    behaviors = [EditNewsletter, Cancel]
    formid = 'formeditnewsletter'
    name = 'editnewsletter'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {EditNewsletter: EditNewsletterView})
