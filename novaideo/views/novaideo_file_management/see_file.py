# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.processinstance.activity import ActionType
from pontus.view import BasicView

from novaideo.content.processes.novaideo_file_management.behaviors import (
    SeeFile)
from novaideo.core import  FileEntity


@view_config(
    name='seefile',
    context=FileEntity,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeFileView(BasicView):
    title = ''
    name = 'seefile'
    behaviors = [SeeFile]
    template = 'novaideo:views/novaideo_file_management/templates/see_file.pt'
    viewid = 'seefile'


    def update(self):
        self.execute(None)
        result = {}
        actions = [a for a in self.context.actions \
                   if a.action.actionType != ActionType.automatic]
        actions = sorted(actions, 
                        key=lambda a: getattr(a.action, 'style_order', 0))
        values = {'object': self.context,
                  'actions': actions}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeFile:SeeFileView})