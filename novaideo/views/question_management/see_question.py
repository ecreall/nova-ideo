# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from substanced.util import Batch, get_oid

from dace.processinstance.core import (
    ValidationError, Validator)
from dace.objectofcollaboration.principal.util import (
    get_current, has_any_roles)
from dace.util import getSite, find_catalog
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView
from pontus.util import merge_dicts
from pontus.view_operation import MultipleView

from novaideo.content.processes import get_states_mapping
from novaideo.core import BATCH_DEFAULT_SIZE
from novaideo.content.processes.question_management.behaviors import SeeQuestion
from novaideo.content.question import Question
from novaideo.utilities.util import (
    generate_navbars, ObjectRemovedException, render_listing_objs,
    render_listing_obj)
from novaideo import _
from novaideo.content.interface import IAnswer
from novaideo.views.filter import (
    get_filter, FILTER_SOURCES, merge_with_filter_view, find_entities)
from novaideo.views.filter.sort import (
    sort_view_objects)


CONTENTS_MESSAGES = {
    '0': _(u"""No answer"""),
    '1': _(u"""One answer"""),
    '*': _(u"""${nember} answers""")
}


@view_config(
    name='seeanswers',
    context=Question,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AnswersView(BasicView):
    name = 'seeanswers'
    viewid = 'seeanswers'
    template = 'novaideo:views/novaideo_view_manager/templates/home.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    view_icon = 'glyphicon glyphicon-saved'
    title = _('Answers')
    empty_message = _("No answer")
    empty_icon = 'glyphicon glyphicon-saved'
    selected_filter = [('temporal_filter', ['negation', 'created_date']),
                       'text_filter']

    def _add_filter(self, user):
        def source(**args):
            filters = [
                {'metadata_filter': {
                    'states': ['published'],
                    'interfaces': [IAnswer]}},
            ]
            # Answer is non a searchable element
            # we need add it to the args dict
            args['interfaces'] = [IAnswer]
            objects = find_entities(
                filters=filters,
                user=user,
                intersect=self._get_answers(user), **args)
            return objects

        url = self.request.resource_url(self.context,
                                        '@@novaideoapi')
        return get_filter(
            self, url=url,
            select=self.selected_filter,
            source=source)

    def _get_answers(self, user):
        dace_catalog = find_catalog('dace')
        container_oid = dace_catalog['containers_oids']
        return container_oid.any([get_oid(self.context)]).execute().ids

    def update(self):
        user = get_current()
        filter_form, filter_data = self._add_filter(user)
        args = merge_with_filter_view(self, {})
        args['request'] = self.request
        filters = [
            {'metadata_filter': {
                'states': ['published'],
                'interfaces': [IAnswer]}},
        ]
        # Answer is non a searchable element
        # we need add it to the args dict
        args['interfaces'] = [IAnswer]
        objects = find_entities(
            filters=filters,
            user=user,
            intersect=self._get_answers(user),
            **args)
        objects, sort_body = sort_view_objects(
            self, objects, ['answer'], user, 'nbsupport')
        url = self.request.resource_url(self.context, self.name)
        batch = Batch(objects, self.request,
                      url=url,
                      default_size=BATCH_DEFAULT_SIZE)
        batch.target = "#results-answers"
        len_answers = batch.seqlen
        index = str(len_answers) if len_answers <= 1 else '*'
        if not self.parent:
            self.title = _(CONTENTS_MESSAGES[index],
                           mapping={'nember': len_answers})
        elif index != '*':
            self.title = _('The answer')

        filter_data['filter_message'] = self.title
        filter_body = self.filter_instance.get_body(filter_data)
        result_body, result = render_listing_objs(
            self.request, batch, user)
        if filter_form:
            result = merge_dicts(
                {'css_links': filter_form['css_links'],
                 'js_links': filter_form['js_links']
                }, result)

        values = {'bodies': result_body,
                  'batch': batch,
                  'empty_message': self.empty_message,
                  'empty_icon': self.empty_icon,
                  'filter_body': filter_body,
                  'sort_body': sort_body}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['isactive'] = True
        result['coordinates'] = {self.coordinates: [item]}
        return result


class AnalyticsValidator(Validator):
    """The validor for the Analytics view"""

    @classmethod
    def validate(cls, context, request, **kw):
        if getattr(context, 'options', []):
            return True

        raise ValidationError(msg=_("Permission denied"))


class AnalyticsView(BasicView):
    name = 'seeanalyticsquestion'
    viewid = 'seeanalyticsquestion'
    validators = [AnalyticsValidator]
    template = 'novaideo:views/question_management/templates/analytics_question.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    view_icon = 'glyphicon glyphicon-stats'

    title = _('Analytics')
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/chartjs/Chart.js',
                                 'novaideo:static/js/analytics.js']}

    def update(self):
        result = {}
        values = {
            'object': self.context,
            'tab_id': self.viewid + self.coordinates
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        result = merge_dicts(self.requirements_copy, result)
        return result


class AnswersDetailsView(MultipleView):
    name = 'seeanswersdetails'
    viewid = 'seeanswersdetails'
    template = 'novaideo:views/templates/multipleview.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    css_class = 'integreted-tab-content question-details'
    title = ''
    views = (AnswersView, AnalyticsView)

    def _activate(self, items):
        pass


class SeeQuestionHeaderView(BasicView):
    title = ''
    name = 'seequestionheader'
    behaviors = [SeeQuestion]
    template = 'novaideo:views/question_management/templates/see_question.pt'
    wrapper_template = 'pontus:templates/views_templates/simple_view_wrapper.pt'
    viewid = 'seequestionheader'

    def update(self):
        self.execute(None)
        try:
            navbars = generate_navbars(self.request, self.context)
        except ObjectRemovedException:
            return HTTPFound(self.request.resource_url(getSite(), ''))

        user = get_current()
        is_censored = 'censored' in self.context.state
        dace_catalog = find_catalog('dace')
        container_oid = dace_catalog['containers_oids']
        answers = find_entities(
            interfaces=[IAnswer],
            user=user,
            add_query=container_oid.any([get_oid(self.context)]))
        len_answers = len(answers.ids)
        index = str(len_answers)
        if len_answers > 1:
            index = '*'

        answers_title = _(CONTENTS_MESSAGES[index],
                          mapping={'nember': len_answers})
        answer_body = None
        if self.context.answer:
            answer_body = render_listing_obj(
                self.request, self.context.answer, user)

        result = {}
        values = {
            'object': self.context,
            'state': get_states_mapping(
                user, self.context, self.context.state[0]),
            'current_user': user,
            'answers_title': answers_title,
            'navbar_body': navbars['navbar_body'],
            'actions_bodies': navbars['body_actions'],
            'footer_body': navbars['footer_body'],
            'support_actions_body': navbars['support_actions_body'],
            'answer_body': answer_body,
            'is_censored': is_censored,
            'to_hide': is_censored and not has_any_roles(
                user=user,
                roles=(('Owner', self.context), 'Moderator'))
        }
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        item['messages'] = navbars['messages']
        item['isactive'] = navbars['isactive']
        result.update(navbars['resources'])
        result['coordinates'] = {self.coordinates: [item]}
        return result


@view_config(
    name='seequestion',
    context=Question,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeQuestionView(MultipleView):
    name = 'seequestion'
    template = 'novaideo:views/templates/entity_multipleview.pt'
    title = ''
    views = (SeeQuestionHeaderView, AnswersDetailsView)
    validators = [SeeQuestion.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeQuestion: SeeQuestionView})


FILTER_SOURCES.update(
    {AnswersView.name: AnswersView})
