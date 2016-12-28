# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
from collections import OrderedDict
from pyramid import renderers
from pyramid_layout.panel import panel_config
from pyramid.threadlocal import get_current_registry

from substanced.util import get_oid

from pontus.util import update_resources
from dace.objectofcollaboration.entity import Entity
from dace.util import (
    getBusinessAction, getSite,
    find_catalog, getAllBusinessAction,
    get_obj)
from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from daceui.interfaces import IDaceUIAPI

from novaideo.utilities.util import (
    generate_listing_menu, ObjectRemovedException)
from novaideo.content.processes.novaideo_view_manager.behaviors import(
    SeeMyContents,
    SeeMySelections,
    SeeMyParticipations,
    SeeMySupports)
from novaideo.content.processes.idea_management.behaviors import CreateIdea
from novaideo.content.person import Person
from novaideo.content.interface import IPerson, Iidea, IProposal, ISmartFolder
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.core import _, SearchableEntity, can_access
from novaideo.content.processes.user_management.behaviors import (
    global_user_processsecurity)
from novaideo.utilities.util import (
    get_actions_navbar,
    render_navbar_body,
    deepcopy,
    FOOTER_NAVBAR_TEMPLATE,
    update_all_ajax_action,
    get_debatescore_data)
from novaideo.views.filter import find_entities, find_more_contents
from novaideo.contextual_help_messages import render_contextual_help
from novaideo.steps import steps_panels
from novaideo.content.idea import Idea
from novaideo.content.proposal import Proposal
from novaideo.content.smart_folder import SmartFolder
from novaideo.fr_lexicon import normalize_title


LEVEL_MENU = 3


DEFAULT_FOLDER_COLORS = {'usual_color': 'white, #2d6ca2',
                         'hover_color': 'white, #2d6ca2'}


MORE_NB = 20


GROUPS_PICTO = {
    'Add': (0, 'glyphicon glyphicon-plus'),
    'See': (1, 'glyphicon glyphicon-eye-open'),
    'Edit': (2, 'glyphicon glyphicon-pencil'),
    'Directory': (3, 'glyphicon glyphicon-book'),
    'More': (4, 'glyphicon glyphicon-cog'),
 }


def _getaction(view, process_id, action_id):
    root = getSite()
    actions = getBusinessAction(root, view.request, process_id, action_id)
    action = None
    action_view = None
    if actions is not None:
        action = actions[0]
        if action.__class__ in DEFAULTMAPPING_ACTIONS_VIEWS:
            action_view = DEFAULTMAPPING_ACTIONS_VIEWS[action.__class__]

    return action, action_view


@panel_config(
    name='usermenu',
    context=Entity,
    renderer='templates/panels/usermenu.pt'
    )
class Usermenu_panel(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        root = getSite()
        resources = deepcopy(getattr(
            self.request, 'resources', {'js_links': [], 'css_links': []}))
        search_action, search_view = _getaction(self,
                                                'novaideoviewmanager',
                                                'search')
        search_view_instance = search_view(root, self.request,
                                           behaviors=[search_action])
        posted_formid = None
        if self.request.POST :
            if '__formid__' in self.request.POST:
                posted_formid = self.request.POST['__formid__']

            if posted_formid and \
              posted_formid.startswith(search_view_instance.viewid):
                search_view_instance.postedform = self.request.POST.copy()
                self.request.POST.clear()

        search_view_result = search_view_instance()
        search_body = ''
        result = {'css_links': [], 'js_links': []}
        if isinstance(search_view_result, dict) and \
           'coordinates' in search_view_result:
            search_render = search_view_result['coordinates'][search_view_instance.coordinates][0]
            result['css_links'] = [c for c in search_view_result['css_links']
                                   if c not in resources['css_links']]
            result['js_links'] = [c for c in search_view_result['js_links']
                                  if c not in resources['js_links']]
            search_body = search_view_instance.render_item(
                search_render,
                search_view_instance.coordinates,
                None)

        result['search_body'] = search_body
        result['view'] = self
        update_resources(self.request, result)
        return result


@panel_config(
    name='addideaform',
    context=NovaIdeoApplication,
    renderer='templates/panels/addideaform.pt'
    )
class AddIdea(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        result = {
            'form': None,
            'css_links': [],
            'js_links': []}
        if(self.request.view_name not in ('', 'seemycontents')):
            return {'form': None}

        root = getSite()
        resources = deepcopy(getattr(
            self.request, 'resources', {'js_links': [], 'css_links': []}))
        add_idea_action, add_idea_view = _getaction(
            self, 'ideamanagement', 'creat')
        if add_idea_view:
            add_idea_view_instance = add_idea_view(
                root, self.request, behaviors=[add_idea_action])
            add_idea_view_instance.viewid = 'formcreateideahome'
            add_idea_view_instance.is_home_form = True
            add_idea_view_result = add_idea_view_instance()
            add_idea_body = ''
            if isinstance(add_idea_view_result, dict) and \
               'coordinates' in add_idea_view_result:
                add_idea_body = add_idea_view_result['coordinates'][add_idea_view_instance.coordinates][0]['body']
                result['css_links'] = [c for c in add_idea_view_result.get('css_links', [])
                                       if c not in resources['css_links']]
                result['js_links'] = [c for c in add_idea_view_result.get('js_links', [])
                                      if c not in resources['js_links']]

            update_resources(self.request, result)
            result['form'] = add_idea_body
            result['view'] = self
            result['action_url'] = self.request.resource_url(
                root, '@@ideasmanagement', query={'op': 'creat_home_idea'})
            result['search_url'] = self.request.resource_url(
                root, '@@novaideoapi', query={'op': 'get_similar_ideas'})

        return result


@panel_config(
    name='usernavbar',
    context=Entity,
    renderer='templates/panels/navbar_view.pt'
    )
class UserNavBarPanel(object):

    navbar_actions = [SeeMyContents, SeeMyParticipations,
                      SeeMySelections, SeeMySupports]

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, has_contextual_help=False):
        root = getSite()
        if getattr(self.request, 'is_idea_box', False):
            self.navbar_actions = [SeeMyContents, SeeMySelections]

        actions_url = OrderedDict()
        for actionclass in self.navbar_actions:
            process_id, action_id = tuple(actionclass.node_definition.id.split('.'))
            action, view = _getaction(self, process_id, action_id)
            if None not in (action, view):
                actions_url[action.title] = {
                            'action': action,
                            'action_id': action_id,
                            'icon': action.style_picto,
                            'url': action.url(root),
                            'view_name': getattr(view,'name', None)}
            else:
                actions_url[actionclass.node_definition.title] = {
                            'action': None,
                            'action_id': action_id,
                            'icon': actionclass.style_picto,
                            'url': None,
                            'view_name': getattr(view,'name', None)}
        result = {}
        result['actions'] = actions_url
        result['view'] = self
        result['has_contextual_help'] = has_contextual_help
        return result


@panel_config(
    name='novaideo_contents',
    context=NovaIdeoApplication,
    renderer='templates/panels/novaideo_contents.pt'
    )
class NovaideoContents(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        if self.request.view_name != '':
            return {'condition': False}

        result = {}
        dace_catalog = find_catalog('dace')
        states_index = dace_catalog['object_states']
        object_provides_index = dace_catalog['object_provides']
        query = object_provides_index.any((IPerson.__identifier__ ,)) & \
                states_index.notany(['deactivated'])
        result['nb_person'] = query.execute().__len__()
        query = object_provides_index.any((Iidea.__identifier__ ,)) & \
                states_index.any(['published'])
        result['nb_idea'] = query.execute().__len__()
        result['nb_proposal'] = 0
        if not getattr(self.request, 'is_idea_box', False):
            query = object_provides_index.any((IProposal.__identifier__ ,)) & \
                    states_index.notany(['archived', 'draft'])
            result['nb_proposal'] = query.execute().__len__()

        result['condition'] = True
        return result


@panel_config(
    name='steps',
    context=Entity,
    renderer='templates/panels/steps.pt'
    )
class StepsPanel(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return steps_panels(self.context, self.request)


@panel_config(
    name='novaideo_footer',
    renderer='templates/panels/novaideo_footer.pt'
    )
class NovaideoFooter(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        root = getSite()
        def actions_getter():
            return [a for a in getAllBusinessAction(
                      root, process_discriminator='Application')
                    if getattr(a, 'style', '') == 'button']

        actions_navbar = get_actions_navbar(
            actions_getter, root, self.request, ['footer-action'])
        return {'navbar_body': render_navbar_body(
            self, self.context, actions_navbar,
            FOOTER_NAVBAR_TEMPLATE, ['footer-action'])}


@panel_config(
    name='lateral_menu',
    context=Entity,
    renderer='templates/panels/lateral_menu.pt'
    )
class LateralMenu(object):
    actions = {
        CreateIdea: ('ideamanagement', 'creat', 'btn-success')}

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        root = getSite()
        # resources = deepcopy(getattr(
        #     self.request, 'resources', {'js_links': [], 'css_links': []}))
        try:
            navbars = generate_listing_menu(
                self.request, root,
                descriminators=['lateral-action'],
                template='novaideo:views/templates/lateral_menu.pt')
        except ObjectRemovedException:
            return {'menu_body': None}

        result = {
            'css_links': [],
            'js_links': [],
            'menu_body': navbars['menu_body']}
        # result['css_links'] = [c for c in navbars['resources'].get('css_links', [])
        #                        if c not in resources['css_links']]
        # result['js_links'] = [c for c in navbars['resources'].get('js_links', [])
        #                       if c not in resources['js_links']]
        # update_resources(self.request, result)
        return result


def group_actions(actions):
    groups = {}
    for action in actions:
        group_id = _('More')
        if action[1].node_definition.groups:
            group_id = action[1].node_definition.groups[0]

        group = groups.get(group_id, None)
        if group:
            group.append(action)
        else:
            groups[group_id] = [action]

    for group_id, group in groups.items():
        groups[group_id] = sorted(group,
            key=lambda e: getattr(e[1], 'style_order', 0))
    groups = sorted(list(groups.items()),
                    key=lambda g: GROUPS_PICTO.get(g[0], ("default", 0))[0])
    return groups


@panel_config(
    name='adminnavbar',
    context=Entity,
    renderer='templates/panels/admin_navbar.pt'
    )
class Adminnavbar_panel(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        root = getSite()
        if not global_user_processsecurity():
            return {'error': True}

        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,
                                                        'dace_ui_api')
        actions = dace_ui_api.get_actions([root], self.request)
        admin_actions = [a for a in actions
                         if getattr(a[1], 'style_descriminator', '') in
                         ('admin-action', 'lateral-action')]
        return {'groups': group_actions(admin_actions),
                'pictos': {g: v[1] for g, v in GROUPS_PICTO.items()},
                'error': False}


@panel_config(
    name='deadline',
    context=NovaIdeoApplication,
    renderer='templates/panels/deadline.pt'
    )
class Deadline_panel(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        if not self.request.content_to_examine or \
           self.request.view_name != '':
            return {'condition': False}

        current_deadline = self.context.deadlines[-1].replace(tzinfo=pytz.UTC)
        previous_deadline = datetime.datetime.now(tz=pytz.UTC)
        try:
            previous_deadline = self.context.deadlines[-2].replace(tzinfo=pytz.UTC)
        except Exception:
            pass

        current_date = datetime.datetime.now(tz=pytz.UTC)
        total_sec_current_deadline = (current_deadline - previous_deadline).total_seconds()
        percent = 100
        expired = False
        if total_sec_current_deadline > 0 and \
           not current_date > current_deadline:
            total_sec_current_date = (current_date - previous_deadline).total_seconds()
            percent = (total_sec_current_date * 100) / total_sec_current_deadline
        else:
            expired = True

        return {'percent': int(percent),
                'expired': expired,
                'current_deadline': current_deadline,
                'current_date': current_date,
                'previous_deadline': previous_deadline,
                'condition': True}


@panel_config(
    name='contextual_help',
    context=Entity,
    renderer='templates/panels/contextual_help.pt'
    )
class ContextualHelp(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        if not self.request.cookies.get('contextual_help', True):
            return {'condition': False}

        user = get_current()
        messages = render_contextual_help(
            self.request, self.context, user, self.request.view_name)
        return {'messages': messages,
                'condition': True}


@panel_config(
    name='social_share',
    context=Entity,
    renderer='templates/panels/social_share.pt'
    )
class SocialShare(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        if self.request.view_name != 'index' or \
           not isinstance(self.context, SearchableEntity) or \
           not self.context.is_published:
            return {'condition': False}

        has_social_share = getattr(
            self.request.root, 'social_share', False),
        return {'request': self.request,
                'object': self.context,
                'condition': has_social_share}


@panel_config(
    name='social_share_toggle',
    context=Entity,
    renderer='templates/panels/social_share_toggle.pt'
    )
class SocialToggleShare(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return {'has_social_share': getattr(
                    self.request.root, 'social_share', False),
                'object': self.context}


@panel_config(
    name='more_contents',
    context=NovaIdeoApplication,
    renderer='templates/panels/more_contents.pt'
    )
@panel_config(
    name='more_contents',
    context=SearchableEntity,
    renderer='templates/panels/more_contents.pt'
    )
class MoreContents(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        is_root = False
        objects = []
        if self.request.view_name in ('', 'index', '@@index'):
            user = get_current()
            more_result = []
            root = getSite()
            if self.context is root:
                keywords = getattr(user, 'keywords', [])
                if not keywords:
                    more_result = []
                else:
                    more_result = find_entities(
                        user=get_current(),
                        metadata_filter={'content_types': ['proposal', 'idea'],
                                         'keywords': keywords},
                        sort_on='release_date')

                is_root = True
            else:
                more_result = find_more_contents(self.context)

            for index, obj in enumerate(more_result):
                objects.append(obj)
                if index > MORE_NB:
                    break

            if self.context in objects:
                objects.remove(self.context)

            objects = sorted(
                list(set(objects)),
                key=lambda e: getattr(e, 'release_date', e.modified_at),
                reverse=True)
        else:
            objects = []

        return {'contents': objects,
                'is_root': is_root,
                'request': self.request}


@panel_config(
    name='channels',
    context=Entity,
    renderer='templates/panels/channels.pt'
    )
class Channels(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _get_channels_bodies(self, root, user, channels, action_id):
        result_body = []
        for channel in channels:
            subject = channel.get_subject(user)
            actions_call, action_resources = update_all_ajax_action(
                subject, self.request, action_id)
            if actions_call:
                object_values = {
                    'object': channel,
                    'current_user': user,
                    'action_call': actions_call[0]}
                body = renderers.render(
                    channel.templates.get('default'),
                    object_values,
                    self.request)
                result_body.append(body)

        return result_body

    def __call__(self):
        user = get_current(self.request)
        result = {}
        users_result_body = []
        others_result_body = []
        general_result_body = []
        if self.request.user:
            root = getSite()
            general_channel = root.channel
            channels = getattr(user, 'following_channels', [])
            user_channel = [c for c in channels
                            if isinstance(c.__parent__, Person)]
            generals = [general_channel]
            others = [c for c in channels if c not in user_channel]
            users_result_body = self._get_channels_bodies(
                root, user, user_channel, 'discuss')
            others_result_body = self._get_channels_bodies(
                root, user, others, 'comment')
            general_result_body = self._get_channels_bodies(
                root, user, generals, 'general_discuss')
            general_result_body.extend(others_result_body)

        result.update({
            'users_channels': users_result_body,
            'others_channels': general_result_body,
        })
        return result


@panel_config(
    name='debatescore',
    context=SearchableEntity,
    renderer='templates/panels/debates_core.pt'
    )
class Debates_core(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        debatescore_data = {}
        if self.request.view_name == 'index' and \
           self.context.is_published and \
           isinstance(self.context, (Idea, Proposal)):
            debatescore_data = get_debatescore_data(
                self.context, self.request)

        return {'debatescore': debatescore_data}


@panel_config(
    name='navigation_bar',
    context=Entity,
    renderer='templates/panels/navigation_bar.pt'
    )
class NavigationBar(object):

    template_sub_menu = 'templates/panels/sub_menu.pt'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.default_folder = SmartFolder(title=_('My interests'),
                                          style=DEFAULT_FOLDER_COLORS,
                                          )
        self.default_folder.folder_order = -1

    def get_sub_menu(
        self, nodes, parent_name, current_level,
        active_folder, parent_active, parent_id):
        body = renderers.render(self.template_sub_menu,
                                {'nodes': nodes,
                                 'active_folder': active_folder,
                                 'parent_name': parent_name,
                                 'view': self,
                                 'current_level': current_level,
                                 'maxi_level': LEVEL_MENU,
                                 'is_active': parent_active,
                                 'parent_id': parent_id
                                },
                                self.request)
        return body

    def get_folder_parent(self, node):
        if node.parents:
            return node.parents[0]

        return self.default_folder

    def get_folder_children(self, node):
        user = get_current(self.request)
        locale = self.request.locale_name
        children = node.children if node is not self.default_folder\
            else self.default_folder.volatile_children
        nodes = [sf for sf in children if can_access(user, sf)
                 and (not sf.locale or sf.locale == locale)]
        nodes = sorted(nodes, key=lambda e: e.get_order())
        return nodes

    def get_folder_id(self, node):
        if node is self.default_folder:
            return None

        return get_oid(node)

    def get_folder_name(self, node):
        if node is self.default_folder:
            return 'default_folder'

        return normalize_title(node.name).replace(' ', '-')

    def __call__(self):
        nodes = find_entities(
            interfaces=[ISmartFolder],
            metadata_filter={'states': ['published']})
        active_folder_id = None
        active_folder = None
        if self.request.GET:
            active_folder_id = dict(self.request.GET._items).get('folderid', None)

        try:
            if active_folder_id:
                active_folder = get_obj(int(active_folder_id))
        except (TypeError, ValueError):
            active_folder = None

        locale = self.request.locale_name
        if self.request.user:
            my_folders = getattr(get_current(), 'folders', [])
            my_folders = [folder for folder in my_folders
                          if isinstance(folder, SmartFolder) and
                          'private' in folder.state and
                          not folder.parents]
            if my_folders:
                self.default_folder.volatile_children = my_folders

        nodes = [sf for sf in nodes
                 if not sf.parents and (not sf.locale or sf.locale == locale)]
        if getattr(self.default_folder, 'volatile_children', []):
            nodes.append(self.default_folder)

        nodes = sorted(nodes, key=lambda e: e.get_order())
        return {'nodes': nodes,
                'active_folder': active_folder,
                'view': self,
                'current_level': 1,
                'maxi_level': LEVEL_MENU
                }
