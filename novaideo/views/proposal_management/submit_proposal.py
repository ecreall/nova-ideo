# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.entity import Entity
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.schema import Schema
from pontus.widget import Select2Widget, RadioChoiceWidget
from pontus.default_behavior import Cancel

from novaideo.content.processes.proposal_management.behaviors import (
    SubmitProposal)
from novaideo.content.proposal import Proposal
from novaideo import _



class SubmitProposalStudyReport(BasicView):
    title = _('Alert for submission')
    name = 'alertforexplanation'
    template ='novaideo:views/proposal_management/templates/alert_submit_proposal.pt'

    def update(self):
        result = {}
        not_published_ideas = [i for i in self.context.related_ideas.keys() \
                              if not('published' in i.state)]
        duration_ballot_report = None
        vp_ballot = None
        try:
            voteform_view = self.parent.validated_children[1]
            voteform_actions = list(voteform_view.behaviors_instances.values())
            duration_ballot_report = voteform_actions[0].process.\
                                           duration_configuration_ballot.\
                                           report
            vp_ballot = voteform_actions[0].process.\
                                           vp_ballot.\
                                           report
        except Exception:
            pass

        values = {'context': self.context, 
                  'duration_ballot_report': duration_ballot_report,
                  'vp_ballot_report': vp_ballot,
                  'ideas': not_published_ideas}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


def subjects_choice(ballot_report):
    subjects = ballot_report.subjects
    def get_title(ob):
        if isinstance(ob, Entity):
            return ob.title
        else:
            return _(ob)

    values = [(i, get_title(i)) for i in subjects]
    return Select2Widget(values=values)


@colander.deferred
def vote_choice(node, kw):
    values = [(True, _('Against')), (False, _('Favour'))]
    return RadioChoiceWidget(values=values)


class SubmitProposalSchema(Schema):

    vote = colander.SchemaNode(
        colander.Boolean(),
        widget=vote_choice,
        title=_('Options'),
        )

    elected = colander.SchemaNode(
            colander.String(),
            title=_('Choices'),
            default=[],
        )


class SubmitProposalFormView(FormView):
    title = _('Submit')
    name = 'formsubmitproposal'
    behaviors = [SubmitProposal, Cancel]
    viewid = 'formsubmitproposal'
    formid = 'submitproposalform'
    validate_behaviors = False
    schema = SubmitProposalSchema()

    def before_update(self):
        duration_ballot_report = None
        try:
            vote_action = list(self.behaviors_instances.values())[0]
            duration_ballot_report = vote_action.process.\
                                           duration_configuration_ballot.\
                                           report
        except Exception:
            return

        subjects_widget = subjects_choice(duration_ballot_report)
        self.schema.get('elected').widget = subjects_widget
        self.schema.view = self


@view_config(
    name='submitproposal',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SubmitProposalView(MultipleView):
    title = _('Publish the proposal')
    name = 'submitproposal'
    viewid = 'submitproposal'
    template = 'daceui:templates/mergedmultipleview.pt'
    views = (SubmitProposalStudyReport, SubmitProposalFormView)
    validators = [SubmitProposal.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({SubmitProposal:SubmitProposalView})
