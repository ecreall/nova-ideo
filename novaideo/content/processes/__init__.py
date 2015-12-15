# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
from webob.multidict import MultiDict
from pyramid.threadlocal import get_current_registry

from dace.objectofcollaboration.principal.util import has_role

from novaideo.core import _


STATES_PARTICIPANT_MAPPING = {
         #Commun
	    'draft': {'amendment':_('In preparation'),
	              'default': _('Draft')},
	    #state by context. 'default' key is required!
	    'published': {'proposal':_('Submitted'),
	                  'amendment':_('Submitted'),
	                  'default': _('Published')},
	    'archived': _('Archived'),
        #Amendment
	    'explanation': _('Explanation'),
	    #Ideas
	    'to work': _('To work'),
	    'submited': _('Submitted for moderation'),
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
	    #Proposal, Idea
	    'examined': _('Examined'),
	    'favorable': _('Favorable'),
	    'to_study': _('To study'),
	    'unfavorable': _('Unfavorable'),
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
	    'draft': {'amendment':_('In preparation'),
	              'default': _('Draft')},
	    #state by context. 'default' key is required!
	    'published': {'proposal':_('Submitted'),
	                  'amendment':_('Submitted'),
	                  'default': _('Published')},
	    'archived': _('Archived'),
        #Amendment
	    'explanation': _('Explanation'),
	    #Ideas
	    'to work': _('To work'),
	    'submited': _('Submitted for moderation'),
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
	    #Proposal, Idea
	    'examined': _('Examined'),
	    'favorable': _('Favorable'),
	    'to_study': _('To study'),
	    'unfavorable': _('Unfavorable'),
	    #Correction
	    'in process': _('In process'),
	    'processed': _('Processed'),
	    #Working group, Person
	    'active': _('Active'),
	    'deactivated': _('Deactivated'),
	    #Working group
	    'closed': _('Closed')
         }


def get_flattened_mapping(mapping):
    result = MultiDict({key: value for key, value in
              mapping.items() if not isinstance(value, dict)})
    for key, value in mapping.items():
        if key not in result:
            values = set(value.values())
            for newvalue in values:
                result[key] = newvalue

    return result


FLATTENED_STATES_MEMBER_MAPPING = get_flattened_mapping(STATES_MEMBER_MAPPING)


FLATTENED_STATES_PARTICIPANT_MAPPING = get_flattened_mapping(STATES_PARTICIPANT_MAPPING)


def get_states_mapping(user, context, state):
    """get the state of the context"""
    registry = get_current_registry()
    content_type = registry.content.typeof(context)
    result = STATES_PARTICIPANT_MAPPING.get(state, None)
    if isinstance(result, dict):
        return result.get(content_type, result['default'])

    return result
