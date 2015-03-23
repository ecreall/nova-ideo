
from dace.objectofcollaboration.principal.util import Anonymous, has_role

from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.content.proposal import Proposal
from novaideo.content.person import Person
from novaideo.content.idea import Idea


def homepage_condition(context, user):
    return isinstance(user, Anonymous) 


def homepage_connected_condition(context, user):
    return not isinstance(user, Anonymous) 


def idea_submited_owner(context, user):
    return has_role(role=('Owner', context))


def idea_submited_moderator(context, user):
    return has_role(role=('Moderator', ))


def proposal_first_vote(context, user):
    return context.creator and getattr(context.creator, 'iteration', 1) == 1


CONTEXTUAL_HELP_MESSAGES = {
	(NovaIdeoApplication, 'any', ''): [
	   (homepage_condition, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/homepage_message.pt', 1),
	   (homepage_connected_condition, 'novaideo:views/templates/panels/'
	   	           'contextual_help_messages/homepage_connected_message.pt', 1)],

	(NovaIdeoApplication, 'any', 'seemycontents'): [
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

	(Proposal, 'draft', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/proposal_draft.pt', 1)],

	(Proposal, 'any', 'editproposal'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/edit_proposal.pt', 1)],

	(Proposal, 'any', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/proposal_sub_helps.pt', 2)],

	(Proposal, 'open to a working group', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposal_open_to_a_working_group.pt', 1)],

	(Proposal, 'votes for publishing', 'index'): [
	   (proposal_first_vote, 'novaideo:views/templates/panels/'
	   	      'contextual_help_messages/proposal_first_vote.pt', 1)],

	(Person, 'any', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/person_index.pt', 1)],

	(Idea, 'to work', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_to_work.pt', 1)],
	   
	(Idea, 'any', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_sub_helps.pt', 2)],

	(Idea, 'archived', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_archived.pt', 1)],

	(Idea, 'submited', 'index'): [
	   (idea_submited_owner, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_submited_owner.pt', 1),
	   (idea_submited_moderator, 'novaideo:views/templates/panels/'
	   	                'contextual_help_messages/idea_submited_moderator.pt', 1)],

	(Idea, 'published', 'index'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/idea_published.pt', 1)],

	(Idea, 'any', 'duplicateidea'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/duplicate_idea.pt', 1)],

	(Idea, 'any', 'publishasproposal'): [
	   (None, 'novaideo:views/templates/panels/'
	   	                    'contextual_help_messages/transform_idea.pt', 1)],

}

