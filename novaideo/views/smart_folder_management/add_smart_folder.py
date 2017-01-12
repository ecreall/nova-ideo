# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.smart_folder_management.behaviors import (
    AddSmartFolder)
from novaideo.content.smart_folder import (
    SmartFolderSchema, SmartFolder)
from novaideo.content.novaideo_application import (
    NovaIdeoApplication)
from novaideo import _


@view_config(
    name='addsmartfolder',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AddSmartFolderView(FormView):

    title = _('Create a topic of interest')
    schema = select(SmartFolderSchema(factory=SmartFolder, editable=True),
                    ['title',
                     'description',
                     'locale',
                     'view_type',
                     'icon_data',
                     # 'style',
                     'filters',
                     'contents'])
    behaviors = [AddSmartFolder, Cancel]
    formid = 'formaddsmartfolder'
    name = 'addsmartfolder'


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {AddSmartFolder: AddSmartFolderView})
