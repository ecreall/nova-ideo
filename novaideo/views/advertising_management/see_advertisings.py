# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
from pyramid.view import view_config

from substanced.util import Batch

from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.advertising_management.behaviors import (
    SeeAdvertisings)
from novaideo.content.processes import get_states_mapping
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo import _


CONTENTS_MESSAGES = {
    '0': _(u"""No announcement found"""),
    '1': _(u"""One announcement found"""),
    '*': _(u"""${nember} announcements found""")
    }


@view_config(
    name='seeadvertisings',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeAdvertisingsView(BasicView):
    title = _('The announcements')
    name = 'seeadvertisings'
    behaviors = [SeeAdvertisings]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seeadvertisings'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'

    def update(self):
        self.execute(None)
        user = get_current()
        objects = self.context.advertisings
        now = datetime.datetime.now(tz=pytz.UTC)
        objects = sorted(objects,
                         key=lambda e: getattr(e, 'modified_at', now),
                         reverse=True)
        batch = Batch(objects, self.request, default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_advertisings"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(CONTENTS_MESSAGES[index],
                       mapping={'nember': len_result})
        result_body = []
        for obj in batch:
            object_values = {'object': obj,
                             'current_user': user,
                             'state': get_states_mapping(user, obj,
                                   getattr(obj, 'state_or_none', [None])[0])}
            body = self.content(args=object_values,
                                template=obj.templates.get('default'))['body']
            result_body.append(body)

        result = {}
        values = {
            'bodies': result_body,
            'length': len_result,
            'batch': batch,
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeAdvertisings: SeeAdvertisingsView})
