# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import Batch

from dace.util import getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.user_management.behaviors import (
    SeeRegistrations)
from novaideo.content.novaideo_application import (
    NovaIdeoApplication)
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo import _


CONTENTS_MESSAGES = {
        '0': _(u"""No registration found"""),
        '1': _(u"""One registration found"""),
        '*': _(u"""${nember} registrations found""")
        }


@view_config(
    name='seeregistrations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeRegistrationsView(BasicView):
    title = _('Registrations')
    name = 'seeregistrations'
    behaviors = [SeeRegistrations]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seeregistrations'

    def update(self):
        self.execute(None)
        root = getSite()
        objects = root.preregistrations
        objects.reverse()
        batch = Batch(objects, self.request, default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_registrations"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(CONTENTS_MESSAGES[index],
                       mapping={'nember': len_result})
        result_body = []
        for obj in batch:
            object_values = {'object': obj}
            body = self.content(args=object_values,
                                template=obj.templates['default'])['body']
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

DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeRegistrations: SeeRegistrationsView})
