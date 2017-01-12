# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
from pyramid.view import view_config


from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, Schema
from pontus.widget import SelectWidget, SequenceWidget
from pontus.file import Object as ObjectType

from novaideo.content.processes.smart_folder_management.behaviors import (
    OrderSmartFolders)
from novaideo.content.novaideo_application import (
    NovaIdeoApplication)
from novaideo import _
from novaideo.views.filter import find_entities
from novaideo.content.interface import ISmartFolder


@colander.deferred
def folders_widget(node, kw):
    folders = node.bindings['folders']
    values = [(o, o.title)for o in folders]
    return SelectWidget(
        values=values,
        template='novaideo:views/templates/folder_select.pt')


@colander.deferred
def folder_seq_widget(node, kw):
    folders = node.bindings['folders']
    len_f = len(folders)
    return SequenceWidget(
        item_css_class="ordered-folder-seq",
        orderable=True,
        max_len=len_f,
        min_len=len_f)


class OrderSmartFoldersSchema(Schema):

    folders = colander.SchemaNode(
        colander.Sequence(),
        colander.SchemaNode(
            ObjectType(),
            widget=folders_widget,
            name=_("topic of interest")
            ),
        widget=folder_seq_widget,
        title=_('The topics of interests'),
        description=_('Drag and drop the topics of interests to be sorted')
        )


@view_config(
    name='ordersmartfolders',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class OrderSmartFoldersView(FormView):

    title = _('Sort')
    schema = select(OrderSmartFoldersSchema(),
                    ['folders'])
    behaviors = [OrderSmartFolders, Cancel]
    formid = 'formordersmartfolders'
    name = 'ordersmartfolders'

    def bind(self):
        user = get_current()
        folders = find_entities(
            user=user,
            interfaces=[ISmartFolder]
            )#states=['published'])
        folders = [sf for sf in folders if not sf.parents]
        folders = sorted(folders, key=lambda e: e.get_order())
        return {'folders': folders}

    def default_data(self):
        folders = self.schema.bindings['folders']
        return {'folders': folders}


DEFAULTMAPPING_ACTIONS_VIEWS.update({OrderSmartFolders: OrderSmartFoldersView})
