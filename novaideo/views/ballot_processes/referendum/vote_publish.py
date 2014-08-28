from pyramid.view import view_config

from dace.util import get_obj
from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.form import FormView
from pontus.view_operation import MultipleView
from pontus.schema import select
from pontus.view import BasicView, View, merge_dicts, ViewError
from pontus.default_behavior import Cancel

from novaideo.content.processes.ballot_processes.referendum.behaviors import  Favour, Against
from novaideo.content.proposal import Proposal
from novaideo import _



class VoteViewStudyReport(BasicView):
    title = _('Vote for publication')
    name='voteforpublication'
    template ='novaideo:views/ballot_processes/referendum/templates/vote_for_publication.pt'

    def update(self):
        result = {}
        ballot_report = None
        try:
            ballot_report = self.parent.children[1].behaviorinstances.values()[0].process.ballot.report
        except Exception:
            pass

        values = {'context': self.context, 'ballot_report': ballot_report}
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class VoteFormView(FormView):
    title =  _('Vote')
    name ='voteform'
    formid = 'formvote'
    behaviors = [Favour, Against]
    validate_behaviors = False


@view_config(
    name='votepublishing',
    context=Proposal,
    renderer='pontus:templates/view.pt',
    )
class VoteViewMultipleView(MultipleView):
    title = _('Vote')
    name = 'votepublishing'
    viewid = 'votepublishing'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    views = (VoteViewStudyReport, VoteFormView)
    validators = [Favour.get_validator(), Against.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({Favour:VoteViewMultipleView})
DEFAULTMAPPING_ACTIONS_VIEWS.update({Against:VoteViewMultipleView})
