import re
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView, ViewError, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI

from novaideo.content.processes.novaideo_view_manager.behaviors import  SeeIdeas
from novaideo.content.novaideo_application import NovaIdeoApplicationSchema, NovaIdeoApplication
from novaideo import _


@view_config(
    name='seeideas',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class SeeIdeasView(BasicView):
    title = _('Ideas')
    name = 'seeideas'
    behaviors = [SeeIdeas]
    template = 'novaideo:views/novaideo_view_manager/templates/see_ideas.pt'
    viewid = 'seeideas'


    def update(self):
        self.execute(None)
        result = {}
        all_messages = {}
        isactive = False
        all_resources = {}
        all_resources['js_links'] = []
        all_resources['css_links'] = []
        all_idea_data = {'ideas':[]}
        dace_ui_api = get_current_registry().getUtility(IDaceUIAPI,'dace_ui_api')
        for idea in self.context.ideas:
            action_updated, messages, resources, actions = dace_ui_api._actions(self.request, idea)
            if action_updated and not isactive:
                isactive = True

            all_messages.update(messages)
            if resources is not None:
                if 'js_links' in resources:
                    all_resources['js_links'].extend(resources['js_links'])
                    all_resources['js_links'] = list(set(all_resources['js_links']))

                if 'css_links' in resources:
                    all_resources['css_links'].extend(resources['css_links'])
                    all_resources['css_links'] =list(set(all_resources['css_links']))

            state = None
            if idea.state:
                state = idea.state[0]

            idea_dic = { 
                'actions': actions,
                'url':self.request.resource_url(idea, '@@index'), 
                'description': idea.description,
                'keywords': idea.keywords,
                'title':idea.title,
                'state':state,
                'author': idea.author.name,
                'created_at': idea.created_at}
            all_idea_data['ideas'].append(idea_dic)
         
        all_idea_data['tabid'] = self.__class__.__name__+'IdeaActions'
        body = self.content(result=all_idea_data, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = all_messages
        item['isactive'] = isactive
        result['coordinates'] = {self.coordinates:[item]}
        result.update(all_resources)
        result  = merge_dicts(self.requirements_copy, result)
        return result



DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeIdeas:SeeIdeasView})
