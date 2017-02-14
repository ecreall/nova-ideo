# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import get_obj
from pontus.form import FormView
from pontus.schema import Schema
from pontus.default_behavior import Cancel
from pontus.widget import AjaxSelect2Widget

from novaideo.content.processes.challenge_management.behaviors import (
    AddMembers)
from novaideo.content.challenge import Challenge
from novaideo import _


@colander.deferred
def members_choice(node, kw):
    """"""
    context = node.bindings['context']
    request = node.bindings['request']
    values = []

    def title_getter(oid):
        author = None
        try:
            author = get_obj(int(oid))
        except Exception:
            return oid

        title = getattr(author, 'title', author.__name__)
        return title

    ajax_url = request.resource_url(context,
                                    '@@novaideoapi',
                                    query={'op': 'find_groups'})
    return AjaxSelect2Widget(
        values=values,
        ajax_url=ajax_url,
        ajax_item_template="related_item_template",
        multiple=True,
        title_getter=title_getter)


class AddMembersSchema(Schema):

    members = colander.SchemaNode(
        colander.Set(),
        widget=members_choice,
        title=_('Members'),
        missing=[]
        )


@view_config(
    name='addmembers',
    context=Challenge,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AddMembersView(FormView):

    title = _('Add Participants')
    schema = AddMembersSchema()
    behaviors = [AddMembers, Cancel]
    formid = 'formaddmembers'
    name = 'addmembers'

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': AddMembers.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


DEFAULTMAPPING_ACTIONS_VIEWS.update({AddMembers: AddMembersView})
