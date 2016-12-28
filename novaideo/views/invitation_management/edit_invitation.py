# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from dace.objectofcollaboration.principal.util import has_role

from novaideo.content.processes.invitation_management.behaviors import (
    EditInvitation)
from novaideo.content.invitation import InvitationSchema, Invitation
from novaideo import _


@view_config(
    name='editinvitation',
    context=Invitation,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditInvitationView(FormView):

    title = _('Edit the invitation')
    schema = select(InvitationSchema(editable=True),
                    ['title',
                     'user_title',
                     'roles',
                     'first_name',
                     'last_name',
                     'email',
                     'organization'])
    behaviors = [EditInvitation, Cancel]
    formid = 'formeditinvitation'
    name = 'editinvitation'

    def before_update(self):
        if not has_role(role=('Moderator',)):
            self.schema = select(InvitationSchema(editable=True),
                                 ['title',
                                  'user_title',
                                  'first_name',
                                  'last_name',
                                  'email'])

        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': EditInvitation.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')

    def default_data(self):
        return self.context

DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {EditInvitation: EditInvitationView})
