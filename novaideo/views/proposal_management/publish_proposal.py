# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
import colander
from pyramid.view import view_config

from dace.util import getSite
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.entity import Entity
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.schema import Schema, select
from pontus.widget import Select2Widget, RadioChoiceWidget
from pontus.default_behavior import Cancel

from novaideo.content.processes.proposal_management.behaviors import (
    PublishProposal)
from novaideo.content.proposal import Proposal
from novaideo import _


class PublishProposalStudyReport(BasicView):
    title = _('Alert for submission')
    name = 'alertforexplanation'
    template = 'novaideo:views/proposal_management/templates/alert_publish_proposal.pt'

    def update(self):
        result = {}
        root = getSite()
        modes = list(root.get_work_modes().keys())
        not_published_ideas = []
        if not self.request.moderate_ideas:
            not_published_ideas = [i for i in self.context.related_ideas
                                   if 'published' not in i.state]
        values = {'context': self.context,
                  'not_published_ideas': not_published_ideas,
                  'is_unique_choice': len(modes) == 1}

        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates: [item]}
        return result


def subjects_choice(ballot_report):
    subjects = ballot_report.subjects
    def get_title(ob):
        if isinstance(ob, Entity):
            return ob.title
        else:
            return _(ob)

    values = [(i, get_title(i)) for i in subjects]
    return Select2Widget(
        values=values,
        item_css_class='work-duration')


@colander.deferred
def mode_choice(node, kw):
    root = getSite()
    values = []
    modes = list(root.get_work_modes().items())
    modes = sorted(modes, key=lambda e: e[1].order)
    values = [(key, value.title) for key, value in modes]
    return RadioChoiceWidget(
        values=values,
        item_css_class='work-mode')


@colander.deferred
def mode_choice_default(node, kw):
    root = getSite()
    return root.get_default_work_mode().work_id


def vote_choice(ballot_report):
    values = [(True, getattr(ballot_report.ballottype,
                            'true_val', _('Against'))),
              (False, getattr(ballot_report.ballottype,
                             'false_val', _('In favour')))]
    return RadioChoiceWidget(values=values)


class PublishProposalSchema(Schema):

    vote = colander.SchemaNode(
        colander.Boolean(false_val='False', true_val='True'),
        default=False,
        title=_('Options'),
        )

    work_mode = colander.SchemaNode(
        colander.String(),
        widget=mode_choice,
        default=mode_choice_default,
        title=_('Work mode'),
        description=_('Choose the work mode')
        )

    elected = colander.SchemaNode(
        colander.String(),
        title=_('Duration of the amendment cycle'),
    )


class PublishProposalFormView(FormView):
    title = _('Submit')
    name = 'formpublishproposal'
    behaviors = [PublishProposal, Cancel]
    viewid = 'formpublishproposal'
    formid = 'publishproposalform'
    validate_behaviors = False
    schema = PublishProposalSchema()
    requirements = {'css_links': [],
                    'js_links': ['novaideo:static/js/proposal_management.js']}

    def before_update(self):
        if getattr(self.context.working_group, 'work_mode', None):
            self.schema = select(PublishProposalSchema(), ['vote', 'elected'])

        duration_ballot = self.context.working_group.duration_configuration_ballot
        vp_ballot = self.context.working_group.vp_ballot
        duration_ballot_report = duration_ballot.report if duration_ballot else None
        vp_ballot_report = vp_ballot.report if vp_ballot else None
        subjects_widget = subjects_choice(duration_ballot_report)
        elected_node = self.schema.get('elected')
        elected_node.title = getattr(duration_ballot_report.ballottype,
                                     'group_title', _('Choices'))
        group_default = getattr(duration_ballot_report.ballottype,
                                'group_default', None)
        if group_default:
            elected_node.default = group_default

        elected_node.widget = subjects_widget
        vote_widget = vote_choice(vp_ballot_report)
        self.schema.get('vote').widget = vote_widget
        self.schema.view = self
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': PublishProposal.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form publish-proposal-form')


@view_config(
    name='publishproposal',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class PublishProposalView(MultipleView):
    title = _("Improve the proposal or submit it as is")
    name = 'publishproposal'
    viewid = 'publishproposal'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    views = (PublishProposalStudyReport, PublishProposalFormView)
    validators = [PublishProposal.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {PublishProposal: PublishProposalView})
