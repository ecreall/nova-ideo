# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import Schema

from novaideo.content.processes.amendment_management.behaviors import (
    DirectSubmitAmendment)
from novaideo.content.amendment import Amendment
from novaideo.widget import LimitedTextAreaWidget
from novaideo import _


class SubmitSchema(Schema):

    justification = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=600),
        widget=LimitedTextAreaWidget(rows=5, 
                                     cols=30, 
                                     limit=600),
        title=_("Justification")
        )


@view_config(
    name='directsubmitamendmentform',
    context=Amendment,
    renderer='pontus:templates/views_templates/grid.pt',
    layout='old'
    )
class DirectSubmitAmendmentFormView(FormView):
    title = _('Submit the amendment')
    schema = SubmitSchema()
    behaviors = [DirectSubmitAmendment, Cancel]
    formid = 'formdirectsubmitamendment'
    name = 'directsubmitamendmentform'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': DirectSubmitAmendment.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


DEFAULTMAPPING_ACTIONS_VIEWS.update({DirectSubmitAmendment: DirectSubmitAmendmentFormView})
