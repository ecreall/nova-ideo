# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.question_management.behaviors import (
    OpposeAnswer, OpposeAnswerAnonymous)
from novaideo.content.question import Answer
from novaideo import _
from novaideo.views.core import ActionAnonymousView


@view_config(
    name='opposeanswer',
    context=Answer,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class OpposeAnswerView(BasicView):
    title = _('Oppose')
    name = 'opposeanswer'
    behaviors = [OpposeAnswer]
    viewid = 'opposeanswer'

    def update(self):
        results = self.execute(None)
        return results[0]


@view_config(
    name='opposeansweranonymous',
    context=Answer,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class OpposeAnswerAnonymousView(ActionAnonymousView):
    behaviors = [OpposeAnswerAnonymous]
    name = 'opposeansweranonymous'


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {OpposeAnswerAnonymous: OpposeAnswerAnonymousView})


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {OpposeAnswer: OpposeAnswerView})
