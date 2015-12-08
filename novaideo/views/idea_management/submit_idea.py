# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.default_behavior import Cancel

from novaideo.content.processes.idea_management.behaviors import SubmitIdea
from novaideo.content.idea import Idea
from novaideo import _


class SubmitIdeaViewStudyReport(BasicView):
    title = _('Alert for submission')
    name = 'alertforsubmission'
    template = 'novaideo:views/idea_management/templates/alert_idea_submission.pt'

    def update(self):
        result = {}
        values = {'context': self.context}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class SubmitIdeaView(FormView):
    title = _('Submit for publishing')
    name = 'submitideaform'
    formid = 'formsubmitidea'
    behaviors = [SubmitIdea, Cancel]
    validate_behaviors = False


@view_config(
    name='submitidea',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PublishIdeaViewMultipleView(MultipleView):
    title = _('Submit for publishing')
    name = 'submitidea'
    viewid = 'submitidea'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    views = (SubmitIdeaViewStudyReport, SubmitIdeaView)
    validators = [SubmitIdea.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SubmitIdea: PublishIdeaViewMultipleView})
