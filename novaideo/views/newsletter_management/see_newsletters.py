# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import Batch

from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.utilities.util import render_listing_objs
from novaideo.content.processes.\
    newsletter_management.behaviors import (
        SeeNewsletters)
from novaideo.content.novaideo_application import (
    NovaIdeoApplication)
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo import _


CONTENTS_MESSAGES = {
    '0': _(u"""No newsletter found"""),
    '1': _(u"""One newsletter found"""),
    '*': _(u"""${nember} newsletters found""")
    }


@view_config(
    name='seenewsletters',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeNewslettersView(BasicView):
    title = ''
    name = 'seenewsletters'
    behaviors = [SeeNewsletters]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seenewsletters'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'

    def update(self):
        self.execute(None)
        objects = self.context.newsletters
        batch = Batch(objects, self.request, default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_newsletters"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(CONTENTS_MESSAGES[index],
                       mapping={'nember': len_result})

        user = get_current()
        result_body, result = render_listing_objs(
            self.request, batch, user)

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
    {SeeNewsletters: SeeNewslettersView})
