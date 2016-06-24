# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import pytz
import datetime
import colander
import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.schema import Schema
from pontus.view import BasicView
from pontus.default_behavior import Cancel

from novaideo.content.processes.ballot_processes.rangevoting.behaviors import (
    Vote)
from novaideo.content.proposal import Proposal
from novaideo import _


def define_date_node(schema):
    schema['vote'] = colander.SchemaNode(
            colander.DateTime(),
            widget=deform.widget.DateTimeInputWidget(),
            validator=colander.Range(min=datetime.datetime.now(tz=pytz.UTC),
                min_err=_('${val} is earlier than earliest datetime ${min}')),
            title=_('Date')
            )               
    

NODE_DEFINITION = {'date': define_date_node}


class VoteViewStudyReport(BasicView):
    title = _('Ballot report')
    name = 'ballotreport'
    template = 'novaideo:views/ballot_processes/referendum/templates/rangevoting_vote.pt'

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
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


class VoteSchema(Schema):

    vote = colander.SchemaNode(colander.String())
    

class VoteFormView(FormView):
    title =  _('Vote')
    name = 'voteform'
    formid = 'formvote'
    behaviors = [Vote]
    schema = VoteSchema()
    validate_behaviors = False

    def before_update(self):
        ballot_report = None
        vote_type = 'string'
        try:
            vote_actions = list(self.behaviors_instances.values())
            ballot_report = vote_actions[0].process.ballot.report
            vote_type = ballot_report.ballottype.subject_type_manager.vote_type
        except Exception:
            pass

        define_node_op = NODE_DEFINITION.get(vote_type, None)
        if define_node_op:
            define_node_op(self.schema)

        formwidget = deform.widget.FormWidget(css_class='vote-form')
        self.action = self.request.resource_url(
            self.context, 'rangevotingvote')
        self.schema.widget = formwidget
     

@view_config(
    name='rangevotingvote',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class VoteViewMultipleView(MultipleView):
    title = _('Vote')
    name = 'rangevotingvote'
    viewid = 'rangevotingvote'
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
