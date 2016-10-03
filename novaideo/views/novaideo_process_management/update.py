# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
import colander
from pyramid.view import view_config

from pontus.schema import Schema
from pontus.widget import Select2Widget
from pontus.form import FormView
from pontus.default_behavior import Cancel
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite

from novaideo.content.processes.novaideo_process_management.behaviors import (
    Update)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


@colander.deferred
def processes_choice(node, kw):
    root = getSite()
    runtime = root['runtime']
    processes = [p for p in list(runtime.processes)
                 if getattr(p.definition, 'isUnique', False)]
    values = [(i.__name__, i.title) for i in processes]
    return Select2Widget(values=values,
                         create=False,
                         multiple=True)


class ProcessesSchema(Schema):

    processes = colander.SchemaNode(
        colander.Set(),
        widget=processes_choice,
        title=_('Processes to update'),
        )


@view_config(
    name='updateprocesses',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class UpdateView(FormView):

    title = _('Update processes')
    schema = ProcessesSchema()
    behaviors = [Update, Cancel]
    formid = 'formupdateprocesses'
    name = 'updateprocesses'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Update.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


DEFAULTMAPPING_ACTIONS_VIEWS.update({Update: UpdateView})
