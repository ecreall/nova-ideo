
from dace.objectofcollaboration.principal.util import has_role

from novaideo.core import _


STATES_PARTICIPANT_MAPPING = {
         #Commun
	    'draft': _('Draft'),
	    'published': _('Published'),
	    'archived': _('Archived'),
        #Amendment
	    'explanation': _('Explanation'),
	    #Ideas
	    'to work': _('To work'),
	    #Invitation
	    'pending': _('Pending'),
	    'accepted': _('Accepted'),
	    'refused': _('Refused'),
	    #Proposal
	    'open to a working group': _('Open to a working group'),
	    'votes for publishing': _('Votes for publishing'),
	    'votes for amendments': _('Votes for amendments'),
	    'proofreading': _('Proofreading'),
	    'amendable': _('Amendable'),
	    #Correction
	    'in process': _('In process'),
	    'processed': _('Processed'),
	    #Working group, Person
	    'active': _('Active'),
	    'deactivated': _('Deactivated'),
	    #Working group
	    'closed': _('Closed')
         }


STATES_MEMBER_MAPPING = {
         #Commun
	    'draft': _('Draft'),
	    'published': _('Published'),
	    'archived': _('Archived'),
        #Amendment
	    'explanation': _('Explication'),
	    #Ideas
	    'to work': _('To work'),
	    #Invitation
	    'pending': _('Pending'),
	    'accepted': _('Accepted'),
	    'refused': _('Refused'),
	    #Proposal
	    'open to a working group': _('Open to a working group'),
	    'votes for publishing': _('Votes for publishing'),
	    'votes for amendments': _('Votes for amendments'),
	    'proofreading': _('Proofreading'),
	    'amendable': _('Amendable'),
	    #Correction
	    'in process': _('In process'),
	    'processed': _('Processed'),
	    #Working group, Person
	    'active': _('Active'),
	    'deactivated': _('Deactivated'),
	    #Working group
	    'closed': _('Closed')
         }


def get_states_mapping(user, context, state):
    #TODO
    return STATES_PARTICIPANT_MAPPING.get(state, None)