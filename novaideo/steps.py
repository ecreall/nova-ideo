import datetime
import pytz
from pyramid import renderers

from dace.util import getSite
from dace.objectofcollaboration.principal.util import get_current

from novaideo.content.processes import get_states_mapping
from novaideo.content.proposal import Proposal
from novaideo.content.workspace import Workspace
from novaideo.content.idea import Idea
from novaideo.content.amendment import Amendment
from novaideo import _


def days_hours_minutes(timed):
    return (timed.days,
           timed.seconds//3600,
           (timed.seconds//60) % 60,
           timed.seconds % 60)


class StepsPanel(object):
    step1_0_template = 'novaideo:views/templates/panels/step1_0.pt'
    step2_0_template = 'novaideo:views/templates/panels/step2_0.pt'
    step3_0_template = 'novaideo:views/templates/panels/step3_0.pt'
    step3_1_template = 'novaideo:views/templates/panels/step3_1.pt'
    step3_2_template = 'novaideo:views/templates/panels/step3_2.pt'
    step3_3_template = 'novaideo:views/templates/panels/step3_3.pt'
    step4_0_template = 'novaideo:views/templates/panels/step4.pt'
    step5_0_template = 'novaideo:views/templates/panels/step5_0.pt'

    def __init__(self):
        self.context = None
        self.request = None

    def _get_process_context(self):
        if isinstance(self.context, (Amendment, Workspace)):
            return self.context.proposal

        return self.context

    def _get_step1_informations(self, context, request):
        proposal_nember = len(context.related_proposals)
        duplicates_len = len(context.duplicates)
        return renderers.render(self.step1_0_template,
                                {'context': context,
                                 'proposal_nember': proposal_nember,
                                 'duplicates_len': duplicates_len},
                                request)

    def _get_step2_informations(self, context, request):
        related_ideas = context.related_ideas
        related_proposals = [idea.related_proposals
                             for idea in related_ideas]
        related_proposals = [item for sublist in related_proposals
                             for item in sublist]
        related_proposals = list(set(related_proposals))
        len_related_proposals = len(related_proposals)
        if context in related_proposals:
            len_related_proposals -= 1

        return renderers.render(self.step2_0_template,
                                {'context': context,
                                 'proposal_nember': len_related_proposals},
                                request)

    def _get_step3_informations(self, context, request):
        time_delta = None
        working_group = context.working_group
        process = working_group.improvement_cycle_proc
        is_closed = 'closed' in working_group.state
        user = get_current()
        working_group_states = [_(get_states_mapping(user, working_group, s))
                                for s in working_group.state]
        if 'amendable' in context.state and process:
            subprocesses = process['work'].sub_processes
            date_iteration = None
            if subprocesses:
                date_iteration = subprocesses[-1]['timer'].eventKind.time_date

            today = datetime.datetime.now()
            if date_iteration is not None and date_iteration > today:
                time_delta = date_iteration - today
                time_delta = days_hours_minutes(time_delta)

            return renderers.render(
                self.step3_1_template,
                {'context': context,
                 'working_group_states': working_group_states,
                 'is_closed': is_closed,
                 'duration': time_delta,
                 'process': process},
                request)
        elif 'votes for publishing' in context.state:
            ballot = working_group.vp_ballot
            today = datetime.datetime.now(tz=pytz.UTC)
            if ballot.finished_at is not None and ballot.finished_at > today:
                time_delta = ballot.finished_at - today
                time_delta = days_hours_minutes(time_delta)

            return renderers.render(
                self.step3_3_template,
                {'context': context,
                 'working_group_states': working_group_states,
                 'is_closed': is_closed,
                 'duration': time_delta,
                 'process': process,
                 'ballot_report': ballot.report},
                request)
        elif 'votes for amendments' in context.state:
            voters = []
            [voters.extend(b.report.voters)
             for b in working_group.amendments_ballots]
            voters = list(set(voters))
            ballot = working_group.amendments_ballots[-1]
            today = datetime.datetime.now(tz=pytz.UTC)
            if ballot.finished_at is not None and ballot.finished_at > today:
                time_delta = ballot.finished_at - today
                time_delta = days_hours_minutes(time_delta)

            return renderers.render(
                self.step3_2_template,
                {'context': context,
                 'working_group_states': working_group_states,
                 'is_closed': is_closed,
                 'duration': time_delta,
                 'process': process,
                 'ballot_report': ballot.report,
                 'voters': voters},
                request)
        elif 'open to a working group' in context.state:
            participants_mini = getSite().participants_mini
            work_mode = getattr(working_group, 'work_mode', None)
            if work_mode:
                participants_mini = work_mode.participants_mini

            return renderers.render(
                self.step3_0_template,
                {'context': context,
                 'process': process,
                 'min_members': participants_mini},
                request)

        return _('Information unvailable.')

    def _get_step4_informations(self, context, request):
        user = get_current()
        support = 0
        if any(t.owner is user for t in context.tokens_support):
            support = 1
        elif any(t.owner is user for t in context.tokens_opposition):
            support = -1

        return renderers.render(self.step4_0_template,
                                {'context': context,
                                 'support': support},
                                request)

    def _get_step5_informations(self, context, request):
        return renderers.render(self.step5_0_template,
                                {'context': context},
                                request)

    def __call__(self, context, request):
        self.context = context
        self.request = request
        if getattr(self.request, 'is_idea_box', False):
            return {'condition': False}

        result = {}
        context = self._get_process_context()
        result['condition'] = isinstance(context, (Proposal, Idea))
        result['current_step'] = 1
        result['step1_message'] = ""
        result['step2_message'] = ""
        result['step3_message'] = ""
        result['step4_message'] = ""
        result['step5_message'] = ""
        if isinstance(context, Proposal):
            if 'draft' in context.state:
                result['current_step'] = 2
                result['step2_message'] = self._get_step2_informations(
                    context, self.request)
            elif self.request.support_proposals and \
                 'submitted_support' in context.state:
                result['current_step'] = 4
                result['step4_message'] = self._get_step4_informations(
                    context, self.request)
            elif 'proposal' in self.request.content_to_examine and\
                 'examined' in context.state:
                result['current_step'] = 5
                result['step5_message'] = self._get_step5_informations(
                    context, self.request)
            elif not ('examined' in context.state or \
                      'submitted_support' in context.state or\
                      'archived' in context.state):
                result['current_step'] = 3
                result['step3_message'] = self._get_step3_informations(
                    context, self.request)
            elif 'examined' in context.state or \
                 'submitted_support' in context.state or\
                 'archived' in context.state:
                result['current_step'] = 0

        if isinstance(context, Idea):
            result['step1_message'] = self._get_step1_informations(
                context, self.request)

        return result


steps_panels = StepsPanel()
