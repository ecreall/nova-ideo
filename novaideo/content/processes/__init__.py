# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
from webob.multidict import MultiDict
from pyramid.threadlocal import get_current_registry, get_current_request

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
        'draft': _('Draft'),
        'submitted_support': _('Submitted for support'),
        'published': _('Published'),
	    'open to a working group': _('Open to a working group'),
	    'votes for publishing': _('Votes for publishing'),
	    'votes for amendments': _('Votes for amendments'),
	    'amendable': _('Being improved'),
	    'archived': _('Archived'),
	    'examined': _('Examined'),
	    'favorable': _('Favorable'),
	    'to_study': _('To study'),
	    'unfavorable': _('Unfavorable'),

    },
    'idea': {
	    'to work': _('To work'),
        'submitted_support': _('Submitted for support'),
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
	    'deactivated': _('Inactive'),
	    'closed': _('Closed'),
        'archived': _('Archived', context='workinggroup')
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
        'draft': _('Draft'),
        'submitted_support': _('Submitted for support'),
        'published': _('Published'),
	    'open to a working group': _('Open to a working group'),
	    'votes for publishing': _('Votes for publishing'),
	    'votes for amendments': _('Votes for amendments'),
	    'amendable': _('Being improved'),
	    'archived': _('Archived'),
	    'examined': _('Examined'),
	    'favorable': _('Favorable'),
	    'to_study': _('To study'),
	    'unfavorable': _('Unfavorable'),

    },
    'idea': {
	    'to work': _('To work'),
        'submitted_support': _('Submitted for support'),
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
	    'deactivated': _('Inactive'),
	    'closed': _('Closed'),
        'archived': _('Archived', context='workinggroup')
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


def get_content_types_states(content_types, flatten=False, request=None):
    if request is None:
        request = get_current_request()

    root = request.root
    results = {c: dict(STATES_PARTICIPANT_MAPPING.get(
        c, STATES_PARTICIPANT_MAPPING.get('default')))
        for c in content_types}

    if 'idea' in results:
        if not getattr(root, 'moderate_ideas', False):
            results['idea'].pop('submitted')

        if 'idea' not in getattr(root, 'content_to_examine', []):
            results['idea'].pop('examined')
            results['idea'].pop('favorable')
            results['idea'].pop('unfavorable')
            results['idea'].pop('to_study')

        if 'idea' not in getattr(root, 'content_to_support', []):
            results['idea'].pop('submitted_support')

    if 'proposal' in results:
        modes = root.get_work_modes()
        if 'amendment' not in modes:
            results['proposal'].pop('votes for amendments')

        if 'proposal' not in getattr(root, 'content_to_examine', []):
            results['proposal'].pop('examined')
            results['proposal'].pop('favorable')
            results['proposal'].pop('unfavorable')
            results['proposal'].pop('to_study')

        if 'proposal' not in getattr(root, 'content_to_support', []):
            results['proposal'].pop('submitted_support')

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
