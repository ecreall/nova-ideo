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
from pontus.view_operation import MultipleView

from novaideo.content.processes.challenge_management.behaviors import EditChallenge
from novaideo.content.challenge import ChallengeSchema, Challenge
from novaideo import _


class EditChallengeFormView(FormView):

    title = _('Edit the challenge')
    schema = select(ChallengeSchema(),
                    ['title',
                     'description',
                     'keywords',
                     'image',
                     'text',
                     'deadline',
                     'attached_files'])
    behaviors = [EditChallenge, Cancel]
    formid = 'formeditchallenge'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    name = 'editChallenge'

    def default_data(self):
        return self.context


@view_config(
    name='editchallenge',
    context=Challenge,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditChallengeView(MultipleView):
    title = _('Edit the challenge')
    name = 'editchallenge'
    wrapper_template = 'novaideo:views/templates/view_wrapper.pt'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (EditChallengeFormView, )
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/compare_challenge.js']}


DEFAULTMAPPING_ACTIONS_VIEWS.update({EditChallenge: EditChallengeView})
