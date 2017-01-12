# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
import datetime
import pytz
from pyramid.view import view_config

from substanced.util import Batch

from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import (
    DEFAULTMAPPING_ACTIONS_VIEWS)

from pontus.view import BasicView

from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeAlerts)
from novaideo import _


BATCH_DEFAULT_SIZE = 30

CONTENTS_MESSAGES = {
    '0': _(u"""You have no new alert"""),
    '1': _(u"""You have one new alert"""),
    '*': _(u"""You have ${nember} new alerts""")
    }


@view_config(
    name='seealerts',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeAlertsView(BasicView):
    title = _('The notifications')
    name = 'seealerts'
    behaviors = [SeeAlerts]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seealerts'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'

    def update(self):
        user = get_current()
        objects = list(getattr(user, 'alerts', []))
        len_result = len(objects)
        objects.extend(getattr(user, 'old_alerts', []))
        now = datetime.datetime.now(tz=pytz.UTC)
        objects = sorted(
            objects,
            key=lambda e: getattr(e, 'modified_at', now),
            reverse=True)
        url = self.request.resource_url(self.context, self.name)
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_alerts"
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(CONTENTS_MESSAGES[index],
                       mapping={'nember': len_result})
        result_body = []
        for obj in batch:
            render_dict = {
                'object': obj,
                'current_user': user
            }
            body = self.content(args=render_dict,
                                template=obj.templates['default'])['body']
            result_body.append(body)

        result = {}
        values = {'bodies': result_body,
                  'batch': batch}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        self.execute(None)
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeAlerts: SeeAlertsView})
