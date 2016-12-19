# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.novaideo_file_management.behaviors import  (
    CreateFile)
from novaideo.content.file import FileSchema, FileEntity
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


@view_config(
    name='createfile',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CreateFileView(FormView):

    title = _('Create a document')
    schema = select(FileSchema(factory=FileEntity, editable=True),
                    ['title',
                     'text'])
    behaviors = [CreateFile, Cancel]
    formid = 'formcreatefile'
    name = 'createfile'


DEFAULTMAPPING_ACTIONS_VIEWS.update({CreateFile: CreateFileView})