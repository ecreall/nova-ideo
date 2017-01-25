# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.question_management.behaviors import (
    SupportQuestion, SupportQuestionAnonymous)
from novaideo.content.question import Question
from novaideo import _
from novaideo.views.core import ActionAnonymousView


@view_config(
    name='supportquestion',
    context=Question,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SupportQuestionView(BasicView):
    title = _('Support')
    name = 'supportquestion'
    behaviors = [SupportQuestion]
    viewid = 'supportquestion'

    def update(self):
        results = self.execute(None)
        return results[0]


@view_config(
    name='supportquestionanonymous',
    context=Question,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SupportQuestionAnonymousView(ActionAnonymousView):
    behaviors = [SupportQuestionAnonymous]
    name = 'supportquestionanonymous'


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SupportQuestionAnonymous: SupportQuestionAnonymousView})


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SupportQuestion: SupportQuestionView})
