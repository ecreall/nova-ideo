from pyramid.view import view_config

from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import CallSelectedContextsViews
from pontus.schema import select
from pontus.view import BasicView, View, merge_dicts, ViewError

from novaideo.content.processes.novaideo_view_manager.behaviors import  AnonymousLogIn
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


@view_config(
    name='anonymouslogIn',
    renderer='pontus:templates/view.pt',
    )
class AnonymousLogInView(BasicView):
    title = _('Log in access')
    name = 'anonymouslogIn'
    item_template = 'pontus:templates/subview_sample.pt'
    behaviors = [AnonymousLogIn]
    template = 'novaideo:views/novaideo_view_manager/templates/anonymous_login.pt'
    viewid = 'anonymouslogIn'


    def update(self):
        self.execute(None)        
        login_url = self.request.resource_url(self.request.context, '@@login')
        result = {}
        values = {}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['isactive'] = True
        result['coordinates'] = {self.coordinates:[item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({AnonymousLogIn:AnonymousLogInView})
