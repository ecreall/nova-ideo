# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from substanced.util import Batch

from dace.objectofcollaboration.principal.util import (
    get_current)
from dace.util import getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView

from novaideo.content.processes import get_states_mapping
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.content.processes.question_management.behaviors import SeeAnswer
from novaideo.content.question import Answer
from novaideo.utilities.util import (
    generate_navbars, ObjectRemovedException, render_listing_objs)
from novaideo import _


CONTENTS_MESSAGES = {
    '0': _(u"""no answer"""),
    '1': _(u"""one answer"""),
    '*': _(u"""${nember} answers""")
}


class AnswersView(BasicView):
    template = 'novaideo:views/novaideo_view_manager/templates/home.pt'
    wrapper_template = 'novaideo:views/templates/simple_wrapper.pt'
    empty_message = _("No answers")
    empty_icon = 'glyphicon glyphicon-user'

    def update(self):
        user = self.context
        objects = self.context.answers
        objects = sorted(
            objects,
            key=lambda e: len(e.votes_positive),
            reverse=True)
        url = self.request.resource_url(
            self.context, '@@seeanswer')
        batch = Batch(objects,
                      self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results-answers"
        result_body, result = render_listing_objs(
            self.request, batch, user)
        len_answers = batch.seqlen
        index = str(len_answers)
        if len_answers > 1:
            index = '*'

        self.title = _(CONTENTS_MESSAGES[index],
                       mapping={'nember': len_answers})
        values = {'bodies': result_body,
                  'batch': batch,
                  'empty_message': self.empty_message,
                  'empty_icon': self.empty_icon}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


@view_config(
    name='seeanswer',
    context=Answer,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeAnswerView(BasicView):
    title = ''
    name = 'seeanswer'
    behaviors = [SeeAnswer]
    template = 'novaideo:views/answer_management/templates/see_answer.pt'
    viewid = 'seeanswer'

    def update(self):
        self.execute(None)
        try:
            navbars = generate_navbars(self.request, self.context)
        except ObjectRemovedException:
            return HTTPFound(self.request.resource_url(getSite(), ''))

        user = get_current()
        answers_instance = AnswersView(self.context, self.request)
        answers_result = answers_instance.update()
        answers_body = answers_result['coordinates'][AnswersView.coordinates][0]['body']
        result = {}
        values = {
            'object': self.context,
            'state': get_states_mapping(
                user, self.context, self.context.state[0]),
            'current_user': user,
            'answers_body': answers_body,
            'answers_len': answers_instance.title,
            'navbar_body': navbars['navbar_body'],
            'actions_bodies': navbars['body_actions'],
            'footer_body': navbars['footer_body'],
            'support_actions_body': navbars['support_actions_body']
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = navbars['messages']
        item['isactive'] = navbars['isactive']
        result.update(navbars['resources'])
        result['coordinates'] = {self.coordinates: [item]}
        return result


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeAnswer: SeeAnswerView})
