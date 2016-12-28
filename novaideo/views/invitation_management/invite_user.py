# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from pyramid.view import view_config

from dace.objectofcollaboration.principal.util import has_role
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import Schema, omit, select
from pontus.widget import Select2Widget, SequenceWidget, SimpleMappingWidget
from pontus.default_behavior import Cancel

from novaideo.content.processes.invitation_management.behaviors import (
    InviteUsers)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.content.invitation import InvitationSchema, Invitation
from novaideo import _

class InviteUsersSchema(Schema):

    invitations = colander.SchemaNode(
                colander.Sequence(),
                select(omit(InvitationSchema(factory=Invitation,
                                         editable=True,
                                         name='Invitation',
                                         widget=SimpleMappingWidget(css_class='object-well default-well')), 
                            ['_csrf_token_']), 
                       ['user_title', 'roles', 'first_name', 
                       'last_name','email']),
                widget=SequenceWidget(min_len=1),
                title=_('The invitations')
                )


def roles_choice(node, roles):
    values = [(i, _(i)) for i in roles]
    return Select2Widget(values=values, multiple=True)


@view_config(
    name='inviteusers',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class InviteUserView(FormView):

    title = _('Invite users')
    schema = InviteUsersSchema()
    behaviors = [InviteUsers, Cancel]
    formid = 'forminviteusers'
    name = 'inviteusers'

    def before_update(self):
        invitations_schema = self.schema.get('invitations').children[0]
        schema_instance = InvitationSchema()
        roles_node = invitations_schema.get('roles')
        if has_role(role=('Moderator',)):
            roles_node.widget = roles_choice(roles_node, 
                                ['Moderator', 'Member', 'Examiner'])
            organization_node = schema_instance.get('organization')
            ismanager_node = schema_instance.get('ismanager')
            invitations_schema.children.append(organization_node)
            invitations_schema.children.append(ismanager_node)
        else:
            invitations_schema.children.remove(roles_node)
            #roles_node.widget = roles_choice(roles_node, ['Member'])



DEFAULTMAPPING_ACTIONS_VIEWS.update({InviteUsers:InviteUserView})