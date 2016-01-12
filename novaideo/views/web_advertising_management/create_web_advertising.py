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
    CreateWebAdvertising)
from novaideo.content.web_advertising import (
    WebAdvertisingSchema, WebAdvertising)
from novaideo.content.novaideo_application import (
    NovaIdeoApplication)
from novaideo import _


@view_config(
    name='createwebadvertising',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CreateWebAdvertisingView(FormView):

    title = _('Create an announcement')
    schema = select(WebAdvertisingSchema(factory=WebAdvertising,
                                         editable=True),
                    ['title', 'visibility_dates',
                     'picture', 'html_content', 'advertisting_url',
                     'positions'])
    behaviors = [CreateWebAdvertising, Cancel]
    formid = 'formcreatewebadvertising'
    name = 'createwebadvertising'
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/advertisting_management.js']}


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CreateWebAdvertising: CreateWebAdvertisingView})
