# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
import colander
from pyramid.view import view_config

from substanced.util import get_oid

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select, Schema
from pontus.default_behavior import Cancel
from pontus.widget import Select2Widget

from novaideo.content.processes.challenge_management.behaviors import (
    RemoveMembers)
from novaideo.content.challenge import Challenge
from novaideo import _


@colander.deferred
def members_choice(node, kw):
    """"""
    context = node.bindings['context']
    values = [(get_oid(m), m.title) for m in
              getattr(context, 'invited_users', [])]

    return Select2Widget(
        values=values,
        multiple=True)


class ChallengeSchema(Schema):
    """Schema for Challenge"""

    members = colander.SchemaNode(
        colander.Set(),
        widget=members_choice,
        title=_('Participants'),
        missing=[]
        )


@view_config(
    name='removemembers',
    context=Challenge,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class RemoveMembersView(FormView):

    title = _('Remove Participants')
    schema = select(ChallengeSchema(),
                    ['members'])
    behaviors = [RemoveMembers, Cancel]
    formid = 'formremovemembers'
    name = 'removemembers'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': RemoveMembers.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


DEFAULTMAPPING_ACTIONS_VIEWS.update({RemoveMembers: RemoveMembersView})
