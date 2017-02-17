# Copyright (c) 2015 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi, Sophie Jazwiecki
import datetime
import pytz
from pyramid.view import view_config
from persistent.list import PersistentList
from pyramid.threadlocal import get_current_registry

from substanced.util import get_oid

from daceui.interfaces import IDaceUIAPI
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import (
    find_catalog, getAllBusinessAction, getBusinessAction,
    getSite, get_obj, find_service)
from dace.objectofcollaboration.principal.util import (
    get_current, get_users_with_role)
from dace.objectofcollaboration.object import Object
from pontus.view import BasicView

from novaideo.views.novaideo_view_manager.search import (
    get_default_searchable_content)
from novaideo.content.interface import (
    IPerson,
    Iidea,
    ISearchableEntity,
    IFile,
    IQuestion,
    IChallenge,
    IOrganization)
from novaideo.utilities.util import (
    render_small_listing_objs, extract_keywords)
from novaideo.utilities.pseudo_react import (
    get_components_data, get_all_updated_data, load_components)
from novaideo.views.filter import find_entities, FILTER_SOURCES
from novaideo import _
from novaideo.core import can_access


ALL_VALUES_KEY = "*"

NBRESULT = 20


def is_all_values_key(key):
    value = key.replace(" ", "")
    return not value or value == ALL_VALUES_KEY


class IndexManagementJsonView(BasicView):

    def _get_pagin_data(self):
        page_limit = self.params('pageLimit')
        if page_limit is None:
            page_limit = 10
        else:
            page_limit = int(page_limit)

        current_page = self.params('page')
        if current_page is None:
            current_page = 1
        else:
            current_page = int(current_page)

        start = page_limit * (current_page - 1)
        end = start + page_limit
        return page_limit, current_page, start, end

    def __call__(self):
        operation_name = self.params('op')
        if operation_name is not None:
            operation = getattr(self, operation_name, None)
            if operation is not None:
                return operation()

        return {}


@view_config(name='novaideoapi',
             context=Object,
             xhr=True,
             renderer='json')
class NovaideoAPI(IndexManagementJsonView):
    alert_template = 'novaideo:views/templates/alerts/alerts.pt'
    search_template = 'novaideo:views/templates/live_search_result.pt'
    search_idea_template = 'novaideo:views/templates/live_search_idea_result.pt'
    search_question_template = 'novaideo:views/templates/live_search_question_result.pt'

    def find_user(self, query=None):
        name = self.params('q')
        if name:
            page_limit, current_page, start, end = self._get_pagin_data()
            if is_all_values_key(name):
                result = find_entities(interfaces=[IPerson],
                                       metadata_filter={'states': ['active']},
                                       add_query=query)
            else:
                result = find_entities(interfaces=[IPerson],
                                       text_filter={'text_to_search': name},
                                       metadata_filter={'states': ['active']},
                                       add_query=query)

            result = [res for res in result]
            if len(result) >= start:
                result = result[start:end]
            else:
                result = result[:end]

            default_img_url = self.request.static_url(
                'novaideo:static/images/user100.png')
            entries = [{'id': str(get_oid(e)),
                        'text': e.title,
                        'img_url': e.get_picture_url(
                            'profil', default_img_url)}
                       for e in result]
            result = {'items': entries, 'total_count': len(result)}
            return result

        return {'items': [], 'total_count': 0}

    def find_organization_user(self):
        novaideo_index = find_catalog('novaideo')
        organization_index = novaideo_index['organizations']
        query = organization_index.any([get_oid(self.context)])
        return self.find_user(query)

    def find_entities(self):
        name = self.params('text_to_search')
        contents = self.params('checkbox')
        if contents and not isinstance(contents, (list, tuple)):
            contents = [contents]

        if not contents:
            contents = get_default_searchable_content(
                self.request)
            contents = [c[0] for c in contents]

        if name:
            states = ['published', 'active']
            user = get_current()
            root = getSite()
            result = []
            if is_all_values_key(name):
                result = find_entities(
                    metadata_filter={
                        'content_types': contents,
                        'states': states},
                    user=user)
            else:
                result = find_entities(
                    metadata_filter={
                        'content_types': contents,
                        'states': states},
                    user=user,
                    text_filter={'text_to_search': name})

            result_body = render_small_listing_objs(
                self.request, list(result)[:NBRESULT], user)
            values = {'entities': result_body,
                      'all_url': self.request.resource_url(
                          root, '@@search_result',
                          query={'text_to_search': name,
                                 'content_types': contents}),
                      'advenced_search_url': self.request.resource_url(
                          root, '@@advanced_search')}
            body = self.content(args=values,
                                template=self.search_template)['body']
            return {'body': body}

        return {'body': ''}

    def find_entity(self, interfaces=[], states=['published', 'active'], query=None):
        name = self.params('q')
        if name:
            user = get_current()
            page_limit, current_page, start, end = self._get_pagin_data()
            if is_all_values_key(name):
                result = find_entities(
                    interfaces=interfaces,
                    metadata_filter={
                        'states': states},
                    user=user,
                    add_query=query)
            else:
                result = find_entities(
                    interfaces=interfaces,
                    metadata_filter={
                        'states': states},
                    user=user,
                    text_filter={'text_to_search': name},
                    add_query=query)

            total_count = len(result)
            if total_count >= start:
                result = list(result)[start:end]
            else:
                result = list(result)[:end]

            entries = [{'id': str(get_oid(e)),
                        'text': e.title,
                        'icon': getattr(
                            e, 'icon', 'glyphicon glyphicon-question-sign')}
                       for e in result]
            result = {'items': entries, 'total_count': total_count}
            return result

        return {'items': [], 'total_count': 0}

    def find_correlable_entity(self):
        return self.find_entity(interfaces=[ISearchableEntity])

    def find_groups(self):
        return self.find_entity(interfaces=[IOrganization, IPerson], states=['published', 'active'])

    def find_smart_folder_contents(self):
        return self.find_entity(interfaces=[ISearchableEntity, IFile], states=[])

    def find_ideas(self):
        novaideo_index = find_catalog('novaideo')
        is_workable_index = novaideo_index['is_workable']
        query = is_workable_index.eq(True)
        return self.find_entity(interfaces=[Iidea], states=[], query=query)

    def find_challenges(self):
        return self.find_entity(interfaces=[IChallenge], states=['pending'])

    def find_all_challenges(self):
        return self.find_entity(interfaces=[IChallenge])

    def filter_result(self):
        filter_source = self.params('filter_source')
        if filter_source is not None and FILTER_SOURCES.get(filter_source, None):
            view_source = FILTER_SOURCES[filter_source](
                self.context, self.request)
            result = view_source.update()
            body = result['coordinates'][view_source.coordinates][0]['body']
            return {'body': body}

        return {'body': ''}

    def remove_comment(self):
        comment_oid = get_oid(self.context, None)
        comment_root = self.context.root
        comment_parent = self.context.comment_parent
        channel = self.context.channel
        subject = channel.subject
        result = self._update_action_view('remove')
        action = result.pop('action_obj')
        result.pop('view_data')
        if subject:
            result.update(get_components_data(
                **get_all_updated_data(
                    action, self.request,
                    subject, self, channel=channel,
                    comment_oid=comment_oid,
                    comment_root=comment_root,
                    comment_parent=comment_parent)))
        return result

    def get_user_alerts(self):
        user = get_current()
        objects = list(getattr(user, 'alerts', []))
        objects.extend(getattr(user, 'old_alerts', []))
        now = datetime.datetime.now(tz=pytz.UTC)
        objects = sorted(
            objects,
            key=lambda e: getattr(e, 'modified_at', now),
            reverse=True)
        result_body = []
        for obj in objects[:20]:
            render_dict = {
                'object': obj,
                'current_user': user
            }
            body = self.content(args=render_dict,
                                template=obj.templates['small'])['body']
            result_body.append(body)

        values = {'bodies': result_body}
        body = self.content(args=values, template=self.alert_template)['body']
        return {'body': body}

    def unsubscribe_user_from_alerts(self):
        user = get_current()
        for alert in getattr(user, 'alerts', []):
            alert.unsubscribe(user)

        return {'status': True}

    def get_similar_ideas(self):
        user = get_current()
        # text = self.params('text')
        title = self.params('title')
        keywords = self.params('keywords')
        # text = text if text else ''
        title = title if title else ''
        keywords = keywords if keywords else []
        if not isinstance(keywords, list):
            keywords = [keywords]

        if not keywords and not title:# and not text:
            return {'body': ''}

        title_keywords = extract_keywords(title)
        # text_keywords = extract_keywords(text)
        # keywords.extend(text_keywords[:5])
        keywords.extend(title_keywords)
        result = find_entities(
            interfaces=[Iidea],
            user=user,
            text_filter={'text_to_search': ', '.join(keywords)},
            defined_search=True,
            generate_text_search=True)
        result_body = render_small_listing_objs(
            self.request, list(result)[:30], user)
        values = {'entities': result_body}
        body = self.content(args=values,
                            template=self.search_idea_template)['body']
        return {'body': body}

    def get_similar_questions(self):
        user = get_current()
        # text = self.params('text')
        title = self.params('title')
        keywords = self.params('keywords')
        # text = text if text else ''
        title = title if title else ''
        keywords = keywords if keywords else []
        if not isinstance(keywords, list):
            keywords = [keywords]

        if not keywords and not title:# and not text:
            return {'body': ''}

        title_keywords = extract_keywords(title)
        # text_keywords = extract_keywords(text)
        # keywords.extend(text_keywords[:5])
        keywords.extend(title_keywords)
        result = find_entities(
            interfaces=[IQuestion],
            user=user,
            text_filter={'text_to_search': ', '.join(keywords)},
            defined_search=True,
            generate_text_search=True)
        result_body = render_small_listing_objs(
            self.request, list(result)[:30], user)
        values = {'entities': result_body}
        body = self.content(args=values,
                            template=self.search_question_template)['body']
        return {'body': body}

    def _execute_action(self, process_id, node_id, appstruct):
        actions = getBusinessAction(
            self.context, self.request,
            process_id, node_id)
        if actions:
            try:
                action = actions[0]
                action.validate(self.context, self.request)
                action.before_execution(self.context, self.request)
                action.execute(self.context, self.request, appstruct)
                return {'state': True, 'action_obj': action}
            except Exception:
                return {'state': False}

        return {'state': False}

    def oppose_idea(self):
        localizer = self.request.localizer
        result = self._execute_action('ideamanagement', 'oppose', {})
        if not result.get('state'):
            self._execute_action(
                'ideamanagement', 'withdraw_token', {})
            result = self._execute_action(
                'ideamanagement', 'oppose', {})
            result['change'] = True

        if result.get('state'):
            result['action'] = self.request.resource_url(
                self.context, 'novaideoapi',
                query={'op': 'withdraw_token_idea',
                       'action': 'oppose'})
            result['title'] = localizer.translate(_('Withdraw my token'))
            if result.get('change', False):
                result['opposit_action'] = self.request.resource_url(
                    self.context, 'novaideoapi',
                    query={'op': 'support_idea'})
                result['opposit_title'] = localizer.translate(_('Support'))

        user = get_current()
        result['hastoken'] = True if getattr(user, 'tokens', []) else False
        result.update(get_components_data(
            **get_all_updated_data(
                result.pop('action_obj', None), self.request, self.context, self)))
        return result

    def oppose_proposal(self):
        localizer = self.request.localizer
        result = self._execute_action('proposalmanagement', 'oppose', {})
        if not result.get('state'):
            self._execute_action(
                'proposalmanagement', 'withdraw_token', {})
            result = self._execute_action(
                'proposalmanagement', 'oppose', {})
            result['change'] = True

        if result.get('state'):
            result['action'] = self.request.resource_url(
                self.context, 'novaideoapi',
                query={'op': 'withdraw_token_proposal',
                       'action': 'oppose'})
            result['title'] = localizer.translate(_('Withdraw my token'))
            if result.get('change', False):
                result['opposit_action'] = self.request.resource_url(
                    self.context, 'novaideoapi',
                    query={'op': 'support_proposal'})
                result['opposit_title'] = localizer.translate(_('Support'))

        user = get_current()
        result['hastoken'] = True if getattr(user, 'tokens', []) else False
        result.update(get_components_data(
            **get_all_updated_data(
                result.pop('action_obj', None),
                self.request, self.context, self)))
        return result

    def support_idea(self):
        localizer = self.request.localizer
        result = self._execute_action('ideamanagement', 'support', {})
        if not result.get('state'):
            self._execute_action(
                'ideamanagement', 'withdraw_token', {})
            result = self._execute_action(
                'ideamanagement', 'support', {})
            result['change'] = True

        if result.get('state'):
            result['action'] = self.request.resource_url(
                self.context, 'novaideoapi',
                query={'op': 'withdraw_token_idea',
                       'action': 'support'})
            result['title'] = localizer.translate(_('Withdraw my token'))
            if result.get('change', False):
                result['opposit_action'] = self.request.resource_url(
                    self.context, 'novaideoapi',
                    query={'op': 'oppose_idea'})
                result['opposit_title'] = localizer.translate(_('Oppose'))

        user = get_current()
        result['hastoken'] = True if getattr(user, 'tokens', []) else False
        result.update(get_components_data(
            **get_all_updated_data(
                result.pop('action_obj', None),
                self.request, self.context, self)))
        return result

    def support_proposal(self):
        localizer = self.request.localizer
        result = self._execute_action('proposalmanagement', 'support', {})
        if not result.get('state'):
            self._execute_action(
                'proposalmanagement', 'withdraw_token', {})
            result = self._execute_action(
                'proposalmanagement', 'support', {})
            result['change'] = True

        if result.get('state'):
            result['action'] = self.request.resource_url(
                self.context, 'novaideoapi',
                query={'op': 'withdraw_token_proposal',
                       'action': 'support'})
            result['title'] = localizer.translate(_('Withdraw my token'))
            if result.get('change', False):
                result['opposit_action'] = self.request.resource_url(
                    self.context, 'novaideoapi',
                    query={'op': 'oppose_proposal'})
                result['opposit_title'] = localizer.translate(_('Oppose'))

        user = get_current()
        result['hastoken'] = True if getattr(user, 'tokens', []) else False
        result.update(get_components_data(
            **get_all_updated_data(
                result.pop('action_obj', None),
                self.request, self.context, self)))
        return result

    def withdraw_token_idea(self):
        localizer = self.request.localizer
        result = self._execute_action('ideamanagement', 'withdraw_token', {})
        if result.get('state'):
            previous_action = self.params('action')
            result['action'] = self.request.resource_url(
                self.context, 'novaideoapi',
                query={'op': previous_action + '_idea'})
            result['title'] = localizer.translate(
                _('Oppose' if previous_action == 'oppose' else 'Support'))
            result['withdraw'] = True

        user = get_current()
        result['hastoken'] = True if getattr(user, 'tokens', []) else False
        result.update(get_components_data(
            **get_all_updated_data(
                result.pop('action_obj', None),
                self.request, self.context, self)))
        return result

    def withdraw_token_proposal(self):
        localizer = self.request.localizer
        result = self._execute_action(
            'proposalmanagement', 'withdraw_token', {})
        if result.get('state'):
            previous_action = self.params('action')
            result['action'] = self.request.resource_url(
                self.context, 'novaideoapi',
                query={'op': previous_action + '_proposal'})
            result['title'] = localizer.translate(
                _('Oppose' if previous_action == 'oppose' else 'Support'))
            result['withdraw'] = True

        user = get_current()
        result['hastoken'] = True if getattr(user, 'tokens', []) else False
        result.update(get_components_data(
            **get_all_updated_data(
                result.pop('action_obj', None),
                self.request, self.context, self)))
        return result

    def update_notification_id(self):
        user = get_current()
        notif_id = self.params('id')
        if not hasattr(user, 'notification_ids'):
            user.notification_ids = PersistentList([])

        user.notification_ids.append(notif_id)
        return {'ids': list(user.notification_ids)}

    def get_entity_popover(self):
        oid_str = self.params('oid')
        from novaideo.utilities.util import (
            generate_listing_menu,
            DEFAUL_LISTING_FOOTER_ACTIONS_TEMPLATE,
            ObjectRemovedException)
        if oid_str:
            try:
                obj = get_obj(int(oid_str))
                user = get_current()
                if obj and can_access(user, obj):
                    try:
                        navbars = generate_listing_menu(
                            self.request, obj,
                            descriminators=['communication-action', 'access-action'],
                            footer_template=DEFAUL_LISTING_FOOTER_ACTIONS_TEMPLATE,
                            view_type='popover')
                    except ObjectRemovedException:
                        return {'body': ''}

                    user = get_current()
                    render_dict = {
                        'object': obj,
                        'oid': oid_str,
                        'current_user': user,
                        'footer_body': navbars['footer_body'],
                        'access_body': navbars['access_body'],
                    }
                    body = self.content(
                        args=render_dict,
                        template=obj.templates.get('popover'))['body']
                    return {'body': body}
            except:
                pass

        return {'body': ''}

    def load_views(self):
        result = {}
        result.update(get_components_data(
            **load_components(
                self.request,
                self.context, self)))
        return result

    def _get_start_action(self):
        action = None
        pd_id = self.params('pd_id')
        action_id = self.params('action_id')
        behavior_id = self.params('behavior_id')
        def_container = find_service('process_definition_container')
        pd = def_container.get_definition(pd_id)
        start_wi = pd.start_process(action_id)[action_id]
        for start_action in start_wi.actions:
            if start_action.behavior_id == behavior_id:
                action = start_action
                break

        return action

    def _update_action_view(self, node_id=None, process_id=None):
        if not node_id:
            node_process = self.params('node_id').split('.')
            process_id = node_process[0]
            node_id = node_process[1]

        node_actions = getAllBusinessAction(
            self.context, self.request,
            process_id=process_id, node_id=node_id,
            process_discriminator='Application')
        if node_actions:
            action = node_actions[0]
            node_view = DEFAULTMAPPING_ACTIONS_VIEWS[action.__class__]
            node_view_instance = node_view(
                self.context, self.request,
                behaviors=[action],
                only_form=True)
            view_result = node_view_instance()
            return {
                'status': True,
                'action_obj': action,
                'view_data': (node_view_instance, view_result)}

        return {
            'status': False,
            'action_obj': None,
            'view_data': None}

    def update_action_view(self):
        result = self._update_action_view()
        action = result.pop('action_obj')
        view_data = result.pop('view_data')
        result.update(get_components_data(
            **get_all_updated_data(
                action, self.request,
                self.context, self, view_data=view_data)))
        return result

    def update_action(self, action=None, context=None):
        # import pdb; pdb.set_trace()
        result = {}
        action_uid = self.params('action_uid')
        try:
            if action_uid:
                action = get_obj(int(action_uid))
            else:
                action = self._get_start_action()
        except Exception:
            return {}

        context_uid = self.params('context_uid')
        try:
            if context_uid:
                context = get_obj(int(context_uid))
        except Exception:
            pass

        dace_ui_api = get_current_registry().getUtility(
            IDaceUIAPI, 'dace_ui_api')
        body, resources = dace_ui_api.get_action_body(
            context, self.request, action,
            include_resources=True)
        result = {'body': body}
        result.update(get_components_data(
            **get_all_updated_data(
                action, self.request, context,
                self, resources=resources)))
        return result

    def after_execution_action(self):
        action_uid = self.params('action_uid')
        context_uid = self.params('context_uid')
        action = None
        context = None
        try:
            if action_uid is not None:
                action = get_obj(int(action_uid))
            else:
                action = self._get_start_action()

        except Exception:
            return {}#message erreur

        try:
            if context_uid is not None:
                context = get_obj(int(context_uid))
        except Exception:
            pass

        if action is not None and action.validate(context, self.request):
            action.after_execution(context, self.request)

        return {}#message erreur

    def update_guide_tour_data(self):
        user = get_current()
        if self.request.user and hasattr(user, 'guide_tour_data'):
            guide_state = self.params('guide_state')
            if guide_state:
                user.guide_tour_data['guide_state'] = guide_state

            guide = self.params('guide')
            page = self.params('page')
            if guide is not None and page is not None:
                page_state = self.params('page_state')
                guide_value = self.params('guide_value')
                page_value = self.params('page_value')
                guide_value = guide_value if guide_value is not None else -1
                page_value = page_value if page_value is not None else 0
                page_state = page_state if page_state is not None else 'pending'
                user.guide_tour_data[guide+'_'+page] = {
                    'guide': guide_value,
                    'page': page_value,
                    'page_state': page_state
                }
                user.guide_tour_data['guide_state'] = 'pending'
