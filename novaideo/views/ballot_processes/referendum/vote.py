# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from pyramid.view import view_config
from pyramid import renderers

from dace.objectofcollaboration.entity import Entity
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.schema import Schema
from pontus.view import BasicView
from pontus.widget import RadioChoiceWidget

from novaideo.content.processes.ballot_processes.referendum.behaviors import (
    Vote)
from novaideo import _


class VoteViewStudyReport(BasicView):
    title = _('Ballot report')
    name = 'ballotreport'
    template = 'novaideo:views/ballot_processes/referendum/templates/referendum_vote.pt'

    def _get_ballot_description(self, ballot_process, ballot_report):
        template = getattr(ballot_report, 'description_template', None)
        process = None
        ballot_managers = ballot_process.involvers
        if ballot_managers:
            process = ballot_managers[0].attachedTo.process

        if template:
            return renderers.render(
                template,
                {'ballot_report': ballot_report,
                 'ballot_process': ballot_process,
                 'process': process,
                 'context': self.context},
                self.request)

        return ballot_report.description

    def update(self):
        result = {}
        ballot_report = None
        ballot_process = None
        try:
            voteform_view = self.parent.validated_children[1]
            voteform_actions = list(voteform_view.behaviors_instances.values())
            ballot_process = voteform_actions[0].process
            ballot_report = ballot_process.ballot.report
        except Exception:
            pass

        description = self._get_ballot_description(
            ballot_process, ballot_report)
        values = {
            'context': self.context,
            'ballot_report': ballot_report,
            'description': description}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


def vote_choice(ballot_report):
    values = [(True, getattr(ballot_report.ballottype,
                            'true_val', _('Against'))),
              (False, getattr(ballot_report.ballottype,
                             'false_val', _('In favour')))]
    return RadioChoiceWidget(values=values)


class VoteSchema(Schema):

    vote = colander.SchemaNode(
        colander.Boolean(false_val='False', true_val='True'),
        default=False,
        title=_('Options'),
        )


class VoteFormView(FormView):
    title = _('Vote')
    name = 'voteform'
    formid = 'formvote'
    behaviors = [Vote]
    schema = VoteSchema()
    validate_behaviors = False

    def before_update(self):
        ballot_report = None
        try:
            vote_actions = list(self.behaviors_instances.values())
            ballot_report = vote_actions[0].process.ballot.report
        except Exception:
            return

        vote_widget = vote_choice(ballot_report)
        self.schema.get('vote').widget = vote_widget
        self.schema.view = self

        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': Vote.node_definition.id,
                   'action_uid': getattr(vote_actions[0], '__oid__', '')})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform vote-form')


@view_config(
    name='referendumvote',
    context=Entity,
    renderer='pontus:templates/views_templates/grid.pt',
    layout='old'
    )
class VoteViewMultipleView(MultipleView):
    title = _('Vote')
    name = 'referendumvote'
    viewid = 'referendumvote'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
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


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {Vote: VoteViewMultipleView})
