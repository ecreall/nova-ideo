# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
import colander
from pyramid.view import view_config

from dace.util import getSite, get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.entity import Entity
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.schema import Schema, select
from pontus.widget import AjaxSelect2Widget, Select2Widget, RadioChoiceWidget
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
        item_css_class='publish-proposal-opt work-duration')


@colander.deferred
def mode_choice(node, kw):
    root = getSite()
    values = []
    modes = list(root.get_work_modes().items())
    modes = sorted(modes, key=lambda e: e[1].order)
    values = [(key, value.title) for key, value in modes]
    return RadioChoiceWidget(
        values=values,
        item_css_class='publish-proposal-opt work-mode')


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


@colander.deferred
def emails_validator(node, kw):
    new_emails = [e for e in kw if isinstance(e, str)]
    validator = colander.Email()
    for email in new_emails:
        validator(node, email)


@colander.deferred
def members_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = []
    ajax_url = request.resource_url(context,
                                    '@@novaideoapi',
                                    query={'op': 'find_user'})

    def title_getter(oid):
        try:
            obj = get_obj(int(oid), None)
            if obj:
                return obj.title
            else:
                return oid
        except Exception as e:
            log.warning(e)
            return oid

    return AjaxSelect2Widget(
        values=values,
        ajax_url=ajax_url,
        multiple=True,
        create=False,
        ajax_item_template="user_item_template",
        title_getter=title_getter,
        item_css_class='publish-proposal-opt'
        )


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

    members_to_invite = colander.SchemaNode(
        colander.Set(),
        widget=members_choice,
        validator=colander.All(emails_validator),
        title=_('Members to invite'),
        description= _('You can invite members to join the workgroup'),
        default=[],
        missing=[]
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
        root = getSite()
        if getattr(self.context.working_group, 'work_mode', None):
            self.schema = select(PublishProposalSchema(), ['vote', 'elected', 'members_to_invite'])

        can_submit_directly = getattr(root, 'can_submit_directly', False)
        if not can_submit_directly:
            self.schema = select(
                PublishProposalSchema(), ['work_mode', 'elected', 'members_to_invite'])

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
        if can_submit_directly:
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
    layout='old'
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
