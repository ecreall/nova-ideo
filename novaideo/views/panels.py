# -*- coding: utf8 -*-
from collections import OrderedDict
from pyramid_layout.panel import panel_config
from pyramid.location import lineage
from pyramid.security import has_permission
from pyramid import renderers
from pyramid_layout.layout import Structure

from dace.objectofcollaboration.entity import Entity
from dace.objectofcollaboration.principal.util import has_any_roles
from dace.util import getBusinessAction, getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS

from novaideo.content.processes.novaideo_view_manager.behaviors import(
    SeeMyIdeas,
    SeeMyContacts,
    SeeMyProposals,
    SeeMySelections,
    SeeMyParticipations,
    SeeMySupports)

from novaideo.content.processes.idea_management.behaviors import CreatIdea

user_menue_actions = {'menue1': [SeeMyIdeas, SeeMyProposals, SeeMyParticipations],
                      'menue2': [SeeMyContacts, SeeMySelections, SeeMySupports],
                      'menue3': [CreatIdea]} #TODO add CreatProposal...



@panel_config(name='usermenu',
              renderer='templates/panels/usermenu.pt')
def usermenu_panel(context, request):
    return {}


@panel_config(
    name = 'usernavbar',
    context = Entity ,
    renderer='templates/panels/navbar_view.pt'
    )
class UserNavBarPanel(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _getaction(self, process_id, action_id):
        root = getSite()
        actions = getBusinessAction(process_id, action_id, '', self.request, root)
        action = None
        view = None
        if actions is not None:
            action = actions[0]
            if action.__class__ in DEFAULTMAPPING_ACTIONS_VIEWS:
                view = DEFAULTMAPPING_ACTIONS_VIEWS[action.__class__]

        return action, view

    def _actions(self):
        root = getSite()
        search_action, search_view = self._getaction('novaideoviewmanager', 'search')
        search_view_instance = search_view(root, self.request, behaviors=[search_action])
        actions_url ={'menue1':OrderedDict(), 'menue2':OrderedDict(), 'menue3':OrderedDict()}
        for (menue, actions) in user_menue_actions.items():
            for actionclass in actions:
                process_id, action_id = tuple(actionclass.node_definition.id.split('.'))
                action, view = self._getaction(process_id, action_id)
                if not (None in (action, view)):
                    actions_url[menue][action.title] = action.url(root)
                else:
                    actions_url[menue][actionclass.node_definition.title] = None
  
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


    def __call__(self):
       return self._actions()
