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

from pontus.util import update_resources, merge_dicts
from dace.objectofcollaboration.entity import Entity
from dace.util import (
    getBusinessAction, getSite, find_catalog, getAllBusinessAction)
from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from daceui.interfaces import IDaceUIAPI

from novaideo.utilities.util import generate_listing_menu, ObjectRemovedException
from novaideo.content.processes.novaideo_view_manager.behaviors import(
    SeeMyContents,
    SeeMySelections,
    SeeMyParticipations,
    SeeMySupports)
# from novaideo.content.processes.proposal_management.behaviors import (
#     CreateProposal)
from novaideo.content.processes.idea_management.behaviors import CreateIdea
from novaideo.content.proposal import Proposal
from novaideo.content.workspace import Workspace
from novaideo.content.idea import Idea
from novaideo.content.person import Person
from novaideo.content.interface import IPerson, Iidea, IProposal
from novaideo.content.amendment import Amendment
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.core import _, SearchableEntity
from novaideo.content.processes import get_states_mapping
from novaideo.content.processes.user_management.behaviors import (
    global_user_processsecurity)
from novaideo.utilities.util import (
    get_actions_navbar,
    render_navbar_body,
    deepcopy,
    FOOTER_NAVBAR_TEMPLATE,
    update_all_modal_action)
from novaideo.views.filter import find_entities, find_more_contents


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

    def __call__(self):
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
                            'icon': action.style_picto,
                            'url': action.url(root),
                            'view_name': getattr(view,'name', None)}
            else:
                actions_url[actionclass.node_definition.title] = {
                            'action': None,
                            'icon': actionclass.style_picto,
                            'url': None,
                            'view_name': getattr(view,'name', None)}
        result = {}
        result['actions'] = actions_url
        result['view'] = self
        return result


@panel_config(
    name = 'novaideo_contents',
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


def days_hours_minutes(timed):
    return (timed.days, 
           timed.seconds//3600,
           (timed.seconds//60)%60, 
           timed.seconds%60)


@panel_config(
    name = 'steps',
    context =Entity,
    renderer='templates/panels/steps.pt'
    )
class StepsPanel(object):
    step1_0_template = 'novaideo:views/templates/panels/step1_0.pt'
    step2_0_template = 'novaideo:views/templates/panels/step2_0.pt'
    step3_0_template = 'novaideo:views/templates/panels/step3_0.pt'
    step3_1_template = 'novaideo:views/templates/panels/step3_1.pt'
    step3_2_template = 'novaideo:views/templates/panels/step3_2.pt'
    step3_3_template = 'novaideo:views/templates/panels/step3_3.pt'
    step4_0_template = 'novaideo:views/templates/panels/step4.pt'
    step5_0_template = 'novaideo:views/templates/panels/step5_0.pt'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _get_process_context(self):
        if isinstance(self.context, (Amendment, Workspace)):
            return self.context.proposal

        return self.context

    def _get_step1_informations(self, context, request):
        proposal_nember = len(list(dict(context.related_proposals).keys()))
        duplicates_len = len(context.duplicates)
        return renderers.render(self.step1_0_template,
                                {'context': context,
                                 'proposal_nember': proposal_nember,
                                 'duplicates_len': duplicates_len},
                                request)

    def _get_step2_informations(self, context, request):
        related_ideas = list(dict(context.related_ideas).keys())
        related_proposals = [list(dict(idea.related_proposals).keys())
                             for idea in related_ideas]
        related_proposals = [item for sublist in related_proposals
                             for item in sublist]
        related_proposals = list(set(related_proposals))
        len_related_proposals = len(related_proposals)
        if context in related_proposals:
            len_related_proposals -= 1

        return renderers.render(self.step2_0_template,
                                {'context': context,
                                 'proposal_nember': len_related_proposals},
                                request)

    def _get_step3_informations(self, context, request):
        time_delta = None
        working_group = context.working_group
        process = working_group.improvement_cycle_proc
        is_closed = 'closed' in working_group.state
        user = get_current()
        working_group_states = [_(get_states_mapping(user, working_group, s))
                                for s in working_group.state]
        if 'amendable' in context.state:
            subprocesses = process['work'].sub_processes
            date_iteration = None
            if subprocesses:
                date_iteration = subprocesses[-1]['timer'].eventKind.time_date

            today = datetime.datetime.now()
            if date_iteration is not None and date_iteration > today:
                time_delta = date_iteration - today
                time_delta = days_hours_minutes(time_delta)

            return renderers.render(self.step3_1_template,
                                    {'context':context,
                                     'working_group_states': working_group_states,
                                     'is_closed': is_closed,
                                     'duration': time_delta,
                                     'process': process},
                                    request)
        elif 'votes for publishing'  in context.state:
            ballot = working_group.vp_ballot
            today = datetime.datetime.now(tz=pytz.UTC)
            if ballot.finished_at is not None and ballot.finished_at > today:
                time_delta = ballot.finished_at - today
                time_delta = days_hours_minutes(time_delta)

            return renderers.render(self.step3_3_template,
                                    {'context': context, 
                                     'working_group_states': working_group_states,
                                     'is_closed': is_closed,
                                     'duration': time_delta,
                                     'process': process,
                                     'ballot_report': ballot.report},
                                    request)
        elif 'votes for amendments' in context.state:
            voters = []
            [voters.extend(b.report.voters)
             for b in working_group.amendments_ballots]
            voters = list(set(voters))
            ballot = working_group.amendments_ballots[-1]
            today = datetime.datetime.now(tz=pytz.UTC)
            if ballot.finished_at is not None and ballot.finished_at > today:
                time_delta = ballot.finished_at - today
                time_delta = days_hours_minutes(time_delta)

            return renderers.render(self.step3_2_template,
                                    {'context': context,
                                     'working_group_states': working_group_states,
                                     'is_closed': is_closed,
                                     'duration': time_delta,
                                     'process': process,
                                     'ballot_report': ballot.report,
                                     'voters': voters},
                                    request)
        elif 'open to a working group' in context.state:
            participants_mini = getSite().participants_mini
            work_mode = getattr(working_group, 'work_mode', None)
            if work_mode:
                participants_mini = work_mode.participants_mini

            return renderers.render(self.step3_0_template,
                                   {'context': context,
                                    'process': process,
                                    'min_members': participants_mini},
                                   request)

        return _('No more Information.')

    def _get_step4_informations(self, context, request):
        user = get_current()
        support = 0
        if any(t.owner is user for t in context.tokens_support):
            support = 1
        elif any(t.owner is user for t in context.tokens_opposition):
            support = -1

        return renderers.render(self.step4_0_template,
                                {'context': context,
                                 'support': support},
                                request)

    def _get_step5_informations(self, context, request):
        return renderers.render(self.step5_0_template,
                                    {'context': context},
                                    request)

    def __call__(self):
        if getattr(self.request, 'is_idea_box', False):
            return {'condition': False}

        result = {}
        context = self._get_process_context()
        result['condition'] = isinstance(context, (Proposal, Idea))
        result['current_step'] = 1
        result['step1_message'] = ""
        result['step2_message'] = ""
        result['step3_message'] = ""
        result['step4_message'] = ""
        result['step5_message'] = ""
        if isinstance(context, Proposal):
            if 'draft' in context.state:
                result['current_step'] = 2
                result['step2_message'] = self._get_step2_informations(context,
                                                                   self.request)
            elif 'proposal' in self.request.content_to_support and \
                 'submitted_support' in context.state:
                result['current_step'] = 4
                result['step4_message'] = self._get_step4_informations(context,
                                                                   self.request)
            elif 'proposal' in self.request.content_to_examine and\
                 'examined' in context.state:
                result['current_step'] = 5
                result['step5_message'] = self._get_step5_informations(context,
                                                                   self.request)
            elif not ('examined' in context.state or \
                      'submitted_support' in context.state or\
                      'archived' in context.state):
                result['current_step'] = 3
                result['step3_message'] = self._get_step3_informations(context,
                                                                   self.request)
            elif 'examined' in context.state or \
                 'submitted_support' in context.state or\
                 'archived' in context.state:
                result['current_step'] = 0

        if isinstance(context, Idea):
            result['step1_message'] = self._get_step1_informations(context,
                                                                   self.request)

        return result


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
        resources = deepcopy(getattr(
            self.request, 'resources', {'js_links': [], 'css_links': []}))
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
        result['css_links'] = [c for c in navbars['resources'].get('css_links', [])
                               if c not in resources['css_links']]
        result['js_links'] = [c for c in navbars['resources'].get('js_links', [])
                              if c not in resources['js_links']]
        update_resources(self.request, result)
        return result
        # actions = []
        # for action_class, data in self.actions.items():
        #     item_actions = getAllBusinessAction(
        #         root,
        #         self.request,
        #         process_id=data[0],
        #         node_id=data[1])
        #     action = None
        #     if item_actions:
        #         action = item_actions[0]

        #     actions.append({'title': action_class.title,
        #                     'action': action,
        #                     'unavailable_link': getattr(
        #                         action_class, 'unavailable_link', None),
        #                     'order': getattr(action_class, 'style_order', 100),
        #                     'style_btn': data[2],
        #                     'style_picto': getattr(action_class,
        #                                            'style_picto', '')})

        # actions = sorted(actions, key=lambda e: e['order'])
        # return {'items': actions}


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
        if not global_user_processsecurity(None, root):
            return {'error': True}

        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,
                                                        'dace_ui_api')
        actions = dace_ui_api.get_actions([root], self.request)
        admin_actions = [a for a in actions
                         if getattr(a[1], 'style_descriminator', '') ==
                         'admin-action']
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

from novaideo.contextual_help_messages import CONTEXTUAL_HELP_MESSAGES

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
        messages = [CONTEXTUAL_HELP_MESSAGES.get((self.context.__class__,
                                                  s, self.request.view_name),
                                                 None)
                    for s in self.context.state]
        messages.append(CONTEXTUAL_HELP_MESSAGES.get(
                        (self.context.__class__, 'any', self.request.view_name),
                        None))
        messages = [m for m in messages if m is not None]
        messages = [item for sublist in messages for item in sublist]
        messages = sorted(messages, key=lambda m: m[2])
        messages = [renderers.render(m[1],
                      {'context': self.context,
                       'user': user},
                      self.request) for m in messages
                    if m[0] is None or m[0](self.context, user)]
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
                                         'keywords': getattr(user, 'keywords', [])},
                        sort_on='modified_at', reverse=True)

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
        resources = {'css_links': [], 'js_links': []}
        for channel in channels:
            subject = channel.get_subject(user)
            actions_call, action_resources = update_all_modal_action(
                subject, self.request, action_id)
            resources = merge_dicts(action_resources, resources)
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

        return result_body, resources

    def __call__(self):
        user = get_current(self.request)
        result = {
            'css_links': [],
            'js_links': []}
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
            resources = deepcopy(getattr(
                self.request, 'resources', {'js_links': [], 'css_links': []}))
            users_result_body, users_resources = self._get_channels_bodies(
                root, user, user_channel, 'discuss')
            others_result_body, others_resources = self._get_channels_bodies(
                root, user, others, 'comment')
            general_result_body, general_resources = self._get_channels_bodies(
                root, user, generals, 'general_discuss')
            general_result_body.extend(others_result_body)
            result['css_links'] = [c for c in users_resources['css_links']
                                   if c not in resources['css_links']]
            result['js_links'] = [c for c in users_resources['js_links']
                                  if c not in resources['js_links']]
            result['css_links'] = [c for c in others_resources['css_links']
                                   if c not in resources['css_links']]
            result['js_links'] = [c for c in others_resources['js_links']
                                  if c not in resources['js_links']]
            result['css_links'] = [c for c in general_resources['css_links']
                                   if c not in resources['css_links']]
            result['js_links'] = [c for c in general_resources['js_links']
                                  if c not in resources['js_links']]
            update_resources(self.request, result)

        result.update({
            'users_channels': users_result_body,
            'others_channels': general_result_body,
        })
        return result
