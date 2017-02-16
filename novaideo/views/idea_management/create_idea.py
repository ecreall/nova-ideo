# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config
from substanced.util import get_oid
from pyramid import renderers

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import get_obj
from dace.objectofcollaboration.principal.util import get_current
from dace.objectofcollaboration.object import Object
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, omit
from pontus.view import BasicView

from novaideo.utilities.util import render_listing_obj
from novaideo.utilities.pseudo_react import (
    get_all_updated_data, get_components_data)
from novaideo.content.processes.idea_management.behaviors import (
    CreateIdea, CrateAndPublish, CrateAndPublishAsProposal)
from novaideo.content.idea import IdeaSchema, Idea
from novaideo.content.novaideo_application import NovaIdeoApplication
from ..filter import get_pending_challenges
from novaideo import _, log


@view_config(
    name='createidea',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CreateIdeaView(FormView):

    title = _('Create an idea')
    schema = select(IdeaSchema(factory=Idea, editable=True),
                    ['challenge',
                     'title',
                     'text',
                     'keywords',
                     'attached_files'])
    behaviors = [CrateAndPublishAsProposal, CrateAndPublish, CreateIdea, Cancel]
    formid = 'formcreateidea'
    name = 'createidea'

    def before_update(self):
        user = get_current(self.request)
        has_challenges = len(get_pending_challenges(user)) > 0
        if not has_challenges:
            self.schema = omit(
                self.schema, ['challenge'])

        if not getattr(self, 'is_home_form', False):
            self.action = self.request.resource_url(
                self.context, 'novaideoapi',
                query={'op': 'update_action_view',
                       'node_id': CreateIdea.node_definition.id})
            self.schema.widget = deform.widget.FormWidget(
                css_class='deform novaideo-ajax-form')
        else:
            self.action = self.request.resource_url(
                self.context, 'createidea')
            self.schema.widget = deform.widget.FormWidget(
                css_class='material-form deform')

    def bind(self):
        if getattr(self, 'is_home_form', False):
            return {'is_home_form': True}

        return {}


@view_config(name='ideasmanagement',
             context=Object,
             xhr=True,
             renderer='json')
class CreateIdeaView_Json(BasicView):

    idea_template = 'novaideo:views/proposal_management/templates/idea_data.pt'
    behaviors = [CreateIdea, CrateAndPublishAsProposal, CrateAndPublish]

    def creat_home_idea(self):
        try:
            view_name = self.params('source_path')
            view_name = view_name if view_name else ''
            is_mycontents_view = view_name.endswith('seemycontents')
            redirect = False
            for action_id in self.behaviors_instances:
                if action_id in self.request.POST:
                    button = action_id
                    break

            add_idea_action = self.behaviors_instances[button]
            add_idea_view = DEFAULTMAPPING_ACTIONS_VIEWS[add_idea_action.__class__]
            add_idea_view_instance = add_idea_view(
                self.context, self.request, behaviors=[add_idea_action])
            add_idea_view_instance.viewid = 'formcreateideahome'
            add_idea_view_result = add_idea_view_instance()
            if add_idea_view_instance.finished_successfully:
                result = get_components_data(
                    **get_all_updated_data(
                        add_idea_action, self.request, self.context, self,
                        view_data=(add_idea_view_instance, add_idea_view_result)
                    ))
                user = get_current()
                body = ''
                if button == 'Create_a_working_group':
                    redirect = True
                    proposal = user.working_groups[-1].proposal
                    if is_mycontents_view:
                        redirect = False
                        body = render_listing_obj(
                            self.request, proposal, user)

                if not redirect:
                    idea = user.ideas[-1]
                    if not is_mycontents_view and \
                       'published' not in idea.state:
                        redirect = True
                    else:
                        result['item_target'] = 'results_contents' \
                            if is_mycontents_view else 'results-idea'
                        body = body + render_listing_obj(
                            self.request, idea, user)

                if not redirect:
                    result['redirect_url'] = None

                result['new_obj_body'] = body
                result['status'] = True
                return result

        except Exception as error:
            log.warning(error)
            return {'status': False}

        return {'status': False}

    def creat_idea(self):
        behavior = None
        try:
            behavior = self.behaviors_instances['Create_an_idea']
            values = {'title': self.params('title'),
                      'text': self.params('text')}
            keywords = self.params('keywords')
            if not isinstance(keywords, (list, tuple)):
                keywords = [keywords]

            values['keywords'] = keywords
            challenge = self.params('challenge')
            if challenge:
                try:
                    challenge = get_obj(int(challenge))
                    values['challenge'] = challenge
                except:
                    pass

            idea = Idea()
            idea.set_data(values)
            appstruct = {'_object_data': idea}
            behavior.execute(self.context, self.request, appstruct)
            oid = get_oid(idea)
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
                    'body': renderers.render(
                        self.idea_template,
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
