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

from novaideo.content.processes.novaideo_view_manager.behaviors import  SeeMyParticipations
from novaideo.content.novaideo_application import NovaIdeoApplicationSchema, NovaIdeoApplication
from novaideo import _
from novaideo.content.interface import Iidea, IProposal, IPerson


@view_config(
    name='seemyparticipations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class SeeMyParticipationsView(BasicView):
    title = _('My participations')
    name = 'seemyparticipations'
    behaviors = [SeeMyParticipations]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seemyparticipations'
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/novaideo.js']}


    def update(self):
        self.execute(None) 
        user = get_current()
        objects = getattr(user, 'participations', [])
        len_result = len(objects)
        result_body = []
        for o in objects:
            object_values = {'object':o, 'current_user':user}
            body = self.content(result=object_values, template=o.result_template)['body']
            result_body.append(body)

        result = {}
        values = {
                'bodies': result_body,
                'length': len_result
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        result  = merge_dicts(self.requirements_copy, result)
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeMyParticipations:SeeMyParticipationsView})

