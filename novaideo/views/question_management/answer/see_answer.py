# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes.question_management.behaviors import (
    SeeAnswer)
from novaideo.content.question import Answer
from novaideo.utilities.util import render_listing_obj


@view_config(
    name='seeanswer',
    context=Answer,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeAnswerView(BasicView):
    title = ''
    name = 'seeanswer'
    viewid = 'seeanswer'
    behaviors = [SeeAnswer]
    template = 'novaideo:views/question_management/answer/templates/see_answer.pt'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    css_class = 'simple-bloc'
    container_css_class = 'home'

    def update(self):
        self.execute(None)
        user = get_current()
        answer_body = render_listing_obj(
            self.request, self.context, user)
        question_body = render_listing_obj(
            self.request, self.context.question, user)
        values = {
            'answer': self.context,
            'answer_body': answer_body,
            'question_body': question_body}
        result = {}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update({SeeAnswer: SeeAnswerView})
