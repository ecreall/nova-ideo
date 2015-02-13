# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
from pyramid.view import view_config

from substanced.util import Batch

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView

from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeMyContents)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.content.processes import get_states_mapping
from novaideo.core import BATCH_DEFAULT_SIZE



MY_CONTENTS_MESSAGES = {
        '0': _(u"""Aucun contenus auxquels j'ai contribué"""),
        '1': _(u"""Un contenu auquel j'ai contribué"""),
        '*': _(u"""${nember} contenus auxquels j'ai contribué""")
                        }


@view_config(
    name='seemycontents',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeMyContentsView(BasicView):
    title = _('My contents')
    name = 'seemycontents'
    behaviors = [SeeMyContents]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seemycontents'

    def update(self):
        self.execute(None)
        user = get_current()
        objects = self.objects
        batch = Batch(objects, self.request, default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_contents"
        len_result = batch.seqlen
        result_body = []
        for obj in batch:
            render_dict = {'object': obj, 
                           'current_user': user, 
                           'state': get_states_mapping(user, obj, 
                                   getattr(obj, 'state', [None])[0])}
            body = self.content(result=render_dict, 
                                template=obj.result_template)['body']
            result_body.append(body)

        result = {}
        values = {
                'bodies': result_body,
                'length': len_result,
                'batch': batch,
                'add_message': False
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result

    def before_update(self):
        user = get_current()
        objects = [o for o in getattr(user, 'contents', [])]
        objects = sorted(objects, 
                         key=lambda e: getattr(e, 'modified_at', 
                                               datetime.datetime.today()),
                         reverse=True)
        self.objects = objects
        len_contents = len(objects)
        index = str(len_contents)
        if len_contents > 1:
            index = '*'

        self.title = _(MY_CONTENTS_MESSAGES[index], 
                       mapping={'nember': len_contents})


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeMyContents:SeeMyContentsView})