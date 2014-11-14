
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.novaideo_abstract_process.behaviors import (
    SeeFile)
from novaideo.core import  FileEntity


@view_config(
    name='seefile',
    context=FileEntity,
    renderer='pontus:templates/view.pt',
    )
class SeeFileView(BasicView):
    title = ''
    name = 'seefile'
    behaviors = [SeeFile]
    template = 'novaideo:views/novaideo_abstract_process/templates/see_file.pt'
    viewid = 'seefile'


    def update(self):
        self.execute(None)
        result = {}
        values = {
                'file': self.context,
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeFile:SeeFileView})