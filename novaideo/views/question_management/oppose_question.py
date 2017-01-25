# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.question_management.behaviors import (
    OpposeQuestion, OpposeQuestionAnonymous)
from novaideo.content.question import Question
from novaideo import _
from novaideo.views.core import ActionAnonymousView


@view_config(
    name='opposequestion',
    context=Question,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class OpposeQuestionView(BasicView):
    title = _('Oppose')
    name = 'opposequestion'
    behaviors = [OpposeQuestion]
    viewid = 'opposequestion'

    def update(self):
        results = self.execute(None)
        return results[0]


@view_config(
    name='opposequestionanonymous',
    context=Question,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class OpposeQuestionAnonymousView(ActionAnonymousView):
    behaviors = [OpposeQuestionAnonymous]
    name = 'opposequestionanonymous'


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {OpposeQuestionAnonymous: OpposeQuestionAnonymousView})


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {OpposeQuestion: OpposeQuestionView})
