# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
import deform
from pyramid.view import view_config
from bs4 import BeautifulSoup
import json

import html_diff_wrapper
from dace.util import get_obj
from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.schema import omit, Schema
from pontus.widget import RadioChoiceWidget
from pontus.file import OBJECT_OID
from pontus.default_behavior import Cancel

from novaideo.content.processes.ballot_processes.majorityjudgment.behaviors import (
    Vote)
from novaideo.content.proposal import Proposal
from novaideo import _, log
from novaideo.views.widget import InLineWidget, ObjectWidget


OMITED_TEXT_TAG = '[...]'


def _prune_text(text, tag_descriminator, attributes_descriminator):
    soup = BeautifulSoup(text)
    descriminators_tags = soup.find_all(tag_descriminator,
                                        attributes_descriminator)
    conserved_tags = []
    for tag in descriminators_tags:
        parents = []
        for source_tag in html_diff_wrapper.HTML_BLOCK_ELEMENTS:
            parents = tag.find_parents(source_tag)
            if parents and parents[0] not in conserved_tags:
                parent = parents[0]
                previous_string = None
                try:
                    previous_string = list(conserved_tags[-1].strings)[0]
                except Exception:
                    pass

                if parent.previous_sibling and \
                   parent.previous_sibling not in conserved_tags and \
                   (not previous_string or \
                    previous_string and previous_string != OMITED_TEXT_TAG):
                    new_p = soup.new_tag('p')
                    new_p.string = OMITED_TEXT_TAG
                    conserved_tags.append(new_p)

                conserved_tags.append(parent)
                break
            elif parents and parents[0] in conserved_tags:
                break

        if not parents:
            conserved_tags.append(tag)

    if conserved_tags:
        las_tag = conserved_tags[-1]
        next_sibling = las_tag.next_sibling
        if next_sibling and \
           (not hasattr(next_sibling, 'get') or \
           hasattr(next_sibling, 'get') and \
           'explanation-inline' not in las_tag.next_sibling.get('class', [])):
            new_p = soup.new_tag('p')
            new_p.string = OMITED_TEXT_TAG
            conserved_tags.append(new_p)

    return soup, conserved_tags


def get_trimed_amendment_text(text):
    soup, source_tags = _prune_text(text, 'span', {'id': 'explanation'})
    explanations_inline_tags = soup.find_all('span',
                                             {'class': 'explanation-inline'})
    source_tags.extend(explanations_inline_tags)
    soup.body.clear()
    for tag in source_tags:
        soup.body.append(tag)

    return html_diff_wrapper.soup_to_text(soup)


def get_trimed_proposal_text(text, amendments):
    merged_text = html_diff_wrapper.get_merged_diffs(
        text,
        amendments,
        {'id': 'modification',
         'class': 'text-removed'},
        {'id': 'modification',
         'class': 'glyphicon glyphicon-plus text-added'})
    soup, source_tags = _prune_text(
        merged_text, 'span', {'id': 'modification'})
    soup.body.clear()
    for tag in source_tags:
        soup.body.append(tag)

    return html_diff_wrapper.soup_to_text(soup)


class VoteViewStudyReport(BasicView):
    title = _('Vote on amendments')
    name = 'voteforamendments'
    template = 'novaideo:views/ballot_processes/majorityjudgment/templates/vote_for_amendments.pt'

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


def judgments_choice(report):
    judgments = report.ballottype.judgments
    judgments = sorted(judgments.keys(),
                       key=lambda o: judgments[o],
                       reverse=True)
    values = [(i, _(i)) for i in judgments]
    widget = RadioChoiceWidget(
        values=values, inline=True,
        template='novaideo:views/ballot_processes/majorityjudgment/templates/radio_choice.pt',
        item_css_class="majorityjudgment-choices")
    return widget


class CandidateSchema(Schema):

    judgment = colander.SchemaNode(
        colander.String(),
        title=_('Judgement')
        )


class CandidatesSchema(Schema):
    candidates = colander.SchemaNode(
        colander.Sequence(),
        omit(CandidateSchema(widget=ObjectWidget(),
                             editable=True,
                             name='candidate',
                             omit=['judgment']), ['_csrf_token_']),
        widget=InLineWidget(),
        title=_('Candidates')
        )


class VoteFormView(FormView):
    title = _('Vote')
    name = 'voteform'
    formid = 'formvote'
    behaviors = [Vote]
    validate_behaviors = False
    schema = CandidatesSchema()

    def before_update(self):
        ballot_report = None
        try:
            vote_action = list(self.behaviors_instances.values())[0]
            ballot_report = vote_action.process.ballot.report
        except Exception:
            return

        judgments_widget = judgments_choice(ballot_report)
        judgment_nd = self.schema.get('candidates').children[0].get('judgment')
        judgment_nd.widget = judgments_widget
        self.schema.get('candidates').children[0].editable = False
        self.schema.view = self
        formwidget = deform.widget.FormWidget(css_class='vote-form')
        self.action = self.request.resource_url(
            self.context, 'voteforamendments',
            query={'action_uid': getattr(vote_action, '__oid__', '')})
        self.schema.widget = formwidget

    def default_data(self):
        ballot_report = None
        try:
            vote_action = list(self.behaviors_instances.values())[0]
            ballot_report = vote_action.process.ballot.report
        except Exception:
            return

        self.subjects = ballot_report.subjects
        return {'candidates': ballot_report.subjects}

    def get_description(self, field, cstruct):
        description_template = 'novaideo:views/amendment_management/templates/description_amendments.pt'
        oid = cstruct[OBJECT_OID]
        current_user = get_current()
        try:
            subject = get_obj(int(oid))
            values = {'amendment': subject,
                      'is_proposal': False,
                      'current_user': current_user,
                      'field': field}
            if isinstance(subject, Proposal):
                amendments = [a.text for a in self.subjects
                              if not isinstance(a, Proposal)]
                values['text'] = get_trimed_proposal_text(
                    subject.text, amendments)
                values['is_proposal'] = True
            else:
                values['text'] = get_trimed_amendment_text(
                    getattr(subject, 'text_diff', ''))

            body = self.content(args=values,
                                template=description_template)['body']
            return body
        except Exception as e:
            log.exception(e)
            return '<dic class="has-error"></div>'


@view_config(
    name='voteforamendments',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class VoteViewMultipleView(MultipleView):
    title = _('Vote')
    name = 'voteforamendments'
    viewid = 'voteforamendments'
    template = 'pontus:templates/views_templates/simple_multipleview.pt'
    wrapper_template = 'novaideo:views/ballot_processes/templates/panel_item.pt'
    views = (VoteViewStudyReport, VoteFormView)
    validators = [Vote.get_validator()]
    requirements = {'css_links': ['novaideo:static/bootstrap-slider/dist/css/bootstrap-slider.min.css'],
                    'js_links': ['novaideo:static/js/explanation_amendment.js',
                                 'novaideo:static/bootstrap-slider/dist/bootstrap-slider.min.js']}

    def get_message(self):
        ballot_report = None
        try:
            voteform_view = self.validated_children[1]
            voteform_actions = list(voteform_view.behaviors_instances.values())
            ballot_report = voteform_actions[0].process.ballot.report
        except Exception:
            pass

        return ballot_report.ballot.title


DEFAULTMAPPING_ACTIONS_VIEWS.update({Vote: VoteViewMultipleView})
