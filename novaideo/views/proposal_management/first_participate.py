from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view_operation import MultipleView
from pontus.view import BasicView
from pontus.default_behavior import Cancel


from novaideo.content.processes.proposal_management.behaviors import (
    FirstParticipate)
from novaideo.content.proposal import Proposal
from novaideo import _
from .submit_proposal import SubmitProposalFormView



class FirstParticipateViewStudyReport(BasicView):
    title = _('Participate')
    name = 'firstparticipatestudy'
    template = 'novaideo:views/proposal_management/templates/first_vote.pt'

    def update(self):
        result = {}
        duration_ballot_report = None
        vp_ballot = None
        try:
            voteform_view = self.parent.validated_children[1]
            voteform_actions = list(voteform_view.behaviors_instances.values())
            duration_ballot_report = voteform_actions[0].process.\
                                           duration_configuration_ballot.\
                                           report
            vp_ballot = voteform_actions[0].process.\
                                           vp_ballot.\
                                           report
        except Exception:
            pass

        values = {'context': self.context, 
                  'duration_ballot_report': duration_ballot_report,
                  'vp_ballot_report': vp_ballot,}
        body = self.content(args=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


class FirstParticipateFormView(SubmitProposalFormView):
    title =  _('Vote')
    name = 'firstparticipateform'
    formid = 'formfirstparticipate'
    behaviors = [FirstParticipate, Cancel]


@view_config(
    name='firstparticipate',
    context=Proposal,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class FirstParticipateViewMultipleView(MultipleView):
    title = _('Participer au groupe de travail')
    name = 'firstparticipate'
    viewid = 'firstparticipate'
    template = 'daceui:templates/mergedmultipleview.pt'
    views = (FirstParticipateViewStudyReport, FirstParticipateFormView)
    validators = [FirstParticipate.get_validator()]


DEFAULTMAPPING_ACTIONS_VIEWS.update({FirstParticipate: FirstParticipateViewMultipleView})