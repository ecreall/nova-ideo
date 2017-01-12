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
from pontus.schema import select, Schema
from pontus.default_behavior import Cancel
from pontus.widget import AjaxSelect2Widget

from novaideo.content.processes.organization_management.behaviors import (
    RemoveMembers)
from novaideo.content.organization import Organization
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
                                    query={'op': 'find_organization_user'})
    return AjaxSelect2Widget(
        values=values,
        ajax_url=ajax_url,
        multiple=True,
        title_getter=title_getter)


class OrganizationSchema(Schema):
    """Schema for Organization"""

    members = colander.SchemaNode(
        colander.Set(),
        widget=members_choice,
        title=_('Members'),
        missing=[]
        )


@view_config(
    name='removemembers',
    context=Organization,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class RemoveMembersView(FormView):

    title = _('Remove Members')
    schema = select(OrganizationSchema(),
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
