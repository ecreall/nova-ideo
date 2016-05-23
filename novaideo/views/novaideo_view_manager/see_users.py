# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
import pytz
import datetime
from pyramid.view import view_config

from substanced.util import Batch

from dace.util import find_catalog
from dace.processinstance.core import (
    DEFAULTMAPPING_ACTIONS_VIEWS, Validator, ValidationError)
from dace.objectofcollaboration.principal.util import (
    get_current, has_role)
from pontus.view import BasicView
from pontus.util import merge_dicts

from novaideo.utilities.util import render_listing_objs
from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeUsers)
from novaideo.content.processes.system_process.behaviors import (
    find_users, INACTIVITY_DURATION)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.views.filter import (
    get_filter, FILTER_SOURCES, merge_with_filter_view, find_entities)


CONTENTS_MESSAGES = {
    '0': _(u"""Aucun membre"""),
    '1': _(u"""Un membre trouvé"""),
    '*': _(u"""${nember} membres trouvés""")
    }


@view_config(
    name='seeusers',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeUsersView(BasicView):
    title = _('Members')
    name = 'seeusers'
    behaviors = [SeeUsers]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result_users.pt'
    viewid = 'seeusers'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'
    contents_messages = CONTENTS_MESSAGES
    selected_filter = [('metadata_filter', ['neagtion', 'states', 'keywords']),
                       'temporal_filter',
                       'text_filter', 'other_filter']

    def _get_title(self, **args):
        return _(self.contents_messages[args.get('index')],
                 mapping={'nember': args.get('len_result')})

    def _add_filter(self, user, is_manager):
        def source(**args):
            filters = [
                {'metadata_filter': {
                    'content_types': ['person']
                }}
            ]
            objects = find_entities(
                user=user,
                sort_on='last_connection',
                filters=filters, **args)
            return objects

        url = self.request.resource_url(self.context,
                                        '@@novaideoapi')
        select = self.selected_filter
        if not is_manager:
            select = [('metadata_filter', ['neagtion', 'states', 'keywords']),
                      ('temporal_filter', ['negation', 'created_date']),
                      'text_filter', 'other_filter']

        return get_filter(
            self, url=url,
            select=select,
            source=source)

    def update(self):
        self.execute(None)
        user = get_current()
        is_manager = has_role(user=user, role=('PortalManager', ))
        filters = [
            {'metadata_filter': {
                'content_types': ['person']
            }}
        ]
        filter_form, filter_data = self._add_filter(user, is_manager)
        args = merge_with_filter_view(self, {})
        args['request'] = self.request
        objects = find_entities(
            user=user,
            sort_on='last_connection',
            filters=filters,
            **args)
        url = self.request.resource_url(self.context, self.name)
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_users"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = self._get_title(
            index=index, len_result=len_result, user=user)
        filter_data['filter_message'] = self.title
        filter_body = self.filter_instance.get_body(filter_data)
        result_body, result = render_listing_objs(
            self.request, batch, user)
        novaideo_catalog = find_catalog('novaideo')
        last_connection_index = novaideo_catalog['last_connection']
        current_date = datetime.datetime.combine(
            datetime.datetime.now(),
            datetime.time(0, 0, 0, tzinfo=pytz.UTC))
        inactive_users = find_users(
            last_connection_index, current_date, (INACTIVITY_DURATION, None))
        if filter_form:
            result = merge_dicts(
                {'css_links': filter_form['css_links'],
                'js_links': filter_form['js_links']
                }, result)

        values = {'bodies': result_body,
                  'batch': batch,
                  'is_manager': is_manager,
                  'inactivity_duration': INACTIVITY_DURATION,
                  'inactive_users': inactive_users.__len__(),
                  'filter_body': filter_body}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class SeeInactiveUsersValidator(Validator):

    @classmethod
    def validate(cls, context, request, **kw):
        if not has_role(role=('PortalManager',)):
            raise ValidationError()


@view_config(
    name='seeinactiveusers',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeInactiveUsersView(BasicView):
    title = _('Inactive members')
    name = 'seeinactiveusers'
    validators = [SeeInactiveUsersValidator]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seeinactiveusers'
    contents_messages = CONTENTS_MESSAGES
    selected_filter = [('metadata_filter', ['neagtion', 'states', 'keywords']),
                       'temporal_filter',
                       'text_filter', 'other_filter']

    def _get_title(self, **args):
        return _(self.contents_messages[args.get('index')],
                 mapping={'nember': args.get('len_result')})

    def _add_filter(self, user, alert_date_min):
        def source(**args):
            filters = [
                {'metadata_filter': {
                    'content_types': ['person']
                },
                'temporal_filter': {
                    'negation': True,
                    'connected_date': {
                        'connected_before': None,
                        'connected_after': alert_date_min
                    }
                }}
            ]
            objects = find_entities(
                user=user,
                sort_on='last_connection',
                filters=filters, **args)
            return objects

        url = self.request.resource_url(self.context,
                                        '@@novaideoapi')
        return get_filter(
            self, url=url,
            select=self.selected_filter,
            source=source)

    def update(self):
        current_date = datetime.datetime.combine(
            datetime.datetime.now(),
            datetime.time(0, 0, 0, tzinfo=pytz.UTC))
        alert_date_min = current_date - datetime.timedelta(
            days=INACTIVITY_DURATION)
        user = get_current()
        filters = [
            {'metadata_filter': {
                'content_types': ['person']
             },
             'temporal_filter': {
                 'negation': True,
                 'connected_date': {
                     'connected_before': None,
                     'connected_after': alert_date_min
                 }
             }}
        ]
        filter_form, filter_data = self._add_filter(user, alert_date_min)
        args = merge_with_filter_view(self, {})
        args['request'] = self.request
        objects = find_entities(
            user=user,
            sort_on='last_connection',
            filters=filters,
            **args)
        url = self.request.resource_url(self.context, self.name)
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_users"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = self._get_title(
            index=index, len_result=len_result, user=user)
        filter_data['filter_message'] = self.title
        filter_body = self.filter_instance.get_body(filter_data)
        result_body, result = render_listing_objs(
            self.request, batch, user)
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
    {SeeUsers: SeeUsersView})


FILTER_SOURCES.update(
    {SeeUsersView.name: SeeUsersView,
     SeeInactiveUsersView.name: SeeInactiveUsersView})
