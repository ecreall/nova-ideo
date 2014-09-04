from pyramid.view import view_config

from substanced.util import Batch

from dace.util import getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView, merge_dicts

from novaideo.content.processes.proposal_management.behaviors import  EditAmendments
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.core import BATCH_DEFAULT_SIZE, can_access



amendments_messages = {'0': u"""Pas d'amendements""",
                      '1': u"""Voir l'amendement""",
                      '*': u"""Voir les {lenamendments} amendements"""}


@view_config(
    name='editamendments',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class EditAmendmentsView(BasicView):
    title = _('Edit amendments')
    name = 'editamendments'
    behaviors = [EditAmendments]
    template = 'novaideo:views/amendment_management/templates/edit_amendments.pt'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    viewid = 'editamendments'


    def update(self):
        self.execute(None)
        user = get_current()
        root = getSite()
        objects = [o for o in getattr( self.context, 'amendments', []) if not('deprecated' in o.state) and can_access(user, o, self.request, root)]
        len_result = len(objects)
        result_body = []
        result = {}
        for o in objects:
            editaction = None
            editactions = [a for a in o.actions if a.action.node_id == 'edit']
            if editactions:
                editaction = editactions[0]

            object_values = {'object': o, 'action': editaction, 'current_user': user}
            body = self.content(result=object_values,
                    template=o.result_template)['body']
            result_body.append(body)

        values = {'bodies': result_body,
                  'length': len_result,
                   }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result

    def get_message(self):
        root = getSite()
        user = get_current()
        amendments = [o for o in getattr( self.context, 'amendments', []) if not('deprecated' in o.state) and can_access(user, o, self.request, root)]
        lenamendments = len(amendments)
        index = str(lenamendments)
        if lenamendments>1:
            index = '*'
        message = (amendments_messages[index]).format(lenamendments=lenamendments)
        return message


DEFAULTMAPPING_ACTIONS_VIEWS.update({EditAmendments:EditAmendmentsView})
