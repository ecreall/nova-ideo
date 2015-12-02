# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import Batch, get_oid

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView

from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeMyContents)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.content.processes import get_states_mapping
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.views.filter import (
    get_filter, FILTER_SOURCES, merge_with_filter_view, find_entities)


CONTENTS_MESSAGES = {
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
    contents_messages = CONTENTS_MESSAGES
    selected_filter = ['metadata_filter', 'temporal_filter',
                     'text_filter', 'other_filter']

    def _get_title(self, **args):
        return _(self.contents_messages[args.get('index')],
                       mapping={'nember': args.get('len_result')})

    def _add_filter(self, user):
        def source(**args):
            objects = find_entities(
                user=user,
                intersect=self._get_content_ids(), **args)
            return objects

        url = self.request.resource_url(self.context,
                                       '@@novaideoapi')
        return get_filter(
            self, url=url,
            select=self.selected_filter,
            source=source)

    def _get_content_ids(self):
        user = get_current()
        return [get_oid(o) for o in getattr(user, 'contents', [])]

    def update(self):
        self.execute(None)
        user = get_current()
        filter_form, filter_data = self._add_filter(user)
        args = merge_with_filter_view(self, {})
        args['request'] = self.request
        objects = find_entities(user=user, intersect=self._get_content_ids(),
                                sort_on='release_date', reverse=True,
                                **args)
        url = self.request.resource_url(self.context, self.name)
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_contents"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = self._get_title(
            index=index, len_result=len_result, user=user)
        filter_data['filter_message'] = self.title
        filter_body = self.filter_instance.get_body(filter_data)
        result_body = []
        for obj in batch:
            render_dict = {'object': obj,
                           'current_user': user,
                           'state': get_states_mapping(user, obj,
                                   getattr(obj, 'state_or_none', [None])[0])}
            body = self.content(args=render_dict,
                                template=obj.templates['default'])['body']
            result_body.append(body)

        result = {}
        values = {'bodies': result_body,
                  'batch': batch,
                  'filter_body': filter_body}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        result['css_links'] = filter_form['css_links']
        result['js_links'] = filter_form['js_links']
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeMyContents: SeeMyContentsView})


FILTER_SOURCES.update(
    {SeeMyContentsView.name: SeeMyContentsView})
