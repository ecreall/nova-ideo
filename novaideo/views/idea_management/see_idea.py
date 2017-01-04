# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import (
    get_current, has_any_roles)
from pontus.view import BasicView
from pontus.view_operation import MultipleView

from novaideo.content.processes.idea_management.behaviors import SeeIdea
from novaideo.content.idea import Idea
from novaideo.content.processes import get_states_mapping
from novaideo.utilities.util import generate_navbars, ObjectRemovedException
from novaideo import _
from .compare_idea import CompareIdeaView
from .see_workinggroups import SeeRelatedWorkingGroupsView


class IdeaHeaderView(BasicView):
    name = 'ideaheader'
    viewid = 'ideaheader'
    behaviors = [SeeIdea]
    validate_behaviors = False
    template = 'novaideo:views/idea_management/templates/header_idea.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    title = _('Idea header')

    def _cant_publish_alert(self, actions, user):
        if not self.request.moderate_ideas and \
           'to work' in self.context.state and self.context.author is user:
            return not any(a.behavior_id == 'publish'
                           for a in actions.get('global-action', []))

        return False

    def _cant_submit_alert(self, actions, user):
        if self.request.moderate_ideas and \
           'to work' in self.context.state and self.context.author is user:
            return not any(a.behavior_id == 'submit'
                           for a in actions.get('global-action', []))

        return False

    def update(self):
        navbars = self.get_binding('navbars')
        root = self.get_binding('root')
        if navbars is None:
            return HTTPFound(self.request.resource_url(root, ''))

        user = self.get_binding('user')
        is_censored = self.get_binding('is_censored')
        to_hide = self.get_binding('to_hide')
        result = {}
        values = {
            'idea': self.context,
            'is_censored': is_censored,
            'to_hide': to_hide,
            'state': get_states_mapping(
                user, self.context, self.context.state[0]),
            'current_user': user,
            'cant_publish': self._cant_publish_alert(
                navbars['all_actions'], user),
            'cant_submit': self._cant_submit_alert(
                navbars['all_actions'], user),
            'navbar_body': navbars['navbar_body']
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = navbars['messages']
        item['isactive'] = navbars['isactive']
        result.update(navbars['resources'])
        result['coordinates'] = {self.coordinates: [item]}
        return result


class DetailIdeaView(BasicView):
    name = 'seeIdea'
    viewid = 'seeidea'
    behaviors = [SeeIdea]
    validate_behaviors = False
    view_icon = 'glyphicon glyphicon-eye-open'
    template = 'novaideo:views/idea_management/templates/see_idea.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    title = _('Details')

    def update(self):
        self.execute(None)
        navbars = self.get_binding('navbars')
        root = self.get_binding('root')
        if navbars is None:
            return HTTPFound(self.request.resource_url(root, ''))

        user = self.get_binding('user')
        to_hide = self.get_binding('to_hide')
        files = getattr(self.context, 'attached_files', [])
        files_urls = []
        for file_ in files:
            files_urls.append({'title': file_.title,
                               'url': file_.url})

        result = {}
        values = {
            'idea': self.context,
            'to_hide': to_hide,
            'text': self.context.text.replace('\n', '<br/>'),
            'current_user': user,
            'files': files_urls,
            'footer_body': navbars['footer_body']
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['isactive'] = True
        result['coordinates'] = {self.coordinates: [item]}
        return result


class SeeIdeaActionsView(MultipleView):
    name = 'seeiactionsdea'
    template = 'novaideo:views/templates/multipleview.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    css_class = 'integreted-tab-content'
    title = ''
    views = (DetailIdeaView, SeeRelatedWorkingGroupsView, CompareIdeaView,)

    def _activate(self, items):
        pass


@view_config(
    name='seeidea',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeIdeaView(MultipleView):
    name = 'seeidea'
    template = 'novaideo:views/templates/entity_multipleview.pt'
    title = ''
    views = (IdeaHeaderView, SeeIdeaActionsView)
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/compare_idea.js',
                                 'novaideo:static/js/comment.js']}
    validators = [SeeIdea.get_validator()]

    def bind(self):
        bindings = {}
        bindings['navbars'] = None
        try:
            navbars = generate_navbars(
                self.request, self.context)
            bindings['navbars'] = navbars
        except ObjectRemovedException:
            return

        bindings['user'] = get_current()
        bindings['root'] = getSite()
        bindings['is_censored'] = 'censored' in self.context.state
        bindings['to_hide'] = bindings['is_censored'] and not has_any_roles(
            user=bindings['user'],
            roles=(('Owner', self.context), 'Moderator'))
        setattr(self, '_bindings', bindings)


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeIdea: SeeIdeaView})
