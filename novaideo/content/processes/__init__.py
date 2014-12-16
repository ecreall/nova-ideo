# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from dace.objectofcollaboration.principal.util import has_role

from novaideo.content.proposal import Proposal
from novaideo.core import _


STATES_PARTICIPANT_MAPPING = {
         #Commun
	    'draft': _('Draft'),
	    #state by context. 'default' key is required!
	    'published': {Proposal:_('Submited'),
	                  'default': _('Published')},
	    'archived': _('Archived'),
        #Amendment
	    'explanation': _('Explanation'),
	    #Ideas
	    'to work': _('To work'),
	    'submited': _('Submited'),
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


#states by memeber
STATES_MEMBER_MAPPING = {
         #Commun
	    'draft': _('Draft'),
	    'published': {Proposal:_('Submited'),
	                  'default': _('Published')},
	    'archived': _('Archived'),
        #Amendment
	    'explanation': _('Explanation'),
	    #Ideas
	    'to work': _('To work'),
	    'submited': _('Submited'),
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
    """get the state of the context"""
    result = STATES_PARTICIPANT_MAPPING.get(state, None)
    if isinstance(result, dict):
        return result.get(context.__class__, result['default'])

    return result