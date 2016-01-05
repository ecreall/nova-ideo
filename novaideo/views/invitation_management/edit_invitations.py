# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.schema import select
from pontus.default_behavior import Cancel

from novaideo.content.processes.invitation_management.behaviors import (
    EditInvitations)
from novaideo.content.novaideo_application import (
    NovaIdeoApplicationSchema,
    NovaIdeoApplication)
from novaideo import _


@view_config(
    name='editinvitations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditInvitationsView(FormView):

    title = _('Edit invitations')
    schema = select(NovaIdeoApplicationSchema(editable=True),
                    [(u'invitations', ['title',
                                       'user_title',
                                       'roles',
                                       'first_name',
                                       'last_name',
                                       'organization'])])
    behaviors = [EditInvitations, Cancel]
    formid = 'formeditinvitations'
    name = 'editinvitations'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {EditInvitations: EditInvitationsView})
