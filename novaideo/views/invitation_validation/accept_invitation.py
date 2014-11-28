# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform.widget
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import Schema

from novaideo.content.processes.invitation_validation.behaviors import (
    AcceptInvitation)
from novaideo.content.invitation import Invitation
from novaideo import _


class AcceptInvitationSchema(Schema):

    password = colander.SchemaNode(
        colander.String(),
        widget = deform.widget.CheckedPasswordWidget(),
        validator=colander.Length(min=3, max=100),
        )


@view_config(
    name='accept_invitation',
    context=Invitation,
    renderer='pontus:templates/view.pt',
    )
class AcceptInvitationView(FormView):

    title = _('Accept invitation users')
    schema = AcceptInvitationSchema()
    behaviors = [AcceptInvitation, Cancel]
    formid = 'formacceptinvitation'
    name = 'accept_invitation'


DEFAULTMAPPING_ACTIONS_VIEWS.update({AcceptInvitation:AcceptInvitationView})
