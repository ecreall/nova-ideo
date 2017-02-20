# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from substanced.util import Batch

from dace.util import find_catalog, getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import (
    get_current, has_any_roles)
from pontus.view import BasicView
from pontus.util import merge_dicts
from pontus.view_operation import MultipleView

from novaideo.utilities.util import render_listing_objs
from novaideo.content.processes.challenge_management.behaviors import (
    SeeChallenge)
from novaideo.content.challenge import Challenge
from novaideo.utilities.util import (
    generate_navbars, ObjectRemovedException, get_home_actions_bodies)
from novaideo import _
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.views.filter import (
    get_filter, FILTER_SOURCES,
    merge_with_filter_view, find_entities)
from novaideo.views.filter.sort import (
    sort_view_objects)
from novaideo.views.core import asyn_component_config


CONTENTS_MESSAGES = {
    '0': _(u"""No element found"""),
    '1': _(u"""One element found"""),
    '*': _(u"""${nember} elements found""")
}


def get_contents_forms(request):
        result = {
            'forms': [],
            'css_links': [],
            'js_links': [],
            'has_forms': False}
        if request.view_name not in ('', 'index', 'seemycontents'):
            return result

        root = getSite()
        result_idea = get_home_actions_bodies(
            'ideamanagement', 'creat', 'formcreateideahome',
            request, root)
        result['forms'].append({
            'id': 'ideahomeform',
            'active': True,
            'title': _('Create an idea'),
            'form': result_idea['form'],
            'action': result_idea['action'],
            'search_url': request.resource_url(
                root, '@@novaideoapi', query={'op': 'get_similar_ideas'}),
            'action_url': request.resource_url(
                root, '@@ideasmanagement',
                query={'op': 'creat_home_idea'}),
            'css_class': 'home-add-idea'
        })
        has_forms = result_idea['form'] is not None
        result['js_links'] = result_idea['js_links']
        result['css_links'] = result_idea['css_links']
        result_question = get_home_actions_bodies(
            'questionmanagement', 'creat',
            'formaskquestionhome', request, root)
        result['forms'].append({
            'id': 'questionhomeform',
            'title': _('Ask a question'),
            'form': result_question['form'],
            'action': result_question['action'],
            'search_url': request.resource_url(
                root, '@@novaideoapi', query={'op': 'get_similar_questions'}),
            'action_url': request.resource_url(
                root, '@@questionsmanagement',
                query={'op': 'creat_home_question'}),
            'css_class': 'home-add-question'
        })
        has_forms = has_forms or result_question['form'] is not None
        result['has_forms'] = has_forms
        result['js_links'].extend(result_idea['js_links'])
        result['css_links'].extend(result_idea['css_links'])
        result['js_links'] = list(set(result['js_links']))
        result['css_links'] = list(set(result['css_links']))
        return result


class ContentView(BasicView):
    template = 'novaideo:views/novaideo_view_manager/templates/home.pt'
    anonymous_template = 'novaideo:views/novaideo_view_manager/templates/anonymous_view.pt'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    content_type = 'idea'
    isactive = False

    def _add_filter(self, user):
        def source(**args):
            default_content = [self.content_type]
            novaideo_index = find_catalog('novaideo')
            challenges = novaideo_index['challenges']
            query = challenges.any([self.context.__oid__])
            filter_ = {
                'metadata_filter': {
                    'content_types': default_content,
                    'states': ['active', 'published']}
            }
            objects = find_entities(
                user=user, filters=[filter_], add_query=query, **args)
            return objects

        url = self.request.resource_url(
            self.context, '@@novaideoapi',
            query={'view_content_type': self.content_type})
        select = [('metadata_filter', ['states', 'keywords']), 'geographic_filter',
                  'contribution_filter',
                  ('temporal_filter', ['negation', 'created_date']),
                  'text_filter', 'other_filter']
        return get_filter(
            self,
            url=url,
            source=source,
            select=select,
            filter_source="challenge",
            filterid=self.content_type)

    def update(self):
        if self.request.is_idea_box:
            self.title = ''

        user = get_current()
        filter_form, filter_data = self._add_filter(user)
        default_content = [self.content_type]
        validated = {
            'metadata_filter':
                {'content_types': default_content,
                'states': ['active', 'published']}
        }
        args = {}
        args = merge_with_filter_view(self, args)
        args['request'] = self.request
        novaideo_index = find_catalog('novaideo')
        challenges = novaideo_index['challenges']
        query = challenges.any([self.context.__oid__])
        objects = find_entities(
            user=user,
            filters=[validated],
            add_query=query,
            **args)
        objects, sort_body = sort_view_objects(
            self, objects, [self.content_type], user)
        url = self.request.resource_url(
            self.context, '',
            query={'view_content_type': self.content_type})
        batch = Batch(objects,
                      self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        self.title = _(self.title, mapping={'nb': batch.seqlen})
        batch.target = "#results"+"-"+ self.content_type
        filter_instance = getattr(self, 'filter_instance', None)
        filter_body = None
        if filter_instance:
            filter_data['filter_message'] = self.title
            filter_body = filter_instance.get_body(filter_data)
        result_body, result = render_listing_objs(
            self.request, batch, user)
        values = {'bodies': result_body,
                  'batch': batch,
                  'empty_message': self.empty_message,
                  'empty_icon': self.empty_icon,
                  'filter_body': filter_body,
                  'sort_body': sort_body}
        if filter_form:
            result = merge_dicts(
                {'css_links': filter_form['css_links'],
                 'js_links': filter_form['js_links']
                }, result)

        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['isactive'] = self.isactive
        result['coordinates'] = {self.coordinates: [item]}
        return result


class IdeasView(ContentView):
    title = _('Ideas (${nb})')
    content_type = 'idea'
    viewid = 'challenge-ideas'
    view_icon = 'icon novaideo-icon icon-idea'
    counter_id = 'challenge-ideas-counter'
    empty_message = _("No registered ideas")
    empty_icon = 'icon novaideo-icon icon-idea'
    isactive = True


class ProposalsView(ContentView):
    title = _('The Working Groups (${nb})')
    content_type = 'proposal'
    viewid = 'challenge-proposals'
    view_icon = 'icon novaideo-icon icon-wg'
    counter_id = 'challenge-proposals-counter'
    empty_message = _("No working group created")
    empty_icon = 'icon novaideo-icon icon-wg'


class QuestionsView(ContentView):
    title = _('Questions (${nb})')
    content_type = 'question'
    viewid = 'challenge-questions'
    view_icon = 'md md-live-help'
    counter_id = 'challenge-questions-counter'
    empty_message = _("No question asked")
    empty_icon = 'md md-live-help'


class DetailChallengeView(BasicView):
    name = 'seechallengedetail'
    viewid = 'seechallengedetail'
    behaviors = [SeeChallenge]
    validate_behaviors = False
    template = 'novaideo:views/challenge_management/templates/see_challenge.pt'
    title = _('Details')

    def update(self):
        self.execute(None)
        root = getSite()
        try:
            navbars = generate_navbars(
                self.request, self.context)
        except ObjectRemovedException:
            return HTTPFound(self.request.resource_url(root, ''))

        user = self.get_binding('user')
        is_censored = 'censored' in self.context.state
        to_hide = is_censored and not has_any_roles(
            user=user,
            roles=(('Owner', self.context), 'Moderator'))

        files = getattr(self.context, 'attached_files', [])
        files_urls = []
        for file_ in files:
            files_urls.append({'title': file_.title,
                               'url': file_.url})

        result = {}
        values = {
            'challenge': self.context,
            'to_hide': to_hide,
            'is_censored': is_censored,
            'text': self.context.text,
            'current_user': user,
            'files': files_urls,
            'navbar_body': navbars['navbar_body'],
            'footer_body': navbars['footer_body']
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['isactive'] = True
        result['coordinates'] = {self.coordinates: [item]}
        # result.update(resources)
        return result


class ParticipateView(BasicView):
    name = 'participatechallenge'
    viewid = 'participatechallenge'
    template = 'novaideo:views/templates/panels/addcontenthomeform.pt'
    title = _('Participate')

    def update(self):
        resources = {
            'js_links': [],
            'css_links': []
        }
        contents_forms = {'has_forms': False}
        if self.context.can_add_content:
            contents_forms = get_contents_forms(self.request)
            resources = {
                'js_links': contents_forms.pop('js_links'),
                'css_links': contents_forms.pop('css_links')
            }

        result = {}
        body = self.content(args=contents_forms, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['isactive'] = True
        result['coordinates'] = {self.coordinates: [item]}
        result.update(resources)
        return result


@asyn_component_config(id='challenge_see_challenge')
class ChallengeContentsView(MultipleView):
    title = ''
    name = 'seechallengecontents'
    template = 'novaideo:views/templates/multipleview.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    viewid = 'challengecontents'
    center_tabs = True
    views = (QuestionsView, IdeasView, ProposalsView)

    def _init_views(self, views, **kwargs):
        if self.params('load_view'):
            if self.request.is_idea_box:
                views = (IdeasView, )

            if self.params('view_content_type') == 'idea':
                views = (IdeasView, )

            if self.params('view_content_type') == 'proposal':
                views = (ProposalsView, )

            if self.params('view_content_type') == 'question':
                views = (QuestionsView, )

        super(ChallengeContentsView, self)._init_views(views, **kwargs)


class ParticipateContentView(MultipleView):
    title = ''
    name = 'participatecontents'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    viewid = 'participatecontents'
    views = (ParticipateView, ChallengeContentsView)


@view_config(
    name='index',
    context=Challenge,
    renderer='pontus:templates/views_templates/grid.pt',
    )
@view_config(
    name='',
    context=Challenge,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ChallengeView(MultipleView):
    title = ''
    name = 'seechallenge'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    viewid = 'challenge'
    css_class = 'simple-bloc'
    container_css_class = 'home'
    views = (DetailChallengeView, ParticipateContentView)
    validators = [SeeChallenge.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeChallenge: ChallengeView})


FILTER_SOURCES.update(
    {"challenge": ChallengeView})
