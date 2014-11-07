
import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.entity import Entity
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.schema import Schema
from pontus.widget import Select2Widget

from novaideo.content.processes.ballot_processes.fptp.behaviors import  Vote
from novaideo.content.proposal import Proposal
from novaideo import _


class VoteViewStudyReport(BasicView):
    title = _('FPTP vote')
    name = 'votefptp'
    template = 'novaideo:views/ballot_processes/fptp/templates/fptp_vote.pt'

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



def subjects_choice(ballot_report):
    subjects = ballot_report.subjects
    def get_title(ob):
        if isinstance(ob, Entity):
            return ob.title
        else:
            return ob

    values = [(i, get_title(i)) for i in subjects]
    values = sorted(values, key=lambda e: e[1])
    return Select2Widget(values=values)



class CondidatesSchema(Schema):

    elected = colander.SchemaNode(
            colander.String(),
            title=_('Choices'),
            default=[],
        )
    

class VoteFormView(FormView):
    title =  _('Vote')
    name = 'voteform'
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

        subjects_widget = subjects_choice(ballot_report)
        self.schema.get('elected').widget = subjects_widget
        self.schema.view = self


@view_config(
    name='votefptp',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class VoteViewMultipleView(MultipleView):
    title = _('Vote')
    name = 'votefptp'
    viewid = 'votefptp'
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
