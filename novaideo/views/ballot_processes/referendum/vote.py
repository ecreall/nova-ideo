# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.schema import Schema
from pontus.view import BasicView
from pontus.widget import RadioChoiceWidget

from novaideo.content.processes.ballot_processes.referendum.behaviors import (
    Vote)
from novaideo.content.proposal import Proposal
from novaideo import _



class VoteViewStudyReport(BasicView):
    title = _('Ballot report')
    name = 'ballotreport'
    template = 'novaideo:views/ballot_processes/referendum/templates/referendum_vote.pt'

    def update(self):
        result = {}
        ballot_report = None
        try:
            voteform_view = self.parent.validated_children[1]
            voteform_actions = list(voteform_view.behaviors_instances.values())
            ballot_report = voteform_actions[0].process.ballot.report
        except Exception:
            pass

        values = {'context': self.context, 'ballot_report': ballot_report}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


@colander.deferred
def vote_choice(node, kw):
    values = [(True, _('Favour')), (False, _('Against'))]
    return RadioChoiceWidget(values=values)


class VoteSchema(Schema):

    vote = colander.SchemaNode(
        colander.Boolean(),
        widget=vote_choice,
        title=_('Options'),
        )
    

class VoteFormView(FormView):
    title =  _('Vote')
    name = 'voteform'
    formid = 'formvote'
    behaviors = [Vote]
    schema = VoteSchema()
    validate_behaviors = False


@view_config(
    name='referendumvote',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class VoteViewMultipleView(MultipleView):
    title = _('Vote')
    name = 'referendumvote'
    viewid = 'referendumvote'
    template = 'daceui:templates/simple_mergedmultipleview.pt'
    wrapper_template = 'novaideo:views/ballot_processes/templates/panel_item.pt'
    views = (VoteViewStudyReport, VoteFormView)
    validators = [Vote.get_validator()]

    def get_message(self):
        ballot_report = None
        try:
            voteform_view = self.validated_children[1]
            voteform_actions = list(voteform_view.behaviors_instances.values())
            ballot_report = voteform_actions[0].process.ballot.report
        except Exception:
            pass

        return ballot_report.ballot.title


DEFAULTMAPPING_ACTIONS_VIEWS.update({Vote:VoteViewMultipleView})
