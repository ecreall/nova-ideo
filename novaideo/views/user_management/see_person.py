from pyramid.view import view_config

from substanced.util import Batch

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView, merge_dicts

from novaideo.content.processes.user_management.behaviors import  SeePerson
from novaideo.content.person import Person
from novaideo import _
from novaideo.views.novaideo_view_manager.search import SearchResultView
from novaideo.core import BATCH_DEFAULT_SIZE


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


    def update(self):
        self.execute(None)
        user = self.context
        objects = [o for o in getattr(user, 'ideas', []) if not('deprecated' in o.state)]# TODO (if o.actions) replace by an other test
        batch = Batch(objects, self.request, default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results_ideas"
        len_result = batch.seqlen
        result_body = []
        result = {}
        current_user = get_current()
        for o in batch:
            object_values = {'object': o, 'current_user': current_user}
            body = self.content(result=object_values,
                    template=o.result_template)['body']
            result_body.append(body)

        values = {'bodies': result_body,
                  'length': len_result,
                  'batch': batch
                  }
        ideas_body = self.content(result=values,
                template=SearchResultView.template)['body']

        #TODO proposals...
        values = {'ideas': (result_body and ideas_body) or None,
                  'proposals': None,
                  'user': self.context}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeePerson:SeePersonView})
