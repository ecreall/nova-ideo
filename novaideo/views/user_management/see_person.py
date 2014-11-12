
from pyramid.view import view_config

from substanced.util import Batch

from dace.util import getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView

from novaideo.content.processes.user_management.behaviors import  SeePerson
from novaideo.content.person import Person
from novaideo.views.novaideo_view_manager.search import SearchResultView
from novaideo.core import BATCH_DEFAULT_SIZE, can_access
from novaideo.content.processes import get_states_mapping


@view_config(
    name='seeperson',
    context=Person,
    renderer='pontus:templates/view.pt',
    )
class SeePersonView(BasicView):
    title = ''
    name = 'seeperson'
    behaviors = [SeePerson]
    template = 'novaideo:views/user_management/templates/see_person.pt'
    viewid = 'seeperson'


    def update(self):
        self.execute(None)
        user = self.context
        current_user = get_current()
        actions = [a for a in self.context.actions \
                   if getattr(a.action, 'style', '') == 'button']
        objects = []
        if current_user is  user:
            objects = [o for o in getattr(user, 'contents', []) \
                      if not('archived' in o.state)]
        else:
            objects = [o for o in getattr(user, 'contents', []) \
                      if not('archived' in o.state) and\
                         can_access(current_user, o)]
      
        batch = Batch(objects, self.request, default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_contents"
        len_result = batch.seqlen
        result_body = []
        result = {}
        for obj in batch:
            object_values = {'object': obj, 
                             'current_user': current_user, 
                             'state': get_states_mapping(current_user, obj, 
                                   getattr(obj, 'state', [None])[0])
                             }
            body = self.content(result=object_values,
                    template=obj.result_template)['body']
            result_body.append(body)

        values = {'bodies': result_body,
                  'length': len_result,
                  'batch': batch
                  }
        contents_body = self.content(result=values,
                template=SearchResultView.template)['body']

        values = {'contents': (result_body and contents_body) or None,
                  'proposals': None,
                  'user': self.context,
                  'state': get_states_mapping(current_user, user, 
                                getattr(user, 'state', [None])[0]), 
                  'actions': actions}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeePerson:SeePersonView})