
import colander
import re
import html2text
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.util import get_obj
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
    values = [(i, i) for i in judgments]
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

    def _get_added_texts(self, text):
        result = text.split("<ins>")
        result = [r.split("</ins>") for r in result]
        result = [r for r in  result if len(r)>1]
        result = [r[0] for r in result]
        result = "..."+"...<br />...".join(result)+"..."
        return result

    def _get_trimed_text(self, text):
        trimed_text =html2text.html2text(text)
        trimed_texts = []
        if len(trimed_text) > 499:
            texts = trimed_text.split('\n')
            length = int(500 / len(texts))
            for t in texts:
                if len(t) > length-1:
                    t = t[:length]
                    t = re.sub('\s[a-z0-9._-]+$', ' <b>...</b>', t)

                trimed_texts.append(t)

            trimed_text = "\n".join(trimed_texts)

        return trimed_text

    def get_description(self, field, cstruct): 
        description_template = 'novaideo:views/amendment_management/templates/description_amendments.pt'
        oid = cstruct[OBJECT_OID]
        current_user = get_current()
        try:
            object = get_obj(oid)
            values = {'amendment': object, 'is_proposal': False, 'current_user': current_user}
            if isinstance(object, Proposal):
                values['text'] = self._get_trimed_text(object.text)
                values['is_proposal'] = True
            else:
                text_analyzer = get_current_registry().getUtility(ITextAnalyzer,'text_analyzer')
                soup, textdiff =  text_analyzer.render_html_diff(getattr(self.context, 'text', ''), getattr(object, 'text', ''))
                values['text'] = self._get_added_texts(textdiff)

            body = self.content(result=values, template=description_template)['body']
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

    def get_message(self):
        ballot_report = None
        try:
            ballot_report = list(self.children[1].behaviorinstances.values())[0].process.ballot.report
        except Exception:
            pass

        return ballot_report.ballot.title


DEFAULTMAPPING_ACTIONS_VIEWS.update({Vote:VoteViewMultipleView})
