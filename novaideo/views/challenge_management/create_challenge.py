# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.challenge_management.behaviors import (
    CreateChallenge, CrateAndPublish)
from novaideo.content.challenge import ChallengeSchema, Challenge
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.views.core import update_anonymous_schemanode


@view_config(
    name='createchallenge',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CreateChallengeView(FormView):

    title = _('Create a challenge')
    schema = select(ChallengeSchema(factory=Challenge, editable=True, omit=('anonymous',)),
                    ['title',
                     'description',
                     'keywords',
                     'image',
                     'text',
                     'is_restricted',
                     'invited_users',
                     'deadline',
                     'attached_files',
                     'anonymous'])
    behaviors = [CrateAndPublish, CreateChallenge, Cancel]
    formid = 'formcreatechallenge'
    name = 'createchallenge'
    css_class = 'panel-transparent'

    def before_update(self):
        self.schema = update_anonymous_schemanode(
            self.request.root, self.schema)


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CreateChallenge: CreateChallengeView})
