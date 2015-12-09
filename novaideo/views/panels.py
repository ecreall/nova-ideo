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


from dace.objectofcollaboration.entity import Entity
from dace.util import (
    getBusinessAction, getSite, find_catalog, getAllBusinessAction)
from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from daceui.interfaces import IDaceUIAPI

from novaideo.content.processes.novaideo_view_manager.behaviors import(
    SeeMyContents,
    SeeMySelections,
    SeeMyParticipations,
    SeeMySupports)
# from novaideo.content.processes.proposal_management.behaviors import (
#     CreateProposal)
from novaideo.content.processes.idea_management.behaviors import CreateIdea
from novaideo.content.proposal import Proposal
from novaideo.content.idea import Idea
from novaideo.content.interface import IPerson, Iidea, IProposal
from novaideo.content.amendment import Amendment
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.core import _, SearchableEntity
from novaideo.content.processes import get_states_mapping
from novaideo.content.processes.user_management.behaviors import (
    global_user_processsecurity)
from novaideo.utilities.util import (
    get_actions_navbar,
    footer_navbar_body)
from novaideo.views.filter import find_entities, find_more_contents


MORE_NB = 20


USER_MENU_ACTIONS = {'menu1': [SeeMyContents, SeeMyParticipations],
                     'menu2': [SeeMySelections, SeeMySupports]}


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
        if isinstance(search_view_result, dict) and \
          'coordinates' in search_view_result:
            search_body = search_view_instance.render_item(
                    search_view_result['coordinates'][search_view_instance.coordinates][0],
                    search_view_instance.coordinates,
                    None)

        result = {}
        result['search_body'] = search_body
        result['view'] = self
        return result


@panel_config(
    name = 'usernavbar',
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
        actions_url = OrderedDict()
        for actionclass in self.navbar_actions:
            process_id, action_id = tuple(actionclass.node_definition.id.split('.'))
            action, view = _getaction(self, process_id, action_id)
            if None not in (action, view):
                actions_url[action.title] = {
                            'action': action,
                            'url': action.url(root),
                            'view_name': getattr(view,'name', None)}
            else:
                actions_url[actionclass.node_definition.title] = {
                            'action': None,
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

        dace_catalog = find_catalog('dace')
        states_index = dace_catalog['object_states']
        object_provides_index = dace_catalog['object_provides']
        query = object_provides_index.any((IPerson.__identifier__ ,)) & \
                states_index.notany(['deactivated']) 
        nb_person = query.execute().__len__()
        query = object_provides_index.any((Iidea.__identifier__ ,)) & \
                states_index.any(['published']) 
        nb_idea = query.execute().__len__()
        query = object_provides_index.any((IProposal.__identifier__ ,)) & \
                states_index.notany(['archived', 'draft']) 
        nb_proposal = query.execute().__len__()
        result = {}
        result['nb_person'] = nb_person
        result['nb_idea'] = nb_idea
        result['nb_proposal'] = nb_proposal
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
        if isinstance(self.context, Amendment):
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
            subprocess = process['work'].sub_processes[-1]
            [voters.extend(b.report.voters)
             for b in subprocess.amendments_ballots]
            voters = list(set(voters))
            ballot = subprocess.amendments_ballots[-1]
            today = datetime.datetime.now(tz=pytz.UTC)
            if ballot.finished_at is not None and ballot.finished_at > today:
                time_delta = ballot.finished_at - today
                time_delta = days_hours_minutes(time_delta)

            return renderers.render(self.step3_2_template,
                                    {'context':context,
                                     'working_group_states': working_group_states,
                                     'is_closed': is_closed,
                                     'duration': time_delta,
                                     'process': process,
                                     'ballot_report': ballot.report,
                                     'voters': voters},
                                    request)
        elif 'open to a working group' in context.state:
            participants_mini = getSite().participants_mini
            work_mode = getattr(context, 'work_mode', None)
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
            elif 'published' in context.state:
                result['current_step'] = 4
                result['step4_message'] = self._get_step4_informations(context,
                                                                   self.request)
            elif 'examined' in context.state:
                result['current_step'] = 5
                result['step5_message'] = self._get_step5_informations(context,
                                                                   self.request)                
            elif 'archived' not in context.state:
                result['current_step'] = 3
                result['step3_message'] = self._get_step3_informations(context,
                                                                   self.request)
            elif 'archived' in context.state:
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
            return [a for a in root.actions
                    if getattr(a.action, 'style', '') == 'button']

        actions_navbar = get_actions_navbar(
            actions_getter, self.request, ['footer-action'])
        return {'navbar_body': footer_navbar_body(
            self, self.context, actions_navbar)}


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
        actions = []
        for action_class, data in self.actions.items():
            item_actions = getAllBusinessAction(
                root,
                self.request,
                process_id=data[0],
                node_id=data[1])
            action = None
            if item_actions:
                action = item_actions[0]

            actions.append({'title': action_class.title,
                            'action': action,
                            'unavailable_link': getattr(
                                action_class, 'unavailable_link', None),
                            'order': getattr(action_class, 'style_order', 100),
                            'style_btn': data[2],
                            'style_picto': getattr(action_class,
                                                   'style_picto', '')})

        actions = sorted(actions, key=lambda e: e['order'])
        return {'items': actions}


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

        return {'request': self.request,
                'condition': True}


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
                more_result = find_entities(
                    user=get_current(),
                    metadata_filter={'content_types': ['proposal', 'idea'],
                                     'states': getattr(user, 'keywords', [])},
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
