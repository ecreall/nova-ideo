import colander
import deform
import htmldiff
import re
import html2text
from pyramid.view import view_config

from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.schema import select
from pontus.view import BasicView, View, merge_dicts, ViewError
from pontus.default_behavior import Cancel
from pontus.schema import select, omit, Schema
from pontus.widget import RadioChoiceWidget

from novaideo.content.processes.ballot_processes.majorityjudgment.behaviors import  Vote
from novaideo.content.proposal import Proposal
from novaideo.content.amendment import AmendmentSchema
from novaideo import _
from novaideo.views.widget import InLineWidget, ObjectWidget
from pontus.file import OBJECT_OID


class VoteViewStudyReport(BasicView):
    title = _('Vote for amendments')
    name='voteforamendments'
    template ='novaideo:views/ballot_processes/majorityjudgment/templates/vote_for_amendments.pt'

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
    judgments = sorted(judgments.keys(), key=lambda o: judgments[o], reverse=True )
    values = [(i, i) for i in judgments]
    widget = RadioChoiceWidget(values=values)
    #widget.template = 'novaideo:views/idea_management/templates/radio_choice.pt'
    return widget


class CondidateSchema(Schema):

    judgment = colander.SchemaNode(
        colander.String(),
        title=_('Judgment')
        )
    
class CondidatesSchema(Schema):
    condidates =  colander.SchemaNode(
        colander.Sequence(),
        omit(CondidateSchema(widget=ObjectWidget() ,editable=True, name='condidate', omit=['judgment']),['_csrf_token_']),
        widget=InLineWidget(),
        title='Condidates'
        )

class VoteFormView(FormView):
    title =  _('Vote')
    name ='voteform'
    formid = 'formvote'
    behaviors = [Vote]
    validate_behaviors = False
    schema = CondidatesSchema()

    def before_update(self):
        ballot_report = None
        try:
            ballot_report = list(self.behaviorinstances.values())[0].process.ballot.report
        except Exception:
            return

        judgments_widget = judgments_choice(ballot_report)
        self.schema.get('condidates').children[0].get('judgment').widget = judgments_widget
        self.schema.get('condidates').children[0].editable = False
        self.schema.view = self


    def default_data(self):
        ballot_report = None
        try:
            ballot_report = list(self.behaviorinstances.values())[0].process.ballot.report
        except Exception:
            return
        
        return {'condidates': ballot_report.subjects}

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
        try:
            object = get_obj(oid)
            values = {'amendment': object, 'is_proposal': False}
            if isinstance(object, Proposal):
                values['text'] = self._get_trimed_text(object.text)
                values['is_proposal'] = True
            else:
                textdiff = htmldiff.render_html_diff(getattr(self.context, 'text', ''), getattr(object, 'text', ''))
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
    item_template = 'novaideo:views/proposal_management/templates/panel_item.pt'
    views = (VoteViewStudyReport, VoteFormView)
    validators = [Vote.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({Vote:VoteViewMultipleView})
