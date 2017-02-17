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
from dace.processinstance.core import ValidationError
from dace.objectofcollaboration.entity import Entity
from dace.util import (
    getSite,
    find_catalog, getAllBusinessAction,
    get_obj)
from dace.objectofcollaboration.principal.util import get_current
from daceui.interfaces import IDaceUIAPI
from pontus.util import merge_dicts

from novaideo.utilities.util import (
    generate_listing_menu, ObjectRemovedException)
from novaideo.content.processes.novaideo_view_manager.behaviors import(
    SeeMyContents,
    SeeMySelections,
    SeeMyParticipations,
    SeeMySupports)
from novaideo.content.processes.idea_management.behaviors import CreateIdea
from novaideo.content.interface import (
    IPerson, Iidea, IProposal, ISmartFolder,
    IQuestion)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.core import SearchableEntity, can_access
from novaideo.content.processes.user_management.behaviors import (
    global_user_processsecurity)
from novaideo.utilities.util import (
    get_actions_navbar,
    render_navbar_body,
    deepcopy,
    FOOTER_NAVBAR_TEMPLATE,
    get_debatescore_data,
    get_action_view)
from novaideo.views.filter import find_entities, find_more_contents
from novaideo.contextual_help_messages import render_contextual_help
from novaideo.guide_tour import get_guide_tour_page
from novaideo.steps import steps_panels
from novaideo.content.idea import Idea
from novaideo.content.proposal import Proposal
from novaideo.content.smart_folder import SmartFolder
from novaideo.fr_lexicon import normalize_title
from novaideo.content.processes.challenge_management.behaviors import (
    SeeChallenge)
from novaideo.views.challenge_management.see_challenges import (
    SeeChallengesHomeView)
from novaideo.views.channel_management.see_channels import SeeChannels
from novaideo.views.challenge_management.see_challenge import get_contents_forms
from novaideo import _, log


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
        search_action, search_view = get_action_view('novaideoviewmanager',
                                                'search',
                                                self.request)
        search_view_instance = search_view(root, self.request,
                                           behaviors=[search_action])
        posted_formid = None
        if self.request.POST:
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
    name='addcontenthomeform',
    context=NovaIdeoApplication,
    renderer='templates/panels/addcontenthomeform.pt'
    )
class AddContent(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return get_contents_forms(self.request)


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
            process_id, action_id = tuple(
                actionclass.node_definition.id.split('.'))
            action, view = get_action_view(process_id, action_id, self.request)
            if None not in (action, view):
                actions_url[action.title] = {
                    'action': action,
                    'action_id': action_id,
                    'icon': action.style_picto,
                    'url': action.url(root),
                    'view_name': getattr(view, 'name', None)}
            else:
                actions_url[actionclass.node_definition.title] = {
                    'action': None,
                    'action_id': action_id,
                    'icon': actionclass.style_picto,
                    'url': None,
                    'view_name': getattr(view, 'name', None)}
        result = {}
        result['actions'] = actions_url
        result['view'] = self
        result['has_contextual_help'] = has_contextual_help
        result['is_root'] = root is self.context and \
            self.request.view_name in ('', 'index', '@@index')
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
        query = object_provides_index.any((IPerson.__identifier__,)) & \
            states_index.notany(['deactivated'])
        result['nb_person'] = query.execute().__len__()
        query = object_provides_index.any((Iidea.__identifier__,)) & \
            states_index.any(['published'])
        result['nb_idea'] = query.execute().__len__()
        query = object_provides_index.any((IQuestion.__identifier__,)) & \
            states_index.any(['published'])
        result['nb_question'] = query.execute().__len__()
        result['nb_proposal'] = 0
        if not getattr(self.request, 'is_idea_box', False):
            query = object_provides_index.any((IProposal.__identifier__,)) & \
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
        groups[group_id] = sorted(
            group, key=lambda e: getattr(e[1], 'style_order', 0))
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
        user = get_current()
        messages = render_contextual_help(
            self.request, self.context, user, self.request.view_name)
        return {'messages': messages}


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

    def __call__(self):
        result = {
            'condition': False
        }
        if self.request.user:
            channels_view = SeeChannels(self.context, self.request)
            try:
                channels_view_result = channels_view()
            except Exception as error:
                log.warning(error)
                return {'condition': False}

            channels = ''
            result = {'condition': True, 'css_links': [], 'js_links': []}
            if isinstance(channels_view_result, dict) and \
               'coordinates' in channels_view_result:
                search_render = channels_view_result['coordinates'][channels_view.coordinates][0]
                result['css_links'] = [c for c in channels_view_result['css_links']
                                       if c not in resources['css_links']]
                result['js_links'] = [c for c in channels_view_result['js_links']
                                      if c not in resources['js_links']]
                channels = channels_view.render_item(
                    search_render,
                    channels_view.coordinates,
                    None)

            result['channels'] = channels
            update_resources(self.request, result)

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
    context=NovaIdeoApplication,
    renderer='templates/panels/navigation_bar.pt'
    )
class NavigationBar(object):

    template_sub_menu = 'templates/panels/sub_menu.pt'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.default_folder = SmartFolder(title=_('My topics of interest'),
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


@panel_config(
    name='homepage',
    context=NovaIdeoApplication,
    renderer='templates/panels/homepage.pt'
    )
class Debates_core(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return {
            'is_homepage': self.request.view_name in ('index', ''),
            'picture': getattr(self.context, 'homepage_picture', None),
            'text': getattr(self.context, 'homepage_text', None)
        }


@panel_config(
    name='guide_tour',
    context=Entity,
    renderer='templates/panels/guide_tour.pt'
    )
class GuideTour(object):

    resources = {
        'css_links': ['novaideo:static/guideline/css/guideline.css'],
        'js_links': ['novaideo:static/guideline/js/guideline.js',
                     'novaideo:static/guideline/js/novaideoguideline.js']
    }

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        user = get_current()
        guide_tour_data = getattr(user, 'guide_tour_data', {})
        guide_state = guide_tour_data.get(
            'guide_state', 'first_start')
        if guide_state in ('pending', 'first_start'):
            page_resources = get_guide_tour_page(
                self.request, self.context, user, self.request.view_name)
            if page_resources:
                page_resources = merge_dicts(
                    self.resources, page_resources)
                page_resources['request'] = self.request
                # if user is not an anonymous
                if self.request.user:
                    root = getSite()
                    page_resources['update_url'] = self.request.resource_url(
                        root,
                        'novaideoapi', query={
                            'op': 'update_guide_tour_data'
                        })
                    guide = page_resources.get('guide', None)
                    page = page_resources.get('page', None)
                    if guide is not None and page is not None:
                        guide_data = guide_tour_data.get(
                            guide+'_'+page, {})
                        page_state = guide_data.get(
                            'page_state', 'pending')
                        if page_state == 'pending':
                            page_resources['guide'] = guide
                            page_resources['page'] = page
                            page_resources['guide_value'] = guide_data.get(
                                'guide', -1)
                            page_resources['page_value'] = guide_data.get(
                                'page', 0)
                            page_resources['guide_state'] = guide_state
                        else:
                            return {}

                return page_resources

        return {}


@panel_config(
    name='challenge',
    context=SearchableEntity,
    renderer='templates/panels/challenge.pt'
    )
class ChallengePanel(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        # TODO Add communication actions
        challenge = getattr(self.context, 'challenge', None)
        if challenge is None:
            return {}

        try:
            SeeChallenge.get_validator().validate(challenge, self.request)
        except ValidationError as error:
            return {}

        result = {
            'challenge': challenge,
            'current_user': get_current()}

        novaideo_index = find_catalog('novaideo')
        dace_catalog = find_catalog('dace')
        states_index = dace_catalog['object_states']
        object_provides_index = dace_catalog['object_provides']
        challenges = novaideo_index['challenges']
        query = challenges.any([challenge.__oid__]) & \
            object_provides_index.any((Iidea.__identifier__,)) & \
            states_index.any(['published'])
        result['nb_idea'] = query.execute().__len__()
        query = challenges.any([challenge.__oid__]) & \
            object_provides_index.any((IQuestion.__identifier__,)) & \
            states_index.any(['published'])
        result['nb_question'] = query.execute().__len__()
        result['nb_proposal'] = 0
        if not getattr(self.request, 'is_idea_box', False):
            query = challenges.any([challenge.__oid__]) & \
                object_provides_index.any((IProposal.__identifier__,)) & \
                states_index.notany(['archived', 'draft'])
            result['nb_proposal'] = query.execute().__len__()

        return result


@panel_config(
    name='challenges',
    context=NovaIdeoApplication,
    renderer='templates/panels/challenges.pt'
    )
class ChallengesPanel(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        is_homepage = self.request.view_name in ('index', '')
        if not is_homepage:
            return {'condition': False}

        challenges_view = SeeChallengesHomeView(self.context, self.request)
        try:
            challenges_view_result = challenges_view()
            if getattr(challenges_view, 'no_challenges', False):
                return {'condition': False}

        except Exception as error:
            log.warning(error)
            return {'condition': False}

        challenges = ''
        result = {'condition': True, 'css_links': [], 'js_links': []}
        if isinstance(challenges_view_result, dict) and \
           'coordinates' in challenges_view_result:
            search_render = challenges_view_result['coordinates'][challenges_view.coordinates][0]
            result['css_links'] = [c for c in challenges_view_result['css_links']
                                   if c not in resources['css_links']]
            result['js_links'] = [c for c in challenges_view_result['js_links']
                                  if c not in resources['js_links']]
            challenges = challenges_view.render_item(
                search_render,
                challenges_view.coordinates,
                None)

        result['challenges'] = challenges
        result['view'] = self
        update_resources(self.request, result)
        return result
