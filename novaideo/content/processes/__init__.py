# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
from webob.multidict import MultiDict
from pyramid.threadlocal import get_current_registry

from dace.objectofcollaboration.principal.util import has_role

from novaideo.core import _


STATES_PARTICIPANT_MAPPING = {
    'default': {
        'draft': _('Draft'),
        'published': _('Published'),
        'archived': _('Archived')
    },
    'amendment': {
        'draft': _('In preparation'),
	    'submitted': _('Submitted'),
	    'explanation': _('Explanation'),
        'archived': _('Archived')
    },
    'correction': {
        'in process': _('In process'),
	    'processed': _('Processed'),
    },
    'proposal': {
        'submitted_support': _('Submitted for support'),
        'published': _('Published'),
	    'open to a working group': _('Open to a working group'),
	    'votes for publishing': _('Votes for publishing'),
	    'votes for amendments': _('Votes for amendments'),
	    'amendable': _('Amendable'),
	    'archived': _('Archived'),
	    'examined': _('Examined'),
	    'favorable': _('Favorable'),
	    'to_study': _('To study'),
	    'unfavorable': _('Unfavorable'),

    },
    'idea': {
	    'to work': _('To work'),
	    'submitted': _('Submitted for moderation'),
	    'archived': _('Archived'),
	    'examined': _('Examined'),
	    'favorable': _('Favorable'),
	    'to_study': _('To study'),
	    'unfavorable': _('Unfavorable'),
	    'published': _('Published')
    },
    'invitation': {
	    'pending': _('Pending'),
	    'accepted': _('Accepted'),
	    'refused': _('Refused')
	},
	'person': {
        'active': _('Active'),
	    'deactivated': _('Deactivated')
	},
	'workinggroup': {
		'active': _('Active'),
	    'deactivated': _('Deactivated'),
	    'closed': _('Closed')
	}
}

STATES_MEMBER_MAPPING = {
    'default': {
        'draft': _('Draft'),
        'published': _('Published'),
        'archived': _('Archived')
    },
    'amendment': {
        'draft': _('In preparation'),
	    'submitted': _('Submitted'),
	    'explanation': _('Explanation'),
        'archived': _('Archived')
    },
    'correction': {
        'in process': _('In process'),
	    'processed': _('Processed'),
    },
    'proposal': {
        'submitted_support': _('Submitted for support'),
        'published': _('Published'),
	    'open to a working group': _('Open to a working group'),
	    'votes for publishing': _('Votes for publishing'),
	    'votes for amendments': _('Votes for amendments'),
	    'amendable': _('Amendable'),
	    'archived': _('Archived'),
	    'examined': _('Examined'),
	    'favorable': _('Favorable'),
	    'to_study': _('To study'),
	    'unfavorable': _('Unfavorable'),

    },
    'idea': {
	    'to work': _('To work'),
	    'submitted': _('Submitted for moderation'),
	    'archived': _('Archived'),
	    'examined': _('Examined'),
	    'favorable': _('Favorable'),
	    'to_study': _('To study'),
	    'unfavorable': _('Unfavorable'),
	    'published': _('Published')
    },
    'invitation': {
	    'pending': _('Pending'),
	    'accepted': _('Accepted'),
	    'refused': _('Refused')
	},
	'person': {
        'active': _('Active'),
	    'deactivated': _('Deactivated')
	},
	'workinggroup': {
		'active': _('Active'),
	    'deactivated': _('Deactivated'),
	    'closed': _('Closed')
	}
}


def get_flattened_mapping(mapping):
    result = [list(s.items()) for s in mapping.values()]
    result = list(set([item for sublist in result for item in sublist]))
    result = MultiDict(result).dict_of_lists()
    return result


FLATTENED_STATES_MEMBER_MAPPING = get_flattened_mapping(
    STATES_MEMBER_MAPPING)


FLATTENED_STATES_PARTICIPANT_MAPPING = get_flattened_mapping(
    STATES_PARTICIPANT_MAPPING)


def get_content_types_states(content_types, flatten=False):
    results = {c: dict(STATES_PARTICIPANT_MAPPING.get(
        c, STATES_PARTICIPANT_MAPPING.get('default')))
        for c in content_types}

    if flatten:
        return get_flattened_mapping(results)

    return results


def get_states_mapping(user, context, state):
    """get the state of the context"""
    registry = get_current_registry()
    content_type = registry.content.typeof(context)
    result = STATES_PARTICIPANT_MAPPING.get(
        content_type, STATES_PARTICIPANT_MAPPING.get('default'))
    return result.get(state, None)


# STATES_PARTICIPANT_MAPPING = {
#          #Commun
# 	    'draft': {'amendment':_('In preparation'),
# 	              'default': _('Draft')},
# 	    #state by context. 'default' key is required!
# 	    'published': {'proposal':_('Submitted'),
# 	                  'amendment':_('Submitted'),
# 	                  'default': _('Published')},
# 	    'archived': _('Archived'),
#         #Amendment
# 	    'explanation': _('Explanation'),
# 	    #Ideas
# 	    'to work': _('To work'),
# 	    'submitted': _('Submitted for moderation'),
# 	    #Invitation
# 	    'pending': _('Pending'),
# 	    'accepted': _('Accepted'),
# 	    'refused': _('Refused'),
# 	    #Proposal
# 	    'open to a working group': _('Open to a working group'),
# 	    'votes for publishing': _('Votes for publishing'),
# 	    'votes for amendments': _('Votes for amendments'),
# 	    'amendable': _('Amendable'),
# 	    #Proposal, Idea
# 	    'examined': _('Examined'),
# 	    'favorable': _('Favorable'),
# 	    'to_study': _('To study'),
# 	    'unfavorable': _('Unfavorable'),
# 	    #Correction
# 	    'in process': _('In process'),
# 	    'processed': _('Processed'),
# 	    #Working group, Person
# 	    'active': _('Active'),
# 	    'deactivated': _('Deactivated'),
# 	    #Working group
# 	    'closed': _('Closed')
#          }


#states by memeber
# STATES_MEMBER_MAPPING = {
#          #Commun
# 	    'draft': {'amendment':_('In preparation'),
# 	              'default': _('Draft')},
# 	    #state by context. 'default' key is required!
# 	    'published': {'proposal':_('Submitted'),
# 	                  'amendment':_('Submitted'),
# 	                  'default': _('Published')},
# 	    'archived': _('Archived'),
#         #Amendment
# 	    'explanation': _('Explanation'),
# 	    #Ideas
# 	    'to work': _('To work'),
# 	    'submitted': _('Submitted for moderation'),
# 	    #Invitation
# 	    'pending': _('Pending'),
# 	    'accepted': _('Accepted'),
# 	    'refused': _('Refused'),
# 	    #Proposal
# 	    'open to a working group': _('Open to a working group'),
# 	    'votes for publishing': _('Votes for publishing'),
# 	    'votes for amendments': _('Votes for amendments'),
# 	    'amendable': _('Amendable'),
# 	    #Proposal, Idea
# 	    'examined': _('Examined'),
# 	    'favorable': _('Favorable'),
# 	    'to_study': _('To study'),
# 	    'unfavorable': _('Unfavorable'),
# 	    #Correction
# 	    'in process': _('In process'),
# 	    'processed': _('Processed'),
# 	    #Working group, Person
# 	    'active': _('Active'),
# 	    'deactivated': _('Deactivated'),
# 	    #Working group
# 	    'closed': _('Closed')
#          }
