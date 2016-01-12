# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.advertising_management.behaviors import (
    EditWebAdvertising)
from novaideo.content.web_advertising import (
    WebAdvertisingSchema, WebAdvertising)
from novaideo import _


@view_config(
    name='editwebadvertising',
    context=WebAdvertising,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditWebAdvertisingView(FormView):

    title = _('Edit the announcement')
    schema = select(WebAdvertisingSchema(factory=WebAdvertising,
                                         editable=True),
                    ['title', 'visibility_dates',
                     'picture', 'html_content', 'advertisting_url',
                     'positions'])
    behaviors = [EditWebAdvertising, Cancel]
    formid = 'formeditwebadvertising'
    name = 'editwebadvertising'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/advertisting_management.js']}

    def default_data(self):
        return self.context

DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {EditWebAdvertising: EditWebAdvertisingView})
