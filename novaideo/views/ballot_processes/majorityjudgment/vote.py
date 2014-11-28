# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry
from bs4 import BeautifulSoup

from dace.util import get_obj, getBusinessAction
from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.schema import omit, Schema
from pontus.widget import RadioChoiceWidget
from pontus.file import OBJECT_OID

from novaideo.content.processes.ballot_processes.majorityjudgment.behaviors import (
    Vote)
from novaideo.content.proposal import Proposal
from novaideo import _
from novaideo.views.widget import InLineWidget, ObjectWidget
from novaideo.utilities.text_analyzer import ITextAnalyzer


SOURCE_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table']

class VoteViewStudyReport(BasicView):
    title = _('Vote for amendments')
    name = 'voteforamendments'
    template = 'novaideo:views/ballot_processes/majorityjudgment/templates/vote_for_amendments.pt'

    def update(self):
        result = {}
        ballot_report = None
        try:
            ballot_report = list(self.parent.children[1].behaviorinstances.values())[0].process.ballot.report
        except Exception:
            pass

        values = {'context': self.context, 'ballot_report': ballot_report}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


def judgments_choice(report):
    judgments = report.ballottype.judgments
    judgments = sorted(judgments.keys(), 
                       key=lambda o: judgments[o], 
                       reverse=True )
    values = [(i, _(i)) for i in judgments]
    widget = RadioChoiceWidget(values=values, inline=True)
    return widget


class CandidateSchema(Schema):

    judgment = colander.SchemaNode(
        colander.String(),
        title=_('Judgment')
        )
    
class CandidatesSchema(Schema):
    candidates =  colander.SchemaNode(
        colander.Sequence(),
        omit(CandidateSchema(widget=ObjectWidget(), 
                             editable=True, 
                             name='candidate', 
                             omit=['judgment']),['_csrf_token_']),
        widget=InLineWidget(),
        title=_('Candidates')
        )

class VoteFormView(FormView):
    title =  _('Vote')
    name = 'voteform'
    formid = 'formvote'
    behaviors = [Vote]
    validate_behaviors = False
    schema = CandidatesSchema()

    def before_update(self):
        ballot_report = None
        try:
            ballot_report = list(self.behaviorinstances.values())[0].process.ballot.report
        except Exception:
            return

        judgments_widget = judgments_choice(ballot_report)
        judgment_nd = self.schema.get('candidates').children[0].get('judgment')
        judgment_nd.widget = judgments_widget
        self.schema.get('candidates').children[0].editable = False
        self.schema.view = self

    def default_data(self):
        ballot_report = None
        try:
            ballot_report = list(self.behaviorinstances.values())[0].process.ballot.report
        except Exception:
            return
        
        return {'candidates': ballot_report.subjects}

    def _get_trimed_modification_text(self, text):
        soup = BeautifulSoup(text)
        explanations_tags = soup.find_all('span', {'id':'explanation'})
        source_tags = []
        for tag in explanations_tags:
            parents = []
            for source_tag in SOURCE_TAGS:
                parents = tag.find_parents(source_tag)
                if parents:
                    source_tags.append(parents[0])
                    break

            if not parents:
                source_tags.append(tag)

        explanations_inline_tags = soup.find_all('span', {'class':'explanation-inline'})
        source_tags.extend(explanations_inline_tags)
        soup.body.clear()
        for tag in source_tags:
            soup.body.append(tag)

        text_analyzer = get_current_registry().getUtility(ITextAnalyzer,
                                                          'text_analyzer')
        return text_analyzer.soup_to_text(soup)

    def _get_trimed_proposal_text(self, text):
        soup = BeautifulSoup(text)
        p_tags = soup.find_all('p')
        new_ps = []
        for tag in p_tags:
            strings = tag.strings
            new_p = soup.new_tag('p') 
            for str_item in strings:
                new_str = self._get_tremed_text(str_item)
                if new_str == str_item:
                    new_p.append(str(new_str))
                else:
                    new_p.append(str(new_str) + ' (...)')

            new_ps.append(new_p)
                
        soup.body.clear()
        for tag in new_ps:
            soup.body.append(tag)

        text_analyzer = get_current_registry().getUtility(ITextAnalyzer,
                                                          'text_analyzer')
        return text_analyzer.soup_to_text(soup)

    def _get_tremed_text(self, text):
        trimed_texts = []
        trimed_text = text
        if len(text) > 199:
            texts = text.split('\n')
            length = int(200 / len(texts))
            for t in texts:
                if len(t) > length-1:
                    t = t[:length]

                trimed_texts.append(t)

            trimed_text = "\n".join(trimed_texts)

        return trimed_text

    def get_description(self, field, cstruct): 
        description_template = 'novaideo:views/amendment_management/templates/description_amendments.pt'
        oid = cstruct[OBJECT_OID]
        current_user = get_current()
        try:
            subject = get_obj(oid)
            values = {'amendment': subject, 
                      'is_proposal': False, 
                      'current_user': current_user}
            if isinstance(subject, Proposal):
                values['text'] = self._get_trimed_proposal_text(subject.text)
                values['is_proposal'] = True
            else:
                seeamendment_actions = getBusinessAction(
                                         subject, self.request,
                                         'amendmentmanagement', 'see')
                if seeamendment_actions:
                    seeamendment_actions[0].execute(
                              subject, self.request, None)

                values['text'] = self._get_trimed_modification_text(
                                getattr(subject, 'explanationtext', ''))

            body = self.content(result=values, 
                                template=description_template)['body']
            return body
        except Exception:
            return {'amendment': None}


@view_config(
    name='voteforamendments',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class VoteViewMultipleView(MultipleView):
    title = _('Vote')
    name = 'voteforamendments'
    viewid = 'voteforamendments'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    item_template = 'novaideo:views/ballot_processes/templates/panel_item.pt'
    views = (VoteViewStudyReport, VoteFormView)
    validators = [Vote.get_validator()]
    requirements = {'css_links':[],
                    'js_links':['novaideo:static/js/explanation_amendment.js']}

    def get_message(self):
        ballot_report = None
        try:
            ballot_report = list(self.children[1].behaviorinstances.values())[0].process.ballot.report
        except Exception:
            pass

        return ballot_report.ballot.title


DEFAULTMAPPING_ACTIONS_VIEWS.update({Vote:VoteViewMultipleView})
