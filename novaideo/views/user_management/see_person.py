import re
import colander
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.util import find_catalog
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite, allSubobjectsOfType
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView, ViewError, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI
from pontus.widget import CheckboxChoiceWidget, RichTextWidget
from pontus.schema import Schema
from pontus.form import FormView

from novaideo.content.processes.user_management.behaviors import  SeePerson
from novaideo.content.person import Person
from novaideo import _
from novaideo.views.novaideo_view_manager.search import SearchResultView


@view_config(
    name='seeperson',
    context=Person,
    renderer='pontus:templates/view.pt',
    )
class SeePersonView(BasicView):
    title = _('Details')
    name = 'seeperson'
    behaviors = [SeePerson]
    template = 'novaideo:views/user_management/templates/see_person.pt'
    viewid = 'seeperson'
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/novaideo.js']}


    def update(self):
        self.execute(None) 
        user = self.context
        ideas = [o for o in getattr(user, 'ideas', []) if o.actions]
        len_result = len(ideas)
        result_body = []
        result = {}
        for o in ideas:
            object_values = {'object':o, 'current_user':user}
            body = self.content(result=object_values, template=o.result_template)['body']
            result_body.append(body)
        values = {
                'bodies': result_body,
                'length': len_result
               }
        ideas_body = self.content(result=values, template=SearchResultView.template)['body']

        #TOTDO proposals...
        values = {'ideas': (result_body and ideas_body) or None,
                  'proposals':None,
                  'user': self.context}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        result  = merge_dicts(self.requirements_copy, result)
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeePerson:SeePersonView})

