
from pyramid import renderers

from dace.objectofcollaboration.principal.util import Anonymous, has_role

from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.content.proposal import Proposal
from novaideo.content.person import Person
from novaideo.content.idea import Idea
from novaideo.content.amendment import Amendment
from novaideo.content.workspace import Workspace


def homepage_condition(context, user):
    return isinstance(user, Anonymous)


def homepage_connected_condition(context, user):
    return not isinstance(user, Anonymous)


def idea_not_examined(context, user):
    return 'examined' not in context.state


def not_version(context, user):
    return 'version' not in context.state


def idea_submitted_owner(context, user):
    return has_role(role=('Owner', context))


def idea_submitted_moderator(context, user):
    return has_role(role=('Moderator', ))


def proposal_proofreading_started(context, user):
    corrections_in_process = [c for c in context.corrections \
                              if 'in process' in c.state]
    return corrections_in_process and \
           not(corrections_in_process[0].author is user)


def proposal_proofreading_started_owner(context, user):
    corrections_in_process = [c for c in context.corrections \
                              if 'in process' in c.state]
    return corrections_in_process and \
           corrections_in_process[0].author is user


def proposal_proofreading_not_started(context, user):
    corrections_in_process = [c for c in context.corrections \
                              if 'in process' in c.state]
    return not corrections_in_process


def amendment_draft_explanation(context, user):
    return 'draft' in context.state and \
           'explanation' in context.state 


def amendment_draft(context, user):
    return 'draft' in context.state and \
           'explanation' not in context.state 


CONTEXTUAL_HELP_MESSAGES = {
	(NovaIdeoApplication, 'any', ''): [
	   (homepage_condition, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/homepage_message.pt', 1),
	   (homepage_connected_condition, 'novaideo:views/templates/panels/'
	   	           'contextual_help_messages/homepage_connected_message.pt', 1),
	   ],
    (NovaIdeoApplication, 'any', 'search'): [
	   (None, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/homepage_search.pt', 1),
	   ],
    (NovaIdeoApplication, 'any', 'analytics'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/analytics.pt', 1)],
	(NovaIdeoApplication, 'any', 'seemycontents'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/see_my.pt', 1)],

	(NovaIdeoApplication, 'any', 'seealerts'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/see_my.pt', 1)],

	(NovaIdeoApplication, 'any', 'seemyparticipations'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/see_my.pt', 1)],

	(NovaIdeoApplication, 'any', 'seemyselections'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/see_my.pt', 1)],

	(NovaIdeoApplication, 'any', 'seemysupports'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/see_my.pt', 1)],

	(NovaIdeoApplication, 'any', 'createidea'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/create_idea.pt', 1)],

	(NovaIdeoApplication, 'any', 'seeideastoexamine'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/ideas_to_examine.pt', 1)],

	(NovaIdeoApplication, 'any', 'proposalstoexamine'): [
	   (None, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposals_to_examine.pt', 1)],

	(NovaIdeoApplication, 'any', 'advanced_search'): [
	   (None, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/advanced_search.pt', 1)],

	(Proposal, 'draft', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/proposal_draft.pt', 1)],

	(Proposal, 'amendable', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/proposal_amendable.pt', 1)],

	(Proposal, 'amendable', 'improveproposal'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/proposal_improve.pt', 1)],

	(Proposal, 'amendable', 'improveproposalcorrection'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/proposal_improve.pt', 1)],

	(Proposal, 'amendable', 'improveproposalwiki'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/proposal_improve.pt', 1)],

	(Proposal, 'any', 'editproposal'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/edit_proposal.pt', 1)],

    (Proposal, 'submitted_support', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/proposal_submitted_support.pt', 1)],

	(Proposal, 'any', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/proposal_sub_helps.pt', 2)],

	(Proposal, 'open to a working group', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposal_open_to_a_working_group.pt', 1)],

	(Proposal, 'votes for publishing', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposal_first_vote.pt', 1)],

	(Proposal, 'any', 'makeopinionform'): [
	   (None, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposal_makeopinion.pt', 1)],

	(Proposal, 'examined', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposal_examined.pt', 1)],

	(Proposal, 'proofreading', 'index'): [
	   (proposal_proofreading_not_started, 'novaideo:views/templates/panels/'
	   	     'contextual_help_messages/proposal_proofreading_not_started.pt', 1),
	   (proposal_proofreading_started_owner, 'novaideo:views/templates/panels/'
	   	     'contextual_help_messages/proposal_proofreading_started_owner.pt', 1),
	   (proposal_proofreading_started, 'novaideo:views/templates/panels/'
	   	     'contextual_help_messages/proposal_proofreading_started.pt', 1)],

    (Workspace, 'any', 'addfilesws'): [
	   (None, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposal_workspace_addfiles.pt', 1)],

	(Workspace, 'any', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposal_workspace_index.pt', 1)],

	(Amendment, 'draft', 'index'): [
	   (amendment_draft, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/amendment_draft.pt', 1),
	   (amendment_draft_explanation, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/amendment_draft_explanation.pt', 1)],

	(Amendment, 'draft', 'submitamendment'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/amendment_prepare.pt', 1)],

	(Amendment, 'any', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/amendment_sub_helps.pt', 2)],

	(Person, 'any', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/person_index.pt', 1)],

	(Idea, 'to work', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_to_work.pt', 1)],
	(Idea, 'examined', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_examined.pt', 1)],
	   
	(Idea, 'any', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_sub_helps.pt', 2)],

    (Idea, 'to work', 'editidea'): [
       (None, 'novaideo:views/templates/panels/'
                            'contextual_help_messages/idea_to_work_edit.pt', 1)],

	(Idea, 'archived', 'index'): [
	   (not_version, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_archived.pt', 1)],
    (Idea, 'version', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_version.pt', 1)],
	(Idea, 'submitted', 'index'): [
	   (idea_submitted_owner, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_submitted_owner.pt', 1),
	   (idea_submitted_moderator, 'novaideo:views/templates/panels/'
	   	                'contextual_help_messages/idea_submitted_moderator.pt', 1)],
	(Idea, 'published', 'index'): [
	   (idea_not_examined, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_published.pt', 1)],
	(Idea, 'any', 'duplicateidea'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/duplicate_idea.pt', 1)],

	(Idea, 'any', 'publishasproposal'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/transform_idea.pt', 1)],
	(Idea, 'any', 'makeopinionformidea'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_makeopinion.pt', 1)],

}


def render_contextual_help(request, context, user, view_name):
    messages = [CONTEXTUAL_HELP_MESSAGES.get(
                   (context.__class__, s, view_name),
                   None)
                for s in context.state]
    messages.append(CONTEXTUAL_HELP_MESSAGES.get(
                    (context.__class__, 'any', view_name),
                    None))
    messages = [m for m in messages if m is not None]
    messages = [item for sublist in messages for item in sublist]
    messages = sorted(messages, key=lambda m: m[2])
    messages = [renderers.render(
                    m[1],
                    {'context': context,
                     'user': user},
                    request) for m in messages
                if m[0] is None or m[0](context, user)]
    return messages
