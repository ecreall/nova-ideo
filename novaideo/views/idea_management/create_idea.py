# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import pytz
import datetime
from pyramid.view import view_config
from substanced.util import get_oid
from pyramid import renderers

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import get_obj
from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view import BasicView

from novaideo.utilities.util import (
    generate_listing_menu, ObjectRemovedException,
    DEFAUL_LISTING_ACTIONS_TEMPLATE, DEFAUL_LISTING_FOOTER_ACTIONS_TEMPLATE,
    DEFAUL_WG_LISTING_ACTIONS_TEMPLATE)
from novaideo.content.processes.idea_management.behaviors import (
    CreateIdea, CrateAndPublish, CrateAndPublishAsProposal)
from novaideo.content.idea import IdeaSchema, Idea
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.utilities.util import to_localized_time
from novaideo.content.processes import get_states_mapping


@view_config(
    name='createidea',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CreateIdeaView(FormView):

    title = _('Create an idea')
    schema = select(IdeaSchema(factory=Idea, editable=True),
                    ['title',
                     'text',
                     'keywords',
                     'attached_files'])
    behaviors = [CrateAndPublishAsProposal, CrateAndPublish, CreateIdea, Cancel]
    formid = 'formcreateidea'
    name = 'createidea'

    # def default_data(self):
    #     localizer = self.request.localizer
    #     user = get_current()
    #     time = to_localized_time(
    #         datetime.datetime.now(tz=pytz.UTC), translate=True)
    #     title = localizer.translate(_('Idea by'))+' '+\
    #             getattr(user, 'title', user.name)+' '+\
    #             localizer.translate(_('the'))+' '+\
    #             time+' (UTC)'
    #     return {'title': title}


@view_config(name='ideasmanagement',
             context=NovaIdeoApplication,
             xhr=True,
             renderer='json')
class CreateIdeaView_Json(BasicView):

    idea_template = 'novaideo:views/proposal_management/templates/idea_data.pt'
    behaviors = [CreateIdea, CrateAndPublishAsProposal, CrateAndPublish]

    # def _get_new_title(self, user):
    #     localizer = self.request.localizer
    #     time = to_localized_time(
    #         datetime.datetime.now(tz=pytz.UTC), translate=True)
    #     return localizer.translate(_('Idea by'))+' '+\
    #             getattr(user, 'title', user.name)+' '+\
    #             localizer.translate(_('the'))+' '+\
    #             time+' (UTC)'

    def _render_obj(self, obj, user):
        try:
            navbars = generate_listing_menu(
                self.request, obj,
                template=DEFAUL_LISTING_ACTIONS_TEMPLATE,
                footer_template=DEFAUL_LISTING_FOOTER_ACTIONS_TEMPLATE,
                wg_template=DEFAUL_WG_LISTING_ACTIONS_TEMPLATE
                )
        except ObjectRemovedException:
            return None

        render_dict = {'object': obj,
                       'current_user': user,
                       'menu_body': navbars['menu_body'],
                       'footer_body': navbars['footer_body'],
                       'wg_body': navbars['wg_body'],
                       'state': get_states_mapping(user, obj,
                               getattr(obj, 'state_or_none', [None])[0])}
        return self.content(args=render_dict,
                            template=obj.templates['default'])['body']

    def creat_home_idea(self):
        try:
            button = 'Create_an_idea' if 'Create_an_idea' in self.request.POST \
                else ('Create_and_publish' if 'Create_and_publish' in self.request.POST
                      else 'Create_a_working_group')
            add_idea_action = self.behaviors_instances[button]
            add_idea_view = DEFAULTMAPPING_ACTIONS_VIEWS[add_idea_action.__class__]
            add_idea_view_instance = add_idea_view(
                self.context, self.request, behaviors=[add_idea_action])
            add_idea_view_instance.viewid = 'formcreateideahome'
            add_idea_view_result = add_idea_view_instance()
            if add_idea_view_instance.finished_successfully:
                user = get_current()
                body = ''
                if button == 'Create_a_working_group':
                    proposal = user.working_groups[-1].proposal
                    body = self._render_obj(proposal, user)

                idea = user.ideas[-1]
                return {'state': True,
                        'body': body+self._render_obj(idea, user),
                        'new_title': ''}#self._get_new_title(user)}

        except Exception:
            return {'state': False}

        return {'state': False}

    def creat_idea(self):
        behavior = None
        try:
            behavior = self.behaviors_instances['Create_an_idea']
            values = {'title': self.params('title'),
                      'text': self.params('text'),
                      'keywords': self.params('keywords')}
            idea = Idea()
            idea.set_data(values)
            appstruct = {'_object_data': idea}
            behavior.execute(self.context, self.request, appstruct)
            oid = get_oid(idea)
            user = get_current()
            new_title = ''#self._get_new_title(user)
            data = {'title': idea.title,
                    'oid': str(oid),
                    'body': renderers.render(self.idea_template,
                                             {'idea': idea},
                                             self.request),
                    'new_title': new_title
                    }
            result = data
            return result
        except Exception:
            return {}

    def get_idea(self):
        try:
            oid = int(self.params('oid'))
            idea = get_obj(oid)
            data = {'title': idea.title,
                    'oid': str(oid),
                    'body': renderers.render(self.idea_template,
                                             {'idea': idea},
                                             self.request)
                    }
            result = data
            return result
        except Exception:
            return {}

    def __call__(self):
        operation_name = self.params('op')
        if operation_name is not None:
            operation = getattr(self, operation_name, None)
            if operation is not None:
                return operation()

        return {}


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CreateIdea: CreateIdeaView})

DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CrateAndPublish: CreateIdeaView})


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CrateAndPublishAsProposal: CreateIdeaView})
