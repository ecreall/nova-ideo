# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
from pyramid.view import view_config

from substanced.util import Batch

from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView
from pontus.util import merge_dicts

from novaideo.utilities.util import render_listing_objs
from novaideo.content.processes.challenge_management.behaviors import (
    SeeChallenges)
from novaideo.content.interface import IChallenge
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.views.filter import (
    get_filter, FILTER_SOURCES, merge_with_filter_view, find_entities)
from novaideo.views.filter.sort import (
    sort_view_objects)
from novaideo.views.core import asyn_component_config


BATCH_DEFAULT_SIZE = 8


BATCH_HOME_DEFAULT_SIZE = 4


CONTENTS_MESSAGES = {
    '0': _(u"""No challenge found"""),
    '1': _(u"""One challenge found"""),
    '*': _(u"""${nember} challenges found""")
    }


@asyn_component_config(id='novaideoap_seechallenges')
@view_config(
    name='seechallenges',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeChallengesView(BasicView):
    title = _('Participate in our challenges')
    name = 'seechallenges'
    behaviors = [SeeChallenges]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seechallenges'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'

    def _add_filter(self, user):
        def source(**args):
            filters = [
                {'metadata_filter': {
                    'content_types': ['challenge']
                }}
            ]
            objects = find_entities(
                user=user, filters=filters, **args)
            return objects

        url = self.request.resource_url(self.context, '@@novaideoapi')
        return get_filter(
            self,
            url=url,
            source=source,
            select=[('metadata_filter', ['negation', 'states', 'keywords']),
                    'contribution_filter', 'temporal_filter',
                    'text_filter', 'other_filter'])

    def update(self):
        self.execute(None)
        user = get_current()
        filter_form, filter_data = self._add_filter(user)
        filters = [
            {'metadata_filter': {
                'content_types': ['challenge']
            }}
        ]
        args = {}
        args = merge_with_filter_view(self, args)
        args['request'] = self.request
        objects = find_entities(user=user,
                                filters=filters,
                                **args)
        objects, sort_body = sort_view_objects(
            self, objects, ['challenge'], user,
            intersect=getattr(self, 'sorts', None))
        url = self.request.resource_url(self.context, self.name)
        batch = Batch(
            objects, self.request, url=url, default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results-home-challenges"
        len_result = batch.seqlen
        index = str(len_result)
        if len_result > 1:
            index = '*'

        self.title = _(CONTENTS_MESSAGES[index],
                       mapping={'nember': len_result})
        filter_data['filter_message'] = self.title
        filter_body = self.filter_instance.get_body(filter_data)
        result_body, result = render_listing_objs(
            self.request, batch, user)
        if filter_form:
            result = merge_dicts(
                {'css_links': filter_form['css_links'],
                 'js_links': filter_form['js_links']
                }, result)

        values = {
            'bodies': result_body,
            'batch': batch,
            'filter_body': filter_body,
            'sort_body': sort_body
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


@view_config(
    name='seehomechallenges',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeChallengesHomeView(BasicView):
    title = _('Participate in our challenges')
    name = 'seehomechallenges'
    behaviors = [SeeChallenges]
    template = 'novaideo:views/challenge_management/templates/see_challenges.pt'
    viewid = 'seehomechallenges'
    wrapper_template = 'novaideo:views/smart_folder_management/templates/folder_blocs_view_wrapper.pt'
    css_class = 'simple-bloc challenges-bloc'
    container_css_class = 'home'

    def update(self):
        self.execute(None)
        user = get_current()
        objects = find_entities(
            user=user, interfaces=[IChallenge],
            metadata_filter={'states': ['pending']},
            sort_on='release_date')
        url = self.request.resource_url(self.context, self.name)
        batch = Batch(
            objects, self.request, url=url, default_size=BATCH_HOME_DEFAULT_SIZE)
        batch.target = "#results-home-challenges"
        len_result = batch.seqlen
        user = get_current()
        if len_result == 0:
            self.no_challenges = True
            result = {}
            result_body = []
        else:
            self.title = self.request.localizer.translate(self.title)
            result_body, result = render_listing_objs(
                self.request, batch, user, 'bloc')

        values = {
            'bodies': result_body,
            'batch': batch
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeChallenges: SeeChallengesView})


FILTER_SOURCES.update(
    {SeeChallengesView.name: SeeChallengesView})
