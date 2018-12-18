# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
import deform
import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import Schema
from pontus.view import BasicView
from pontus.default_behavior import Cancel

from novaideo.content.processes.proposal_management.behaviors import (
    Participate)
from novaideo.content.proposal import Proposal
from novaideo.content.idea import anonymous_widget
from novaideo import _
from novaideo.views.core import update_anonymous_schemanode


class ParticipateBasicView(BasicView):
    title = _('Participate')
    name = 'participate'
    behaviors = [Participate]
    viewid = 'participate'

    def update(self):
        results = self.execute({})
        return results[0]


class ParticipateSchema(Schema):
    """Schema for ParticipateView"""

    anonymous = colander.SchemaNode(
        colander.Boolean(),
        widget=anonymous_widget,
        label=_('Remain anonymous'),
        description=_('Check this box if you want to remain anonymous.'),
        title='',
        missing=False,
        default=False
        )


@view_config(
    name='participate',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    layout='old'
    )
class ParticipateView(FormView):
    title = _('Participate')
    name = 'participate'
    formid = 'formparticipate'
    schema = ParticipateSchema()
    behaviors = [Participate, Cancel]

    def update(self):
        if getattr(self.request.root, 'anonymisation', False):
            return super(ParticipateView, self).update()

        return ParticipateBasicView(self.context, self.request).update()

    def before_update(self):
        self.schema = update_anonymous_schemanode(
            self.request.root, self.schema)
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Participate.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


DEFAULTMAPPING_ACTIONS_VIEWS.update({Participate:ParticipateView})
