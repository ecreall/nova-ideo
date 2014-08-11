# -*- coding: utf8 -*-
from collections import OrderedDict
from pyramid_layout.panel import panel_config

from dace.objectofcollaboration.entity import Entity
from dace.util import getBusinessAction, getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.schema import select

from novaideo.content.processes.novaideo_view_manager.behaviors import(
    SeeMyIdeas,
    SeeMyContacts,
    SeeMyProposals,
    SeeMySelections,
    SeeMyParticipations,
    SeeMySupports)

from novaideo.content.processes.idea_management.behaviors import CreateIdea

user_menu_actions = {'menu1': [SeeMyIdeas, SeeMyProposals, SeeMyParticipations],
                     'menu2': [SeeMyContacts, SeeMySelections, SeeMySupports],
                     'menu3': [CreateIdea]}  #TODO add CreateProposal...


def _getaction(view, process_id, action_id):
    root = getSite()
    actions = getBusinessAction(process_id, action_id, '', view.request, root)
    action = None
    action_view = None
    if actions is not None:
        action = actions[0]
        if action.__class__ in DEFAULTMAPPING_ACTIONS_VIEWS:
            action_view = DEFAULTMAPPING_ACTIONS_VIEWS[action.__class__]

    return action, action_view


@panel_config(
    name='usermenu',
    context = Entity ,
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
        search_view_instance.viewid = search_view_instance.viewid + 'usermenu' 
        if self.request.POST:
            search_view_instance.postedform = self.request.POST.copy()
            self.request.POST.clear()

        search_view_instance.schema = select(search_view_instance.schema, ['text'])
        search_view_result = search_view_instance()
        search_body = ''
        if isinstance(search_view_result, dict) and 'coordinates' in search_view_result:
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
    context = Entity ,
    renderer='templates/panels/navbar_view.pt'
    )
class UserNavBarPanel(object):

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
        actions_url = {'menu1': OrderedDict(),
                       'menu2': OrderedDict(),
                       'menu3': OrderedDict()}
        for (menu, actions) in user_menu_actions.items():
            for actionclass in actions:
                process_id, action_id = tuple(actionclass.node_definition.id.split('.'))
                action, view = _getaction(self, process_id, action_id)
                if not (None in (action, view)):
                    actions_url[menu][action.title] = action.url(root)
                else:
                    actions_url[menu][actionclass.node_definition.title] = None

        if self.request.POST:
            search_view_instance.postedform = self.request.POST.copy()
            self.request.POST.clear()

        search_view_result = search_view_instance()
        search_body = ''
        if isinstance(search_view_result, dict) and 'coordinates' in search_view_result:
            search_body = search_view_instance.render_item(
                              search_view_result['coordinates'][search_view_instance.coordinates][0],
                              search_view_instance.coordinates,
                              None)

        result = {}
        result['actions'] = actions_url
        result['search_body'] = search_body
        result['view'] = self
        return result
